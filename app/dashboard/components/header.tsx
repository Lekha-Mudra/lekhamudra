'use client';

import { FileText, Plus, Search } from "lucide-react";
import { Button } from "@/app/ui/button";
import { Input } from "@/app/ui/input";
// import { ModeToggle } from "@/components/mode-toggle";
// import { SidebarTrigger } from "@/app/dashboard/components/sidebar";
import { Sidebar } from "./sidebar";

export function Header() {
  return (
    <header className="sticky top-0 z-50 w-full border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
                 
      <div className="container flex h-14 max-w-screen-2xl items-center justify-between gap-4 px-4">
        <div className="flex items-center gap-2 md:gap-4">
          <div className="flex items-center gap-2">

            <FileText className="h-5 w-5 md:h-6 md:w-6" />
            <span className="font-semibold">DocShare</span>
          </div>
          <div className="hidden md:flex">
            <div className="relative w-60 lg:w-80">
              <Search className="absolute left-2 top-2.5 h-4 w-4 text-muted-foreground" />
              <Input placeholder="Search documents..." className="pl-8" />
            </div>
          </div>
        </div>

        <div className="flex items-center gap-2 md:gap-4">
          <Button size="sm" className="hidden sm:flex">
            <Plus className="h-4 w-4 mr-2" />
            New Document
          </Button>
          <Button size="sm" className="h-8 w-8 sm:hidden">
            <Plus className="h-4 w-4" />
          </Button>
          <Button
            variant="ghost"
            size="sm"
            className="h-8 w-8 md:hidden"
            onClick={() => (document.querySelector('input[type="search"]') as HTMLInputElement)?.focus()}

          >
            <Search className="h-4 w-4" />
          </Button>
          {/* <ModeToggle /> */}
        </div>
      </div>
    </header>
  );
}