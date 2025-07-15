"use client";
import { Header } from "./components/header";
import { DocumentGrid } from "@/app/dashboard/components/document-grid";
import { Sidebar } from "@/app/dashboard/components/sidebar";
import { useEffect } from "react";
import { useRouter } from "next/navigation";

export default function Home() {
  const router = useRouter();
  useEffect(() => {
    const token = localStorage.getItem("token");
    if (!token) {
      router.push("/");
    }
  }, [router]);

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
