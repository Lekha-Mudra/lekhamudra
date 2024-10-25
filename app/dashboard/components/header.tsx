import { FileText, Plus, Search } from "lucide-react";
import { Button } from "@/app/ui/button";
import { Input } from "@/app/ui/input";
import Image from "next/image";
// import { ModeToggle } from "@/app/mode-toggle";

export function Header() {
  return (
    <header className="sticky top-0 z-50 w-full border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
      <div className="container h-16 flex items-center justify-between gap-4">
        <div className="flex items-center gap-4 lg:gap-6">
          <div className="flex items-center gap-2">
          <Image src="/logo-sm.png" width={1024} height={1024} alt="logo" className="h-6 w-6" />
            
            <span className="hidden font-semibold sm:inline-block">
              LekhaMudra
            </span>
          </div>
          <div className="hidden md:flex">
            <div className="relative w-60 lg:w-80">
              <Search className="absolute left-2 top-2.5 h-4 w-4 text-muted-foreground" />
              <Input placeholder="Search..." className="pl-8" />
            </div>
          </div>
        </div>

        <div className="flex items-center gap-4">
          <Button className="hidden sm:flex">
            <Plus className="h-4 w-4 mr-2" />
            New Document
          </Button>
          <Button size="lg" className="sm:hidden">
            <Plus className="h-4 w-4" />
          </Button>
          {/* <ModeToggle /> */}
        </div>
      </div>
    </header>
  );
}