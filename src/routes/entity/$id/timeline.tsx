import { createFileRoute } from "@tanstack/react-router";
import { useQuery } from "@tanstack/react-query";
import { Panel } from "@/components/ciran/ui-kit";
import { TimelineView } from "@/components/ciran/timeline-view";

export const Route = createFileRoute("/entity/$id/timeline")({
  component: EntityTimelineTab,
});

function EntityTimelineTab() {
  const { id } = Route.useParams();

  const { data: events, isLoading } = useQuery({
    queryKey: ["entity-timeline", id],
    queryFn: async () => {
      const res = await fetch(`/api/entities/${id}/timeline`);
      return res.json();
    },
  });

  if (isLoading)
    return <div className="py-10 text-center text-muted-foreground">Loading timeline...</div>;
  if (!events) return null;

  return (
    <Panel title="Temporal Analysis" bodyClassName="p-4">
      <TimelineView events={events} />
    </Panel>
  );
}
