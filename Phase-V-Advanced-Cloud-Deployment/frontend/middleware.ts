import { NextResponse } from "next/server";
import type { NextRequest } from "next/server";

const protectedPaths = ["/dashboard"];
const authPaths = ["/signin", "/signup"];

export function middleware(request: NextRequest) {
  const { pathname } = request.nextUrl;
  const token = request.cookies.get("auth_token")?.value;

  const isProtected = protectedPaths.some(
    (path) => pathname === path || pathname.startsWith(path + "/")
  );

  const isAuthRoute = authPaths.some(
    (path) => pathname === path || pathname.startsWith(path + "/")
  );

  // 🚫 Not logged in → protect dashboard
  if (isProtected && !token) {
    return NextResponse.redirect(new URL("/signin", request.url));
  }

  // ✅ Logged in → block signin/signup (SAFE)
  if (isAuthRoute && token && pathname !== "/signin") {
    return NextResponse.redirect(new URL("/dashboard", request.url));
  }

  return NextResponse.next();
}

export const config = {
  matcher: [
    "/((?!_next/static|_next/image|favicon.ico|.*\\.(?:svg|png|jpg|jpeg|gif|webp)$).*)",
  ],
};
