// import type { Metadata } from "next";
// import localFont from "next/font/local";
// import "./globals.css";
// import { Inter } from 'next/font/google'

// const inter = Inter({ subsets: ['latin'] })
// const geistSans = localFont({
//   src: "./fonts/GeistVF.woff",
//   variable: "--font-geist-sans",
//   weight: "100 900",
// });
// const geistMono = localFont({
//   src: "./fonts/GeistMonoVF.woff",
//   variable: "--font-geist-mono",
//   weight: "100 900",
// });

// export const metadata: Metadata = {
//   title: "LekhaMudra",
//   description: "your document intelligence platform",
// };

// export default function RootLayout({
//   children,
// }: Readonly<{
//   children: React.ReactNode;
// }>) {
//   return (
//     <html lang="en">
//       <body
//         className={`${inter.className} antialiased`}
//       >
//         {children}
//       </body>
//     </html>
//   );
// }

import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";
// import { ThemeProvider } from "@/app/theme-provide";
// import { Toaster } from "@/components/ui/sonner";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "Document Sharing Platform",
  description: "A modern document sharing platform built with Next.js",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body className={inter.className}>

          {children}
          {/* <Toaster /> */}
      </body>
    </html>
  );
}
