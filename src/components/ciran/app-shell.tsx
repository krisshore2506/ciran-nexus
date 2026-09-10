import { Link, useRouterState } from "@tanstack/react-router";
import { useState, type ReactNode } from "react";
import {
  Bell,
  Bot,
  FileSearch,
  GitCompareArrows,
  LayoutDashboard,
  Menu,
  Radar,
  Search,
  Settings,
  ShieldCheck,
  Share2,
  Clock,
  Users,
} from "lucide-react";
import { cn } from "@/lib/utils";
import { useNavigate } from "@tanstack/react-router";

const nav = [
  { to: "/dashboard", label: "Dashboard", icon: LayoutDashboard },
  { to: "/investigations", label: "Investigations", icon: Search },
  { to: "/network", label: "Network Intelligence", icon: Share2 },
  { to: "/entity-resolution", label: "Entity Resolution", icon: Users },
  { to: "/cross-case", label: "Cross-Case Analysis", icon: GitCompareArrows },
  { to: "/timeline", label: "Timeline", icon: Clock },
  { to: "/patterns", label: "Pattern Detection", icon: Radar },
  { to: "/alerts", label: "Intelligence Alerts", icon: Bell },
  { to: "/copilot", label: "Investigator Copilot", icon: Bot },
  { to: "/evidence", label: "Evidence & Audit", icon: FileSearch },
  { to: "/settings", label: "Settings", icon: Settings },
] as const;

export function AppShell({ children }: { children: ReactNode }) {
  const pathname = useRouterState({ select: (s) => s.location.pathname });
  const [open, setOpen] = useState(false);
  const navigate = useNavigate();
  const [searchQuery, setSearchQuery] = useState("");

  const handleSearch = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === "Enter" && searchQuery.trim().toLowerCase().includes("ravi")) {
      navigate({ to: "/entity/$id", params: { id: "P-RAVI" } });
      setSearchQuery("");
    }
  };

  return (
    <div className="min-h-screen bg-background lg:grid lg:grid-cols-[260px_1fr]">
      <aside
        className={cn(
          "fixed inset-y-0 left-0 z-40 flex w-[260px] flex-col border-r border-border bg-background transition-transform lg:static lg:translate-x-0",
          open ? "translate-x-0" : "-translate-x-full",
        )}
      >
        <div className="flex items-center gap-3 border-b border-border px-4 py-4">
          <div className="flex size-9 items-center justify-center rounded-md border border-primary/40 bg-primary/10">
            <ShieldCheck className="size-5 text-primary" />
          </div>
          <div>
            <p className="text-sm font-semibold tracking-[0.2em] text-foreground">CIRAN</p>
            <p className="text-[10px] leading-tight text-muted-foreground">
              Criminal Intelligence &amp; Relationship Analysis Network
            </p>
          </div>
        </div>

        <nav className="flex-1 space-y-0.5 overflow-y-auto p-2">
          {nav.map((item) => {
            const active = pathname === item.to;
            const Icon = item.icon;
            return (
              <Link
                key={item.to}
                to={item.to}
                onClick={() => setOpen(false)}
                className={cn(
                  "flex items-center gap-3 rounded-md px-3 py-2 text-sm transition-colors",
                  active
                    ? "bg-primary/10 text-primary border-l-2 border-primary rounded-l-none"
                    : "text-muted-foreground hover:bg-surface hover:text-foreground",
                )}
              >
                <Icon className={cn("size-4", active && "text-primary")} />
                {item.label}
              </Link>
            );
          })}
        </nav>

        <div className="border-t border-border px-4 py-3">
          <p className="text-[10px] leading-relaxed text-muted-foreground">
            Intelligence layer over connected CCTNS / ICJS records. CIRAN does not replace source
            systems.
          </p>
        </div>
      </aside>

      {open && (
        <div
          className="fixed inset-0 z-30 bg-background/70 lg:hidden"
          onClick={() => setOpen(false)}
        />
      )}

      <div className="flex min-h-screen flex-col">
        <header className="sticky top-0 z-20 flex items-center gap-3 border-b border-border bg-surface/95 px-4 py-3 backdrop-blur">
          <button
            className="rounded-md p-2 text-muted-foreground hover:bg-surface-2 lg:hidden"
            onClick={() => setOpen(true)}
            aria-label="Open navigation"
          >
            <Menu className="size-4" />
          </button>

          <div className="relative hidden max-w-md flex-1 md:block group">
            <Search className="absolute top-1/2 left-3 size-4 -translate-y-1/2 text-muted-foreground group-focus-within:text-primary transition-colors" />
            <input
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              onKeyDown={handleSearch}
              placeholder="Global search — person, phone, vehicle, case, location"
              className="w-full rounded-md border border-transparent bg-surface py-2 pr-3 pl-9 text-sm text-foreground placeholder:text-muted-foreground focus:border-border-strong focus:bg-input transition-all focus:outline-none"
            />
          </div>

          <div className="ml-auto flex items-center gap-3">
            <Link
              to="/investigations"
              className="hidden items-center gap-2 rounded-md border border-border bg-surface-2 px-3 py-1.5 text-xs sm:flex"
            >
              <span className="size-1.5 rounded-full bg-success" />
              <span className="text-muted-foreground">Active investigation</span>
              <span className="font-mono font-semibold text-foreground">CASE-203</span>
            </Link>

            <Link
              to="/alerts"
              className="relative rounded-md p-2 text-muted-foreground hover:bg-surface-2 hover:text-foreground"
              aria-label="Notifications"
            >
              <Bell className="size-4" />
              <span className="absolute top-1.5 right-1.5 size-2 rounded-full bg-critical" />
            </Link>

            <div className="flex items-center gap-2 border-l border-border pl-3 opacity-80 hover:opacity-100 transition-opacity">
              <div className="flex size-7 items-center justify-center rounded-full border border-border bg-surface-2 text-[10px] font-semibold text-muted-foreground">
                SM
              </div>
              <div className="hidden leading-tight sm:block">
                <p className="text-[11px] font-medium text-muted-foreground">Insp. S. Menon</p>
                <p className="text-[9px] tracking-wider text-muted-foreground/70 uppercase">
                  Senior Investigator
                </p>
              </div>
            </div>
          </div>
        </header>

        <main className="flex-1 space-y-5 p-4 lg:p-6">{children}</main>
      </div>
    </div>
  );
}
