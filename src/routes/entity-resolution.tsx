import { createFileRoute } from "@tanstack/react-router";
import { useQuery } from "@tanstack/react-query";
import { AppShell } from "@/components/ciran/app-shell";
import { PageHeader, Panel, ActionButton, SeverityBadge } from "@/components/ciran/ui-kit";
import { QueryLoader } from "@/components/ciran/query-loader";
import { getEntityResolution } from "@/lib/ciran-service";

export const Route = createFileRoute("/entity-resolution")({
  component: EntityResolutionPage,
});

function EntityResolutionPage() {
  const query = useQuery({ queryKey: ["entity-resolution"], queryFn: getEntityResolution });

  return (
    <AppShell>
      <PageHeader
        title="Entity Resolution"
        subtitle="Identify and merge duplicate entity records across disparate source systems."
      />

      <div className="max-w-4xl space-y-6">
        <Panel title="Potential Entity Match Requires Review" bodyClassName="p-6">
          <QueryLoader isLoading={query.isLoading} error={query.error} data={query.data}>
            {(data) => (
              <>
                <div className="flex items-center gap-4 mb-6">
                  <SeverityBadge severity="high">Confidence: {data.confidence}%</SeverityBadge>
                  <p className="text-sm text-muted-foreground">
                    Detected high attribute overlap between two independent records.
                  </p>
                </div>

                <div className="grid md:grid-cols-2 gap-6 relative">
                  <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 z-10 hidden md:flex h-8 w-8 items-center justify-center rounded-full bg-surface-2 border border-border text-muted-foreground text-xs font-bold">
                    VS
                  </div>

                  <div className="rounded-md border border-border bg-surface-2 p-4">
                    <p className="text-xs font-semibold tracking-wider text-muted-foreground uppercase mb-4">
                      {data.recordA.title}
                    </p>
                    <p className="text-lg font-medium text-foreground mb-4">{data.recordA.name}</p>
                    <div className="space-y-2">
                      {data.recordA.fields.map((f: unknown, i: number) => (
                        <div key={i} className="flex justify-between text-sm">
                          <span className="text-muted-foreground">{f.label}</span>
                          <span className="font-mono text-foreground">{f.value}</span>
                        </div>
                      ))}
                    </div>
                  </div>

                  <div className="rounded-md border border-border bg-surface-2 p-4">
                    <p className="text-xs font-semibold tracking-wider text-muted-foreground uppercase mb-4">
                      {data.recordB.title}
                    </p>
                    <p className="text-lg font-medium text-foreground mb-4">{data.recordB.name}</p>
                    <div className="space-y-2">
                      {data.recordB.fields.map((f: unknown, i: number) => (
                        <div key={i} className="flex justify-between text-sm">
                          <span className="text-muted-foreground">{f.label}</span>
                          <span className="font-mono text-foreground">{f.value}</span>
                        </div>
                      ))}
                    </div>
                  </div>
                </div>

                <div className="mt-6 pt-6 border-t border-border grid md:grid-cols-2 gap-6">
                  <div>
                    <p className="text-xs font-semibold tracking-wider text-success uppercase mb-2">
                      Matching Factors
                    </p>
                    <ul className="space-y-1 text-sm text-foreground">
                      {data.matching.map((m: string, i: number) => (
                        <li key={i} className="flex items-center gap-2">
                          <span className="w-1.5 h-1.5 rounded-full bg-success" />
                          {m}
                        </li>
                      ))}
                    </ul>
                  </div>
                  <div>
                    <p className="text-xs font-semibold tracking-wider text-critical uppercase mb-2">
                      Discrepancies
                    </p>
                    <ul className="space-y-1 text-sm text-foreground">
                      {data.nonMatching.map((m: string, i: number) => (
                        <li key={i} className="flex items-center gap-2">
                          <span className="w-1.5 h-1.5 rounded-full bg-critical" />
                          {m}
                        </li>
                      ))}
                    </ul>
                  </div>
                </div>

                <div className="mt-8 flex flex-wrap gap-3">
                  <ActionButton variant="primary">Confirm Match & Merge</ActionButton>
                  <ActionButton>Reject Match</ActionButton>
                  <ActionButton>Flag for Supervisor</ActionButton>
                </div>
              </>
            )}
          </QueryLoader>
        </Panel>
      </div>
    </AppShell>
  );
}
