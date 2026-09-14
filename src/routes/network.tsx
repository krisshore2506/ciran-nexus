import { createFileRoute, Link } from "@tanstack/react-router";
import { useState } from "react";
import { useQuery } from "@tanstack/react-query";
import { X } from "lucide-react";
import { AppShell } from "@/components/ciran/app-shell";
import {
  FilterChips,
  NetworkGraph,
  entityTypeOrder,
  relationTypeOrder,
} from "@/components/ciran/network-graph";
import {
  ActionButton,
  Confidence,
  Disclaimer,
  EntityChip,
  PageHeader,
  Panel,
  PathTrail,
  Tag,
} from "@/components/ciran/ui-kit";
import { QueryLoader } from "@/components/ciran/query-loader";
import {
  entityTypeLabel,
  relationTypeLabel,
  type EntityType,
  type RelationType,
} from "@/lib/ciran-data";
import { getEntity, getNeighbours, getNetwork } from "@/lib/ciran-service";

export const Route = createFileRoute("/network")({
  head: () => ({
    meta: [
      { title: "Network Intelligence — CIRAN" },
      {
        name: "description",
        content:
          "Interactive relationship graph across persons, phones, vehicles, accounts, locations and cases with evidence-linked intelligence panels.",
      },
      { property: "og:title", content: "Network Intelligence — CIRAN" },
      {
        property: "og:description",
        content: "Explore entity relationships and evidence-backed connection paths.",
      },
    ],
  }),
  component: NetworkPage,
});

function NetworkPage() {
  const [entityTypes, setEntityTypes] = useState<EntityType[]>([...entityTypeOrder]);
  const [relationTypes, setRelationTypes] = useState<RelationType[]>([...relationTypeOrder]);
  const [selected, setSelected] = useState<string | null>("P-RAVI");

  const networkQuery = useQuery({
    queryKey: ["network", { entityTypes, relationTypes }],
    queryFn: () => getNetwork({ entityTypes, relationTypes }),
  });

  const entityQuery = useQuery({
    queryKey: ["entity", selected],
    queryFn: () => (selected ? getEntity(selected) : undefined),
    enabled: !!selected,
  });

  const neighboursQuery = useQuery({
    queryKey: ["neighbours", selected],
    queryFn: () => (selected ? getNeighbours(selected) : []),
    enabled: !!selected,
  });

  const toggle = <T extends string>(list: T[], set: (v: T[]) => void, v: T) =>
    set(list.includes(v) ? list.filter((x) => x !== v) : [...list, v]);

  return (
    <AppShell>
      <PageHeader
        title="Network Intelligence"
        subtitle="Relationship graph built from connected investigation records"
        actions={
          <Tag tone="outline">
            {networkQuery.data?.nodes?.length || 0} entities ·{" "}
            {networkQuery.data?.edges?.length || 0} relationships
          </Tag>
        }
      />

      <div className="grid gap-5 xl:grid-cols-[1fr_380px]">
        <div className="space-y-3">
          <div className="panel flex flex-wrap items-center gap-x-6 gap-y-3 p-3">
            <div>
              <p className="mb-1.5 text-[11px] tracking-wider text-muted-foreground uppercase">
                Entity type
              </p>
              <FilterChips
                options={entityTypeOrder}
                labels={entityTypeLabel}
                active={entityTypes}
                onToggle={(v) => toggle(entityTypes, setEntityTypes, v)}
              />
            </div>
            <div>
              <p className="mb-1.5 text-[11px] tracking-wider text-muted-foreground uppercase">
                Relationship type
              </p>
              <FilterChips
                options={relationTypeOrder}
                labels={relationTypeLabel}
                active={relationTypes}
                onToggle={(v) => toggle(relationTypes, setRelationTypes, v)}
              />
            </div>
          </div>

          <div className="min-h-[620px] rounded-md border border-border bg-surface relative">
            <QueryLoader
              isLoading={networkQuery.isLoading}
              error={networkQuery.error}
              data={networkQuery.data}
              isEmpty={(d) => d.nodes.length === 0}
              emptyMessage="No intelligence data available."
            >
              {({ nodes, edges }) => (
                <NetworkGraph
                  nodes={nodes}
                  edges={edges}
                  selectedId={selected}
                  onSelect={setSelected}
                  height={620}
                />
              )}
            </QueryLoader>
          </div>
          <p className="text-xs text-muted-foreground">
            Click a node to open the intelligence panel. Drag to pan, use the controls to zoom.
          </p>
        </div>

        <aside className="panel flex h-fit flex-col xl:sticky xl:top-20 min-h-[500px]">
          {selected ? (
            <QueryLoader
              isLoading={entityQuery.isLoading || neighboursQuery.isLoading}
              error={entityQuery.error || neighboursQuery.error}
              data={entityQuery.data}
              emptyMessage="No intelligence data available."
            >
              {(entity) => (
                <>
                  <header className="flex items-start justify-between gap-3 border-b border-border px-4 py-3">
                    <div>
                      <p className="text-[11px] tracking-wider text-primary uppercase">
                        Selected Entity
                      </p>
                      <p className="text-sm font-semibold text-foreground">{entity.label}</p>
                      <p className="text-xs text-muted-foreground">
                        {entityTypeLabel[entity.type as EntityType]} · {entity.subtitle}
                      </p>
                    </div>
                    <button
                      onClick={() => setSelected(null)}
                      className="rounded p-1 text-muted-foreground hover:bg-surface-2"
                      aria-label="Close panel"
                    >
                      <X className="size-4" />
                    </button>
                  </header>

                  <div className="space-y-4 p-4">


                    <div>
                      <p className="mb-2 text-[11px] font-semibold tracking-wider text-muted-foreground uppercase">
                        Connected entities
                      </p>
                      <ul className="space-y-3">
                        {neighboursQuery.data?.map(({ relation, other }) => (
                          <li
                            key={`${relation.source}-${relation.target}-${relation.type}`}
                            className="rounded-md border border-border/60 bg-surface/30 p-3 hover:border-primary/40 transition-colors"
                          >
                            <div className="flex items-start justify-between gap-2 mb-2">
                              <EntityChip
                                type={other.type}
                                label={other.label}
                                onClick={() => setSelected(other.id)}
                              />
                              <div className="flex flex-col items-end">
                                <span className="font-mono text-[10px] text-muted-foreground mb-0.5">
                                  Conf:
                                </span>
                                <span className="font-mono text-xs font-semibold text-foreground">
                                  {relation.confidence}%
                                </span>
                              </div>
                            </div>
                            <div className="mt-2 text-xs text-muted-foreground border-l-2 border-border pl-2">
                              <p className="font-medium text-foreground mb-0.5">
                                {relationTypeLabel[relation.type as RelationType]}
                              </p>
                              <p>{relation.label}</p>
                            </div>
                            <div className="mt-3 flex items-center justify-between">
                              <span className="font-mono text-[10px] text-muted-foreground">
                                Source: {relation.sourceRecord}
                              </span>
                            </div>
                          </li>
                        ))}
                      </ul>
                    </div>

                    <div className="flex flex-wrap gap-2">
                      <Link to="/evidence">
                        <ActionButton variant="primary">View Evidence</ActionButton>
                      </Link>
                      <ActionButton onClick={() => setEntityTypes([...entityTypeOrder])}>
                        Expand Network
                      </ActionButton>
                      <Link to="/patterns">
                        <ActionButton>Analyze Relationship</ActionButton>
                      </Link>
                    </div>

                    <Disclaimer>
                      Relationships are potential associations derived from source records. They are
                      investigative signals only and require analyst review.
                    </Disclaimer>
                  </div>
                </>
              )}
            </QueryLoader>
          ) : (
            <div className="p-6 text-sm text-muted-foreground">
              Select a node in the graph to open its intelligence panel.
            </div>
          )}
        </aside>
      </div>
    </AppShell>
  );
}
