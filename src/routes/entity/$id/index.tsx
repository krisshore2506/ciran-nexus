import { createFileRoute } from "@tanstack/react-router";
import { useQuery } from "@tanstack/react-query";
import { Panel } from "@/components/ciran/ui-kit";
import type { Entity } from "@/lib/ciran-data";

export const Route = createFileRoute("/entity/$id/")({
  component: EntityProfileIndex,
});

function EntityProfileIndex() {
  const { id } = Route.useParams();

  const { data: entity } = useQuery<Entity>({
    queryKey: ["entity", id],
    queryFn: async () => {
      const res = await fetch(`/api/entities/${id}`);
      return res.json();
    },
  });

  if (!entity) return null;

  return (
    <div className="grid gap-6 md:grid-cols-2">
      <Panel title="Entity Attributes" bodyClassName="p-0">
        <table className="w-full text-sm">
          <tbody className="divide-y divide-border">
            {entity.attributes?.map((attr, i) => (
              <tr key={i} className="hover:bg-surface-2">
                <td className="px-4 py-3 font-medium text-muted-foreground w-1/3">{attr.label}</td>
                <td className="px-4 py-3 text-foreground">{attr.value}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </Panel>

      {entity.priorityFactors && (
        <Panel title="Investigation Priority Signals" bodyClassName="p-0">
          <table className="w-full text-sm">
            <tbody className="divide-y divide-border">
              {entity.priorityFactors.map((factor, i) => (
                <tr key={i} className="hover:bg-surface-2">
                  <td className="px-4 py-3 font-medium text-foreground w-2/3">{factor.label}</td>
                  <td className="px-4 py-3 text-right">
                    <div className="flex items-center justify-end gap-2">
                      <div className="h-1.5 w-16 overflow-hidden rounded-full bg-surface-2">
                        <div
                          className="h-full bg-primary"
                          style={{ width: `${(factor.weight / 40) * 100}%` }}
                        />
                      </div>
                      <span className="font-mono text-xs text-muted-foreground">
                        {factor.weight}
                      </span>
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </Panel>
      )}
    </div>
  );
}
