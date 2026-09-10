import { createFileRoute } from "@tanstack/react-router";
import { useQuery } from "@tanstack/react-query";
import { NetworkGraph } from "@/components/ciran/network-graph";
import { Panel } from "@/components/ciran/ui-kit";

export const Route = createFileRoute("/entity/$id/network")({
  component: EntityNetworkTab,
});

function EntityNetworkTab() {
  const { id } = Route.useParams();

  const { data: network, isLoading } = useQuery({
    queryKey: ["entity-network", id],
    queryFn: async () => {
      const res = await fetch(`/api/entities/${id}/network`);
      return res.json();
    },
  });

  if (isLoading)
    return <div className="py-10 text-center text-muted-foreground">Loading network...</div>;
  if (!network) return null;

  return (
    <Panel title="Local Network View" bodyClassName="p-2">
      <NetworkGraph nodes={network.nodes} edges={network.edges} height={600} />
    </Panel>
  );
}
