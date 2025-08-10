"use client";
import Image from "next/image";
import LoginPage from "./auth/page";
import { Button } from "@/app/ui/button";
import { Moon, Sun, FileText } from "lucide-react";
import { useState, useEffect } from "react";
import clsx from "clsx";
import { useRouter } from "next/navigation";

export default function Home() {
  const [isDarkMode, setIsDarkMode] = useState(false);
  const router = useRouter();

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
          if (data.authenticated && !cancelled) router.push("/dashboard");
        }
      } catch (_) {
        /* ignore */
      }
    })();
    return () => {
      cancelled = true;
    };
  }, [router]);

  const toggleTheme = () => {
    setIsDarkMode(!isDarkMode);
  };
  return (
    <>
      <div className={`h-screen w-screen ${isDarkMode ? "bg-black" : ""}`}>
        <div
          className={clsx("absolute top-4 right-4", {
            "hover: text-black": isDarkMode,
          })}
        >
          <Button variant="outline" size="sm" onClick={toggleTheme}>
            {isDarkMode ? (
              <Sun className="h-[1.2rem] w-[1.2rem] text-white hover:text-black" />
            ) : (
              <Moon className="h-[1.2rem] w-[1.2rem]" />
            )}
            <span className="sr-only">Toggle theme</span>
          </Button>
        </div>
        <LoginPage isDarkMode={isDarkMode} />
      </div>
    </>
  );
}
