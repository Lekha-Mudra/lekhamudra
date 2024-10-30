'use client';

import { Clock, File, MoreVertical, Star } from "lucide-react";
import { Button } from "@/app/ui/button";
import {
  Card,
  CardContent,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/app/ui/card";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from "@/app/dashboard/components/dropdown-menu";
import { Input } from "@/app/ui/input";

const documents = [
  {
    id: 1,
    title: "Project Proposal",
    lastModified: "2 hours ago",
    starred: true,
  },
  {
    id: 2,
    title: "Meeting Notes",
    lastModified: "Yesterday",
    starred: false,
  },
  {
    id: 3,
    title: "Research Paper",
    lastModified: "3 days ago",
    starred: true,
  },
  {
    id: 4,
    title: "Product Roadmap",
    lastModified: "1 week ago",
    starred: false,
  },
];

export function DocumentList() {
  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h2 className="text-xl font-semibold md:text-2xl">Recent Documents</h2>
        <div className="flex md:hidden">
          <Input
            type="search"
            placeholder="Search..."
            className="w-[150px] sm:w-[200px]"
          />
        </div>
      </div>
      <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
        {documents.map((doc) => (
          <Card key={doc.id} className="group hover:border-primary/50 transition-colors">
            <CardHeader className="flex flex-row items-start justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium line-clamp-2">
                {doc.title}
              </CardTitle>
              <div className="flex items-center space-x-1">
                <Button
                  variant="ghost"
                  size="sm"
                  className="h-8 w-8 text-muted-foreground hover:text-primary"
                >
                  <Star
                    className={`h-4 w-4 ${
                      doc.starred ? "fill-primary text-primary" : ""
                    }`}
                  />
                </Button>
                <DropdownMenu>
                  <DropdownMenuTrigger asChild>
                    <Button
                      variant="ghost"
                      size="sm"
                      className="h-8 w-8 text-muted-foreground hover:text-primary"
                    >
                      <MoreVertical className="h-4 w-4" />
                    </Button>
                  </DropdownMenuTrigger>
                  <DropdownMenuContent align="end">
                    <DropdownMenuItem>Open</DropdownMenuItem>
                    <DropdownMenuItem>Share</DropdownMenuItem>
                    <DropdownMenuItem>Duplicate</DropdownMenuItem>
                    <DropdownMenuItem className="text-destructive">
                      Delete
                    </DropdownMenuItem>
                  </DropdownMenuContent>
                </DropdownMenu>
              </div>
            </CardHeader>
            <CardContent>
              <div className="aspect-[3/2] rounded-md border border-dashed flex items-center justify-center">
                <File className="h-8 w-8 text-muted-foreground" />
              </div>
            </CardContent>
            <CardFooter>
              <div className="flex items-center text-sm text-muted-foreground">
                <Clock className="mr-1 h-3 w-3" />
                {doc.lastModified}
              </div>
            </CardFooter>
          </Card>
        ))}
      </div>
    </div>
  );
}