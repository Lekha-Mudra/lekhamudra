import { Clock, FileText, MoreVertical, Star } from "lucide-react";
import { Button } from "@/app/ui/button";
import {
  Card,
  CardContent,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/app/dashboard/components/card";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from "@/app/dashboard/components/dropdown-menu";

interface Document {
  id: number;
  title: string;
  lastModified: string;
  starred: boolean;
  type: string;
}

interface DocumentCardProps {
  document: Document;
}

export function DocumentCard({ document }: DocumentCardProps) {
  return (
    <Card className="group hover:border-primary/50 transition-colors">
      <CardHeader className="flex flex-row items-start justify-between space-y-0 pb-2">
        <CardTitle className="text-sm font-medium line-clamp-2">
          {document.title}
        </CardTitle>
        <div className="flex items-center space-x-1">
          <Button
            variant="ghost"
            size="lg"
            className="h-8 w-8 text-muted-foreground hover:text-primary"
          >
            <Star
              className={`h-4 w-4 ${
                document.starred ? "fill-primary text-primary" : ""
              }`}
            />
          </Button>
          <DropdownMenu>
            <DropdownMenuTrigger asChild>
              <Button
                variant="ghost"
                size="lg"
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
        <div className="rounded-md border border-dashed p-8 flex items-center justify-center">
          <FileText className="h-8 w-8 text-muted-foreground" />
        </div>
      </CardContent>
      <CardFooter>
        <div className="flex items-center text-sm text-muted-foreground">
          <Clock className="mr-1 h-3 w-3" />
          {document.lastModified}
        </div>
      </CardFooter>
    </Card>
  );
}