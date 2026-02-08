import { User } from "@/types";

const AUTH_TOKEN_KEY = "auth_token";
const AUTH_USER_KEY = "auth_user";
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "https://shahidali1-separate-backend.hf.space";

interface SignInResponse {
  user: User;
  token: string;
}

interface SignUpResponse {
  user: User;
  token: string;
}

interface ApiErrorResponse {
  detail: string;
}

export class AuthApiError extends Error {
  public statusCode?: number;
  public details?: any;

  constructor(message: string, statusCode?: number, details?: any) {
    super(message);
    this.name = "AuthApiError";
    this.statusCode = statusCode;
    this.details = details;
  }
}

async function authApiRequest<T>(endpoint: string, options: RequestInit = {}): Promise<T> {
  const token = localStorage.getItem(AUTH_TOKEN_KEY);
  const headers = new Headers(options.headers);
  headers.set("Content-Type", "application/json");

  if (token) headers.set("Authorization", `Bearer ${token}`);

  const response = await fetch(`${API_BASE_URL}${endpoint}`, { ...options, headers });

  if (!response.ok) {
    let msg = `HTTP error ${response.status}`;
    try {
      const data = (await response.json()) as ApiErrorResponse;
      msg = data.detail || msg;
    } catch {}
    throw new AuthApiError(msg, response.status);
  }

  if (response.status === 204) return {} as T;
  return await response.json();
}


export async function signIn(email: string, password: string): Promise<SignInResponse> {
  const response = await authApiRequest<any>(
    `/api/auth/login?email=${encodeURIComponent(email)}&password=${encodeURIComponent(password)}`,
    { method: "POST" }
  );

  if (!response.access_token) throw new Error("No access token from server");

  const token = response.access_token;
  let userId = "";
  let decodedEmail = email;

  try {
    const parts = token.split(".");
    if (parts.length === 3) {
      const payload = JSON.parse(atob(parts[1]));
      userId = payload.sub || "";
      decodedEmail = payload.email || decodedEmail;
    }
  } catch (e) {
    console.error("JWT decode failed:", e);
  }

  const user: User = { userId, email: decodedEmail };

  localStorage.setItem(AUTH_TOKEN_KEY, token);
  localStorage.setItem(AUTH_USER_KEY, JSON.stringify(user));

  document.cookie = `auth_token=${token}; path=/; secure; samesite=lax`;

  window.dispatchEvent(new StorageEvent("storage", { key: AUTH_TOKEN_KEY, newValue: token }));

  return { user, token };
}


export async function signUp(firstName: string, lastName: string, email: string, password: string): Promise<SignInResponse> {
  const response = await authApiRequest<any>("/api/auth/register", {
    method: "POST",
    body: JSON.stringify({ firstName, lastName, email, password }),
  });

  if (!response || !response.id || !response.email) throw new Error("Invalid response from server");

  const user: User = { userId: response.id, email: response.email };

  const { token } = await signIn(email, password);

  return { user, token };
}


export function signOut(): void {
  localStorage.removeItem(AUTH_TOKEN_KEY);
  localStorage.removeItem(AUTH_USER_KEY);

  document.cookie =
    "auth_token=; path=/; expires=Thu, 01 Jan 1970 00:00:00 GMT";

  window.location.href = "/signin";
}

export function checkAuthState(): { isAuthenticated: boolean; user: User | null } {
  const token = localStorage.getItem(AUTH_TOKEN_KEY);
  const userStr = localStorage.getItem(AUTH_USER_KEY);

  if (token && userStr) {
    try {
      const user = JSON.parse(userStr) as User;
      return { isAuthenticated: true, user };
    } catch (e) {
      console.error("User parse error:", e);
    }
  }
  return { isAuthenticated: false, user: null };
}

export function getAuthToken(): string | null {
  return localStorage.getItem(AUTH_TOKEN_KEY);
}

