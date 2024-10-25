import { DocumentCard } from "@/app/dashboard/components/document-card";

const documents = [
  {
    id: 1,
    title: "Q1 Project Proposal",
    lastModified: "2 hours ago",
    starred: true,
    type: "document",
  },
  {
    id: 2,
    title: "Team Meeting Notes",
    lastModified: "Yesterday",
    starred: false,
    type: "document",
  },
  {
    id: 3,
    title: "Research Findings",
    lastModified: "3 days ago",
    starred: true,
    type: "document",
  },
  {
    id: 4,
    title: "2024 Product Roadmap",
    lastModified: "1 week ago",
    starred: false,
    type: "spreadsheet",
  },
  {
    id: 5,
    title: "Marketing Strategy",
    lastModified: "2 weeks ago",
    starred: true,
    type: "presentation",
  },
  {
    id: 6,
    title: "Budget Analysis",
    lastModified: "3 weeks ago",
    starred: false,
    type: "spreadsheet",
  },
];

export function DocumentGrid() {
  return (
    <div>
      <h2 className="text-2xl font-semibold mb-6">Recent Documents</h2>
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
        {documents.map((doc) => (
          <DocumentCard key={doc.id} document={doc} />
        ))}
      </div>
    </div>
  );
}