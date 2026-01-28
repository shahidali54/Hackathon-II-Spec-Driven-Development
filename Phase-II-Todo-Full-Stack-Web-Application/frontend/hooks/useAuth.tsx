"use client";

import { createContext, useContext, useState, useEffect, useCallback, ReactNode } from "react";
import { useRouter } from "next/navigation";
import { signIn as authSignIn, signUp as authSignUp, signOut as authSignOut, checkAuthState } from "@/lib/auth";
import type { AuthState } from "@/types";

interface AuthContextType extends AuthState {
  signIn: (email: string, password: string) => Promise<void>;
  signUp: (firstName: string, lastName: string, email: string, password: string) => Promise<void>;
  signOut: () => void;
  clearError: () => void;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: ReactNode }) {
  const router = useRouter();
  const [state, setState] = useState<AuthState>({ user: null, isAuthenticated: false, isLoading: true, error: null });

  useEffect(() => {
    const { isAuthenticated, user } = checkAuthState();
    setState({ user, isAuthenticated, isLoading: false, error: null });
  }, []);

  useEffect(() => {
    const handleStorageChange = (e: StorageEvent) => {
      if (e.key === "auth_token" && !e.newValue) {
        setState({ user: null, isAuthenticated: false, isLoading: false, error: null });
        router.push("/auth/signin");
      }
    };
    window.addEventListener("storage", handleStorageChange);
    return () => window.removeEventListener("storage", handleStorageChange);
  }, [router]);

  const signIn = useCallback(async (email: string, password: string) => {
    setState(prev => ({ ...prev, isLoading: true, error: null }));
    try {
      const { user } = await authSignIn(email, password);
      setState({ user, isAuthenticated: true, isLoading: false, error: null });
      router.push("/dashboard"); 
    } catch (error) {
      const message = error instanceof Error ? error.message : "Sign in failed";
      setState(prev => ({ ...prev, isLoading: false, error: message }));
      throw error;
    }
  }, [router]);

  const signUp = useCallback(async (firstName: string, lastName: string, email: string, password: string) => {
    setState(prev => ({ ...prev, isLoading: true, error: null }));
    try {
      const { user } = await authSignUp(firstName, lastName, email, password);
      setState({ user, isAuthenticated: true, isLoading: false, error: null });
      router.push("/dashboard");
    } catch (error) {
      const message = error instanceof Error ? error.message : "Sign up failed";
      setState(prev => ({ ...prev, isLoading: false, error: message }));
      throw error;
    }
  }, [router]);

  const signOut = useCallback(() => {
    authSignOut();
    setState({ user: null, isAuthenticated: false, isLoading: false, error: null });

    window.location.href = "/auth/signin";
  }, []);

  const clearError = useCallback(() => setState(prev => ({ ...prev, error: null })), []);

  return (
    <AuthContext.Provider value={{ ...state, signIn, signUp, signOut, clearError }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth(): AuthContextType {
  const context = useContext(AuthContext);
  if (!context) throw new Error("useAuth must be used within an AuthProvider");
  return context;
}

// Page guard
export function useRequireAuth(): AuthState & { isReady: boolean } {
  const { user, isAuthenticated, isLoading, error } = useAuth();
  const router = useRouter();

  useEffect(() => {
    if (!isLoading && !isAuthenticated) router.push("/auth/signin");
  }, [isLoading, isAuthenticated, router]);

  return { user, isAuthenticated, isLoading, error, isReady: !isLoading && isAuthenticated };
}

export function useRedirectIfAuthenticated(): void {
  const { isAuthenticated, isLoading } = useAuth();
  const router = useRouter();

  useEffect(() => {
    if (!isLoading && isAuthenticated) router.push("/dashboard");
  }, [isLoading, isAuthenticated, router]);
}
