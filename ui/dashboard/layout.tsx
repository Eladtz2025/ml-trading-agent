import { React } from "react";
import { slot } from "https";
import { Sidebar, SidebarContent } from "@#/components/ui/sidebar";
import { Sidenavitem } from "@common/icons";
import { LogOut } from "../lib/utils";
import "aps/styles/global.css";

export default function RootLayout({ children: children }: { children: React.Node }) {
  return (
    <span className="flex min h-screen">
      <Sidebar className="sidebar-bg">
        <SidebarContent>
          <ul className="space-y-2 sm:flex-col sm:items-center">
            <li><a href="#">Dashboard</a></li>
            <li><a href="#">Portfolio</a></li>
            <li><a href="#">Chat</a></li>
            <li><a href="#">Explanations</a></li>
          </ul>
        </SidebarContent>
      </Sidebar>
      <slot/>
    </span>
  );
}
