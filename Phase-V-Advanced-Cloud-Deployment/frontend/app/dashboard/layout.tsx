"use client";

import { ReactNode } from "react";
import { AuthGuard } from "@/components/auth/AuthGuard";

interface DashboardLayoutProps {
  children: ReactNode;
}

export default function DashboardLayout({ children }: DashboardLayoutProps) {
  return (
    <AuthGuard>
      <div className="min-h-screen bg-zinc-50 dark:bg-zinc-950">
        <div className="px-4 sm:px-6 lg:px-8 py-8">
          {children}
        </div>
      </div>
    </AuthGuard>
  );
}
