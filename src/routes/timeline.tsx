import { createFileRoute } from "@tanstack/react-router";
import { AppShell } from "@/components/ciran/app-shell";
import { PageHeader, Panel } from "@/components/ciran/ui-kit";
import { TimelineView } from "@/components/ciran/timeline-view";
import { useQuery } from "@tanstack/react-query";

export const Route = createFileRoute("/timeline")({
  head: () => ({ meta: [{ title: "Global Timeline — CIRAN" }] }),
  component: GlobalTimelinePage,
});

function GlobalTimelinePage() {
  // Let's use the entire timeline for the global view
  const { data: events, isLoading } = useQuery({
    queryKey: ["global-timeline"],
    queryFn: async () => {
      const res = await import("@/lib/ciran-service");
      return res.getTimeline();
    },
  });

  return (
    <AppShell>
      <PageHeader
        title="Global Temporal Analysis"
        subtitle="Chronological sequence of connected events across all investigations."
      />
      <Panel title="All Events" bodyClassName="p-4">
        {isLoading ? (
          <div className="py-10 text-center text-muted-foreground">Loading timeline...</div>
        ) : (
          <TimelineView events={events || []} />
        )}
      </Panel>
    </AppShell>
  );
}
