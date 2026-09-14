import { createFileRoute, Link } from "@tanstack/react-router";
import { useQuery } from "@tanstack/react-query";
import { AppShell } from "@/components/ciran/app-shell";
import { PageHeader, Panel, SeverityBadge, ActionButton } from "@/components/ciran/ui-kit";

export const Route = createFileRoute("/alerts")({
  head: () => ({ meta: [{ title: "Intelligence Alerts — CIRAN" }] }),
  component: AlertsPage,
});

function AlertsPage() {
  const { data: alerts, isLoading } = useQuery({
    queryKey: ["alerts"],
    queryFn: async () => {
      const res = await fetch(`/api/alerts`);
      return res.json();
    },
  });

  return (
    <AppShell>
      <PageHeader
        title="Intelligence Alerts"
        subtitle="Prioritised automated alerts requiring analyst review."
      />
      {isLoading ? (
        <div className="py-20 text-center text-muted-foreground">Loading alerts...</div>
      ) : (
        <div className="grid gap-4">
          {alerts?.map((a: unknown) => (
            <div
              key={a.id}
              className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 p-4 border border-border bg-surface rounded-lg hover:border-primary/50 transition-colors"
            >
              <div>
                <div className="flex flex-wrap items-center gap-2 mb-2">
                  <SeverityBadge severity={a.severity} />
                  <span className="font-mono text-xs font-semibold text-primary">{a.case}</span>
                  <span className="text-xs text-muted-foreground">{a.timestamp}</span>
                </div>
                <p className="text-sm font-semibold text-foreground mb-1">{a.title}</p>
                <p className="text-sm text-muted-foreground max-w-3xl">{a.explanation}</p>
                <div className="flex items-center gap-2 mt-3">
                  <span className="text-[10px] font-semibold uppercase tracking-wider text-muted-foreground">
                    Entities:
                  </span>
                  {a.entities.map((e: string, i: number) => (
                    <span
                      key={i}
                      className="px-1.5 py-0.5 border border-border bg-surface-2 rounded text-[10px] text-foreground font-mono"
                    >
                      {e}
                    </span>
                  ))}
                </div>
              </div>
              <div className="flex flex-col sm:items-end gap-2 shrink-0">
                <span className="text-xs font-mono text-muted-foreground">
                  Confidence: {a.confidence}%
                </span>
                <div className="flex gap-2">
                  <Link to={`/network`}>
                    <ActionButton variant="primary">Review</ActionButton>
                  </Link>
                  <ActionButton>Dismiss</ActionButton>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </AppShell>
  );
}
