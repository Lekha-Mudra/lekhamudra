// 'use client';

// import { Button } from "@/app/ui/button";
// import { cn } from "@/app/lib/utils";
// import {
//   FileText,
//   Star,
//   Clock,
//   Trash,
//   ChevronLeft,
//   Menu,
// } from "lucide-react";
// import { useState } from "react";

// const sidebarItems = [
//   { icon: FileText, label: "All Documents", count: 24 },
//   { icon: Star, label: "Starred", count: 8 },
//   { icon: Clock, label: "Recent", count: 12 },
//   { icon: Trash, label: "Trash", count: 3 },
// ];

// export function Sidebar() {
//   const [collapsed, setCollapsed] = useState(false);
//   const [isOpen, setIsOpen] = useState(false);

//   return (
//     <>
//       <div
//         className={cn(
//           "fixed inset-0 z-50 bg-background/80 backdrop-blur-sm data-[state=open]:animate-in data-[state=closed]:animate-out data-[state=closed]:fade-out-0 data-[state=open]:fade-in-0 md:hidden",
//           isOpen ? "block" : "hidden"
//         )}
//         onClick={() => setIsOpen(false)}
//       />
//       <div
//         className={cn(
//           "fixed inset-y-0 left-0 z-50 w-[240px] border-r bg-background transition-transform duration-300 ease-in-out md:sticky md:top-14 md:block md:h-[calc(100vh-3.5rem)]",
//           collapsed ? "md:w-[60px]" : "md:w-[240px]",
//           isOpen ? "translate-x-0" : "-translate-x-full md:translate-x-0"
//         )}
//       >
//         <div className="flex h-full flex-col">
//           <div className="flex items-center justify-end p-2">
//             <Button
//               variant="ghost"
//               size="sm"
//               onClick={() => setCollapsed(!collapsed)}
//               className="h-10 w-10 md:block hidden"
//             >
//               {collapsed ? (
//                 <Menu className="h-4 w-4" />
//               ) : (
//                 <ChevronLeft className="h-4 w-4" />
//               )}
//             </Button>
//           </div>
//           <nav className="space-y-1 px-2">
//             {sidebarItems.map((item) => (
//               <Button
//                 key={item.label}
//                 variant="ghost"
//                 className={cn(
//                   "w-full justify-start",
//                   collapsed ? "px-2" : "px-4"
//                 )}
//                 onClick={() => setIsOpen(false)}
//               >
//                 <item.icon className="h-4 w-4 shrink-0" />
//                 {!collapsed && (
//                   <>
//                     <span className="ml-3 flex-1 text-left truncate">
//                       {item.label}
//                     </span>
//                     <span className="ml-auto text-sm text-muted-foreground">
//                       {item.count}
//                     </span>
//                   </>
//                 )}
//               </Button>
//             ))}
//           </nav>
//         </div>
//       </div>
//     </>
//   );
// }

'use client';

import { Button } from "@/app/ui/button";
import { cn } from "@/app/lib/utils";
import { FileText, Star, Clock, Trash, ChevronLeft, Menu } from "lucide-react";
import { useState } from "react";

const sidebarItems = [
  { icon: FileText, label: "All Documents", count: 24 },
  { icon: Star, label: "Starred", count: 8 },
  { icon: Clock, label: "Recent", count: 12 },
  { icon: Trash, label: "Trash", count: 3 },
];

export function Sidebar() {
  const [collapsed, setCollapsed] = useState(false);
  const [isOpen, setIsOpen] = useState(false);

  return (
    <>
      {/* Overlay for mobile sidebar when open */}
      <div
        className={cn(
          "fixed inset-0 z-50 bg-background/80 backdrop-blur-sm md:hidden",
          isOpen ? "block" : "hidden"
        )}
        onClick={() => setIsOpen(false)}
      />

      {/* Sidebar content */}
      <div
        className={cn(
          "fixed inset-y-0 left-0 z-50 w-[240px] border-r bg-background transition-transform duration-300 ease-in-out md:sticky md:top-14 md:block md:h-[calc(100vh-3.5rem)]",
          collapsed ? "md:w-[60px]" : "md:w-[240px]",
          isOpen ? "translate-x-0" : "-translate-x-full md:translate-x-0"
        )}
      >
        <div className="flex h-full flex-col">
          <div className="flex items-center justify-end p-2">
            <Button
              variant="ghost"
              size="sm"
              onClick={() => setCollapsed(!collapsed)}
              className="h-10 w-10 md:block hidden"
            >
              {collapsed ? (
                <Menu className="h-4 w-4" />
              ) : (
                <ChevronLeft className="h-4 w-4" />
              )}
            </Button>
          </div>
          <nav className="space-y-1 px-2">
            {sidebarItems.map((item) => (
              <Button
                key={item.label}
                variant="ghost"
                className={cn(
                  "w-full justify-start",
                  collapsed ? "px-2" : "px-4"
                )}
                onClick={() => setIsOpen(false)}
              >
                <item.icon className="h-4 w-4 shrink-0" />
                {!collapsed && (
                  <>
                    <span className="ml-3 flex-1 text-left truncate">
                      {item.label}
                    </span>
                    <span className="ml-auto text-sm text-muted-foreground">
                      {item.count}
                    </span>
                  </>
                )}
              </Button>
            ))}
          </nav>
        </div>
      </div>

      {/* Mobile bottom navigation */}
      <div className="fixed bottom-0 left-0 z-50 w-full border-t bg-background p-2 md:hidden flex justify-around">
        {sidebarItems.map((item) => (
          <Button
            key={item.label}
            variant="ghost"
            size="sm"
            onClick={() => setIsOpen(!isOpen)}
            className="flex flex-col items-center"
          >
            <item.icon className="h-6 w-6" />
          </Button>
        ))}
      </div>
    </>
  );
}
