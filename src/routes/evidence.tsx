import { createFileRoute } from "@tanstack/react-router";
import { useQuery } from "@tanstack/react-query";
import { AppShell } from "@/components/ciran/app-shell";
import { PageHeader, Panel, SeverityBadge } from "@/components/ciran/ui-kit";

export const Route = createFileRoute("/evidence")({
  head: () => ({
    meta: [{ title: "Evidence & Audit — CIRAN" }],
  }),
  component: EvidencePage,
});

function EvidencePage() {
  const { data: evidenceList, isLoading } = useQuery({
    queryKey: ["evidence-list"],
    queryFn: async () => {
      // For the prototype we mock the list fetch directly since there's no list API in the prompt,
      // but we have getEvidence() in the service.
      const res = await import("@/lib/ciran-service");
      return res.getEvidence();
    },
  });

  return (
    <AppShell>
      <PageHeader
        title="Evidence & Audit Trail"
        subtitle="Traceability and accountability for all intelligence signals."
      />

      {isLoading ? (
        <div className="py-20 text-center text-muted-foreground">Loading evidence records...</div>
      ) : (
        <div className="grid gap-6">
          {evidenceList?.map((item: any) => (
            <Panel key={item.id} title={item.insight} bodyClassName="p-0">
              <div className="px-5 py-3 border-b border-border/50 bg-surface/30 flex items-center justify-between">
                <div className="flex items-center gap-4">
                  <span className="text-[11px] font-mono text-muted-foreground">{item.id}</span>
                  <SeverityBadge severity={item.status === "Accepted" ? "info" : "medium"}>
                    {item.status}
                  </SeverityBadge>
                </div>
                <span className="text-[11px] font-medium text-muted-foreground">
                  {item.relationship}
                </span>
              </div>

              <div className="p-0 grid md:grid-cols-2 divide-y md:divide-y-0 md:divide-x divide-border/50">
                <div className="p-5">
                  <h4 className="text-[10px] font-semibold uppercase tracking-wider text-muted-foreground mb-4">
                    Supporting Source Records
                  </h4>
                  <ul className="space-y-2">
                    {item.sources.map((src: any, i: number) => (
                      <li
                        key={i}
                        className="flex flex-col gap-1 rounded bg-surface border border-border-strong p-2.5 hover:border-primary/50 transition-colors"
                      >
                        <div className="flex justify-between items-center">
                          <span className="font-mono text-[11px] text-foreground">{src.id}</span>
                          <span className="text-[10px] font-mono text-muted-foreground">
                            {src.timestamp}
                          </span>
                        </div>
                        <span className="text-[10px] text-muted-foreground/80">{src.type}</span>
                      </li>
                    ))}
                  </ul>
                </div>

                <div className="p-5">
                  <h4 className="text-[10px] font-semibold uppercase tracking-wider text-muted-foreground mb-4">
                    Analyst Audit History
                  </h4>
                  <div className="relative ml-2 space-y-4 border-l border-border pl-4 py-1">
                    {item.audit.map((entry: any, i: number) => (
                      <div key={i} className="relative">
                        <div className="absolute -left-[21px] top-1 h-2 w-2 rounded-full bg-border ring-4 ring-surface" />
                        <div className="flex justify-between items-start mb-0.5">
                          <p className="text-[11px] font-medium text-foreground">{entry.stage}</p>
                          <span className="text-[10px] font-mono text-muted-foreground">
                            {entry.timestamp}
                          </span>
                        </div>
                        <p className="text-[10px] text-muted-foreground">By: {entry.actor}</p>
                        {entry.note && (
                          <p className="text-[11px] mt-2 bg-surface/50 p-2.5 rounded text-foreground border border-border/50 italic">
                            "{entry.note}"
                          </p>
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
    </AppShell>
  );
}
