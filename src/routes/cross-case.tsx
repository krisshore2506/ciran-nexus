import { createFileRoute } from "@tanstack/react-router";
import { useQuery } from "@tanstack/react-query";
import { AppShell } from "@/components/ciran/app-shell";
import { PageHeader, Panel, SeverityBadge, ActionButton } from "@/components/ciran/ui-kit";
import { Link } from "@tanstack/react-router";
import { Link as LinkIcon } from "lucide-react";
import { getCrossCaseLinks } from "@/lib/ciran-service";
import { QueryLoader } from "@/components/ciran/query-loader";

export const Route = createFileRoute("/cross-case")({
  head: () => ({
    meta: [{ title: "Cross-Case Intelligence — CIRAN" }],
  }),
  component: CrossCasePage,
});

function CrossCasePage() {
  const query = useQuery({
    queryKey: ["cross-case-links"],
    queryFn: getCrossCaseLinks,
  });

  return (
    <AppShell>
      <PageHeader
        title="Cross-Case Intelligence"
        subtitle="Shared entities and overlapping patterns detected between independent case records."
      />

      <QueryLoader
        isLoading={query.isLoading}
        error={query.error}
        data={query.data}
        emptyMessage="No intelligence data available."
      >
        {(links) => (
          <div className="grid gap-6">
            {links.map((link: any, i: number) => (
              <Panel key={i} title={`Connected: ${link.cases.join(" · ")}`} bodyClassName="p-4">
                <div className="grid gap-6 md:grid-cols-2">
                  <div className="flex flex-col">
                    <div className="flex items-center gap-2 mb-4">
                      <SeverityBadge severity="high">Potential Cross-Case Relationship</SeverityBadge>
                      <span className="font-mono text-[10px] text-muted-foreground bg-surface-2 px-1.5 py-0.5 rounded border border-border">
                        Confidence {link.confidence}%
                      </span>
                    </div>

                    <div className="mb-6 border border-border rounded-lg p-4 bg-surface/50">
                      <p className="text-[10px] font-semibold uppercase tracking-wider text-muted-foreground mb-2">
                        Why was this flagged?
                      </p>
                      <p className="text-sm text-foreground">{link.summary}</p>
                    </div>

                    <div className="mb-6">
                      <p className="text-[10px] font-semibold uppercase tracking-wider text-muted-foreground mb-3">
                        Shared Attributes
                      </p>
                      <ul className="space-y-2">
                        {link.shared.map((s: any, j: number) => (
                          <li key={j} className="text-sm text-foreground flex items-center gap-3">
                            <span className="w-1.5 h-1.5 rounded-full bg-primary/50" />
                            <span className="text-muted-foreground min-w-[80px]">{s.type}:</span>
                            <span className="font-mono">{s.value}</span>
                          </li>
                        ))}
                      </ul>
                    </div>

                    <div className="mt-auto flex gap-2 pt-4">
                      <Link to="/network">
                        <ActionButton variant="primary">Review in Network</ActionButton>
                      </Link>
                    </div>
                  </div>

                  <div className="rounded-md border border-border bg-surface-2 p-5 relative overflow-hidden">
                    <div className="absolute top-4 right-4 text-muted-foreground/20">
                      <LinkIcon className="size-24" />
                    </div>
                    <h4 className="text-[10px] font-semibold uppercase tracking-wider text-muted-foreground mb-4">
                      Relationship Path
                    </h4>
                    <div className="space-y-1 relative z-10">
                      {link.path.map((node: string, j: number) => (
                        <div key={j} className="flex flex-col">
                          <div className="flex items-center gap-2">
                            <span className="px-2.5 py-1.5 bg-background text-[11px] font-mono rounded border border-border-strong text-foreground shadow-sm">
                              {node}
                            </span>
                          </div>
                          {j < link.path.length - 1 && (
                            <div className="w-px h-3 bg-border ml-5 my-1" />
                          )}
                        </div>
                      ))}
                    </div>
                  </div>
                </div>
              </Panel>
            ))}
          </div>
        )}
      </QueryLoader>
    </AppShell>
  );
}
