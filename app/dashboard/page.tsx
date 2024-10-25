import { Header } from "./components/header";
import { DocumentGrid } from "@/app/dashboard/components/document-grid";
// import { Sidebar } from "@/components/sidebar";

export default function Home() {
  return (
    <div className="min-h-screen bg-background">
      <Header />

      <main className="flex-1 p-6">
          <DocumentGrid />
        </main>
    </div>
  );
}