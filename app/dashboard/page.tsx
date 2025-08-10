"use client";
import { Header } from "./components/header";
import { DocumentGrid } from "@/app/dashboard/components/document-grid";
import { Sidebar } from "@/app/dashboard/components/sidebar";
import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";

export default function Home() {
  const router = useRouter();
  const [loading, setLoading] = useState(true);
  useEffect(() => {
    let cancelled = false;
    (async () => {
      try {
        const API_BASE =
          process.env.NEXT_PUBLIC_API_BASE || "http://localhost:8000/api/v1";
        const res = await fetch(`${API_BASE}/auth/me`, {
          credentials: "include",
        });
        if (res.ok) {
          const data = await res.json();
          if (!data.authenticated && !cancelled) {
            router.push("/");
            return;
          }
        } else if (!cancelled) {
          router.push("/");
          return;
        }
      } catch (_) {
        if (!cancelled) router.push("/");
        return;
      } finally {
        if (!cancelled) setLoading(false);
      }
    })();
    return () => {
      cancelled = true;
    };
  }, [router]);

  if (loading)
    return <div className="p-8 text-sm text-muted-foreground">Loading...</div>;
  return (
    <div className="min-h-screen bg-background">
      <Header />
      <div className="flex">
        <Sidebar />
        <main className="flex-1 p-6">
          <DocumentGrid />
        </main>
      </div>
    </div>
  );
}
