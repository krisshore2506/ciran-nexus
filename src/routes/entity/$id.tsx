import { createFileRoute, Link, Outlet } from "@tanstack/react-router";
import { useQuery } from "@tanstack/react-query";
import { AppShell } from "@/components/ciran/app-shell";
import { PageHeader, Tag, SeverityBadge } from "@/components/ciran/ui-kit";
import type { Entity } from "@/lib/ciran-data";

export const Route = createFileRoute("/entity/$id")({
  component: EntityLayout,
});

function EntityLayout() {
  const { id } = Route.useParams();

  const { data: entity, isLoading } = useQuery<Entity>({
    queryKey: ["entity", id],
    queryFn: async () => {
      const res = await fetch(`/api/entities/${id}`);
      if (!res.ok) throw new Error("Failed to fetch entity");
      return res.json();
    },
  });

  if (isLoading) {
    return (
      <AppShell>
        <div className="flex items-center justify-center py-20 text-muted-foreground">
          Loading entity profile...
        </div>
      </AppShell>
    );
  }

  if (!entity) {
    return (
      <AppShell>
        <div className="flex items-center justify-center py-20 text-muted-foreground">
          Entity not found.
        </div>
      </AppShell>
    );
  }

  return (
    <AppShell>
      <PageHeader
        title={entity.label}
        subtitle={entity.subtitle}
        actions={
          <div className="flex gap-2">
            {entity.priorityBand && (
              <SeverityBadge severity={entity.priorityBand === "HIGH" ? "critical" : "medium"}>
                Priority: {entity.priority}
              </SeverityBadge>
            )}
            <Tag tone="outline">{entity.type.toUpperCase()}</Tag>
          </div>
        }
      />

      {/* Tabs */}
      <div className="flex gap-6 border-b border-border/60 text-sm font-medium mt-6">
        <Link
          to={`/entity/${id}`}
          className="pb-3 text-muted-foreground hover:text-foreground transition-colors [&.active]:border-b-2 [&.active]:border-primary [&.active]:text-foreground"
          activeOptions={{ exact: true }}
        >
          Profile Details
        </Link>
        <Link
          to={`/entity/${id}/network`}
          className="pb-3 text-muted-foreground hover:text-foreground transition-colors [&.active]:border-b-2 [&.active]:border-primary [&.active]:text-foreground"
        >
          Network Intelligence
        </Link>
        <Link
          to={`/entity/${id}/timeline`}
          className="pb-3 text-muted-foreground hover:text-foreground transition-colors [&.active]:border-b-2 [&.active]:border-primary [&.active]:text-foreground"
        >
          Timeline
        </Link>
      </div>

      <div className="pt-6">
        <Outlet />
      </div>
    </AppShell>
  );
}
