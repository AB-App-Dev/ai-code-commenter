import type { Metadata } from "next"; // Importing the metadata type from next package
import { Geist, Geist_Mono } from "next/font/google"; // Importing fonts from google fonts API
import "./globals.css"; // Global stylesheet
import { Toaster } from "@/components/ui/sonner"; // Importing Toaster component for notifications

const geistSans = Geist({ // Configuring the Geist font and setting it as a variable in CSS
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({ // Configuring the Geist Mono font and setting it as a variable in CSS
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

// Setting metadata for the HTML document
export const metadata: Metadata = {
  title: "CodeNest",
  description: "Bookmark and code snippet manager for developers",
};

export default function RootLayout({ // Component that wraps around other components in the application
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    // HTML root element with lang set to English and class 'dark' for dark mode support
    <html lang="en" className="dark">
      {/* Body of the document, containing fonts classes */}
      <body
        className={`${geistSans.variable} ${geistMono.variable} antialiased`}
      >
        {children}  // Components nested inside this layout will appear in the body
        <Toaster />  // Toaster component for displaying notifications
      </body>
    </html>
  );
}