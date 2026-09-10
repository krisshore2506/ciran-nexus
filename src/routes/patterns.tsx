import { createFileRoute } from "@tanstack/react-router";
import { useQuery } from "@tanstack/react-query";
import { AppShell } from "@/components/ciran/app-shell";
import { PageHeader, Panel, SeverityBadge, ActionButton } from "@/components/ciran/ui-kit";

export const Route = createFileRoute("/patterns")({
  head: () => ({ meta: [{ title: "Pattern Detection — CIRAN" }] }),
  component: PatternsPage,
});

function PatternsPage() {
  const { data: patterns, isLoading } = useQuery({
    queryKey: ["patterns"],
    queryFn: async () => {
      const res = await fetch(`/api/patterns`);
      return res.json();
    },
  });

  return (
    <AppShell>
      <PageHeader
        title="Pattern Detection"
        subtitle="Hidden structural and temporal anomalies detected in the intelligence graph."
      />
      {isLoading ? (
        <div className="py-20 text-center text-muted-foreground">Loading patterns...</div>
      ) : (
        <div className="grid gap-6 xl:grid-cols-2">
          {patterns?.map((p: any) => (
            <Panel key={p.id} title={p.category} bodyClassName="p-5">
              <div className="flex items-start justify-between gap-4 mb-5">
                <div>
                  <h3 className="text-sm font-semibold text-foreground mb-1">{p.title}</h3>
                </div>
                <div className="shrink-0 text-right flex flex-col items-end gap-1">
                  <SeverityBadge severity="high">Investigation Signal</SeverityBadge>
                  <span className="font-mono text-[10px] text-muted-foreground bg-surface-2 px-1.5 py-0.5 rounded border border-border">
                    Confidence {p.confidence}%
                  </span>
                </div>
              </div>

              <div className="mb-4">
                <p className="text-[10px] font-semibold uppercase tracking-wider text-muted-foreground mb-1">
                  Why flagged
                </p>
                <p className="text-sm text-foreground">{p.why}</p>
              </div>

              <div className="mb-4">
                <p className="text-[10px] font-semibold uppercase tracking-wider text-muted-foreground mb-2">
                  Connected Entities
                </p>
                <div className="flex flex-wrap gap-2">
                  {p.entities.map((e: string, i: number) => (
                    <span
                      key={i}
                      className="px-2 py-1 bg-surface-2 border border-border-strong rounded text-xs text-foreground font-mono"
                    >
                      {e}
                    </span>
                  ))}
                </div>
              </div>

              {p.path && (
                <div className="mb-6 bg-surface p-4 rounded border border-border/50">
                  <p className="text-[10px] font-semibold uppercase tracking-wider text-muted-foreground mb-3">
                    Detection Path
                  </p>
                  <div className="flex flex-wrap items-center gap-2">
                    {p.path.map((node: string, j: number) => (
                      <div
                        key={j}
                        className="flex items-center gap-2 text-[11px] font-mono text-muted-foreground"
                      >
                        <span className="bg-background px-1.5 py-0.5 rounded border border-border">
                          {node}
                        </span>
                        {j < p.path.length - 1 && <span className="text-border-strong">→</span>}
                      </div>
                    ))}
                  </div>
                </div>
              )}

              <div className="flex items-center justify-between border-t border-border/50 pt-4 mt-auto">
                <div>
                  <p className="text-[10px] font-semibold uppercase tracking-wider text-muted-foreground mb-1.5">
                    Evidence
                  </p>
                  <div className="flex gap-2">
                    {p.evidence.map((ev: string, j: number) => (
                      <span
                        key={j}
                        className="px-1.5 py-0.5 rounded border border-border bg-background font-mono text-[10px] text-muted-foreground"
                      >
                        {ev}
                      </span>
                    ))}
                  </div>
                </div>
                <div className="flex flex-col items-end gap-1.5">
                  <ActionButton variant="primary">Review connection</ActionButton>
                  <span className="text-[9px] text-muted-foreground uppercase tracking-wider">
                    Requires analyst review
                  </span>
                </div>
              </div>
            </Panel>
          ))}
        </div>
      )}
    </AppShell>
  );
}
