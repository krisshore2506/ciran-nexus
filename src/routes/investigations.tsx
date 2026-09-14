import { createFileRoute, Link } from "@tanstack/react-router";
import { useState } from "react";
import { useQuery } from "@tanstack/react-query";
import { Search } from "lucide-react";
import { AppShell } from "@/components/ciran/app-shell";
import { NetworkGraph } from "@/components/ciran/network-graph";
import { AiInsight } from "@/components/ciran/ai-insight";
import {
  ActionButton,
  Confidence,
  Disclaimer,
  EntityChip,
  KeyValue,
  PageHeader,
  Panel,
  SeverityBadge,
  Tag,
} from "@/components/ciran/ui-kit";
import { QueryLoader } from "@/components/ciran/query-loader";
import {
  entityTypeLabel,
  relationTypeLabel,
  type EntityType,
  type RelationType,
} from "@/lib/ciran-data";
import {
  getEntity,
  getEvidence,
  getNeighbours,
  getNetwork,
  getTimeline,
  searchEntities,
} from "@/lib/ciran-service";

export const Route = createFileRoute("/investigations")({
  head: () => ({
    meta: [
      { title: "Investigation Workspace — CIRAN" },
      {
        name: "description",
        content:
          "Search persons, phones, vehicles, cases and locations to open a unified entity profile with network, timeline and evidence context.",
      },
      { property: "og:title", content: "Investigation Workspace — CIRAN" },
      {
        property: "og:description",
        content: "Unified entity profiles built from fragmented investigation records.",
      },
    ],
  }),
  component: WorkspacePage,
});

const tabs = ["Overview", "Network", "Timeline", "Cases", "Evidence", "AI Insights"] as const;
type Tab = (typeof tabs)[number];

function WorkspacePage() {
  const [query, setQuery] = useState("");
  const [selectedId, setSelectedId] = useState("P-RAVI");
  const [tab, setTab] = useState<Tab>("Overview");

  const resultsQuery = useQuery({
    queryKey: ["search", query],
    queryFn: () => searchEntities(query),
  });
  const entityQuery = useQuery({
    queryKey: ["entity", selectedId],
    queryFn: () => getEntity(selectedId),
    enabled: !!selectedId,
  });
  const neighboursQuery = useQuery({
    queryKey: ["neighbours", selectedId],
    queryFn: () => getNeighbours(selectedId),
    enabled: !!selectedId,
  });
  const networkQuery = useQuery({ queryKey: ["network"], queryFn: () => getNetwork() });
  const timelineQuery = useQuery({ queryKey: ["timeline"], queryFn: () => getTimeline() });
  const evidenceQuery = useQuery({ queryKey: ["evidence"], queryFn: () => getEvidence() });

  return (
    <AppShell>
      <PageHeader
        title="Investigation Workspace"
        subtitle="Resolve fragmented records into a single investigative view"
        actions={<Tag tone="outline">Active investigation: CASE-203</Tag>}
      />

      <div className="grid gap-5 xl:grid-cols-[320px_1fr]">
        <div className="space-y-3">
          <div className="relative">
            <Search className="absolute top-1/2 left-3 size-4 -translate-y-1/2 text-muted-foreground" />
            <input
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="Search person, phone, vehicle, case or location..."
              className="w-full rounded-md border border-border bg-input py-2.5 pr-3 pl-9 text-sm text-foreground placeholder:text-muted-foreground focus:border-primary/60 focus:outline-none"
            />
          </div>

          <Panel title="Search results" bodyClassName="p-0 min-h-[400px]">
            <QueryLoader
              isLoading={resultsQuery.isLoading}
              error={resultsQuery.error}
              data={resultsQuery.data}
              emptyMessage="No intelligence data available."
            >
              {(results) => (
                <ul className="divide-y divide-border">
                  {results.map((r) => (
                    <li key={r.id}>
                      <button
                        onClick={() => setSelectedId(r.id)}
                        className={`flex w-full flex-col gap-1 px-4 py-3 text-left transition-colors hover:bg-surface-2 ${
                          r.id === selectedId ? "bg-accent" : ""
                        }`}
                      >
                        <div className="flex items-center justify-between gap-2">
                          <EntityChip type={r.type} label={r.label} />
                          <span className="text-[10px] tracking-wider text-muted-foreground uppercase">
                            {entityTypeLabel[r.type as EntityType]}
                          </span>
                        </div>
                        <span className="text-xs text-muted-foreground">{r.subtitle}</span>
                      </button>
                    </li>
                  ))}
                  {results.length === 0 && (
                    <li className="px-4 py-6 text-sm text-muted-foreground">
                      No matching records in the connected source systems.
                    </li>
                  )}
                </ul>
              )}
            </QueryLoader>
          </Panel>
        </div>

        <div className="space-y-4">
          <QueryLoader
            isLoading={entityQuery.isLoading}
            error={entityQuery.error}
            data={entityQuery.data}
          >
            {(entity) => (
              <div className="panel p-4">
                <div className="flex flex-wrap items-start justify-between gap-4">
                  <div>
                    <p className="text-[11px] tracking-wider text-muted-foreground uppercase">
                      Unified Entity Profile
                    </p>
                    <h2 className="mt-1 text-lg font-semibold text-foreground">{entity.label}</h2>
                    <p className="text-xs text-muted-foreground">{entity.subtitle}</p>
                  </div>
                  {entity.priority && (
                    <div className="w-52 rounded-md border border-border bg-surface-2 p-3">
                      <div className="flex items-center justify-between">
                        <span className="text-[11px] tracking-wider text-muted-foreground uppercase">
                          Investigation Priority
                        </span>
                        <SeverityBadge
                          severity={entity.priorityBand === "HIGH" ? "critical" : "medium"}
                        >
                          {entity.priorityBand}
                        </SeverityBadge>
                      </div>
                      <p className="mt-1 font-mono text-2xl font-semibold">{entity.priority}</p>
                      <ul className="mt-2 space-y-1">
                        {entity.priorityFactors?.map((f: any) => (
                          <li key={f.label} className="flex justify-between text-[11px]">
                            <span className="text-muted-foreground">{f.label}</span>
                            <span className="font-mono">{f.weight}</span>
                          </li>
                        ))}
                      </ul>
                    </div>
                  )}
                </div>

                <div className="mt-4 grid gap-3 sm:grid-cols-4">
                  <Stat label="Entity Type" value={entityTypeLabel[entity.type as EntityType]} />
                  <Stat label="Associated Cases" value={String(entity.cases?.length ?? 0)} />
                  <Stat label="Known Relationships" value={String(entity.relationships ?? 0)} />
                  <Stat label="Recent Activity" value={`${entity.recentEvents ?? 0} events`} />
                </div>

                <div className="mt-4">
                  <Disclaimer>
                    Priority score is an investigative signal and does not represent guilt or
                    criminality.
                  </Disclaimer>
                </div>
              </div>
            )}
          </QueryLoader>

          {entityQuery.data && (
            <>
              <div className="flex flex-wrap gap-1 border-b border-border">
                {tabs.map((t) => (
                  <button
                    key={t}
                    onClick={() => setTab(t)}
                    className={`-mb-px border-b-2 px-3 py-2 text-sm transition-colors ${
                      tab === t
                        ? "border-primary text-foreground"
                        : "border-transparent text-muted-foreground hover:text-foreground"
                    }`}
                  >
                    {t}
                  </button>
                ))}
              </div>

              {tab === "Overview" && (
                <Panel title="Record attributes">
                  <KeyValue items={entityQuery.data.attributes ?? []} />
                </Panel>
              )}

              {tab === "Network" && (
                <Panel title="Direct relationships" bodyClassName="space-y-3 min-h-[400px]">
                  <QueryLoader
                    isLoading={networkQuery.isLoading || neighboursQuery.isLoading}
                    error={networkQuery.error || neighboursQuery.error}
                    data={networkQuery.data}
                    emptyMessage="No intelligence data available."
                  >
                    {({ nodes, edges }) => (
                      <>
                        <NetworkGraph
                          nodes={nodes}
                          edges={edges}
                          selectedId={selectedId}
                          onSelect={setSelectedId}
                          height={380}
                          compact
                        />
                        <div className="flex flex-wrap gap-2">
                          {neighboursQuery.data?.map(({ relation, other }) => (
                            <EntityChip
                              key={other.id + relation.type}
                              type={other.type}
                              label={`${other.label} · ${relationTypeLabel[relation.type as RelationType]}`}
                              onClick={() => setSelectedId(other.id)}
                            />
                          ))}
                        </div>
                      </>
                    )}
                  </QueryLoader>
                </Panel>
              )}

              {tab === "Timeline" && (
                <Panel title="Recent activity" bodyClassName="p-0 min-h-[200px]">
                  <QueryLoader
                    isLoading={timelineQuery.isLoading}
                    error={timelineQuery.error}
                    data={timelineQuery.data?.filter((e: any) => e.entities.includes(selectedId))}
                    emptyMessage="No intelligence data available."
                  >
                    {(events) => (
                      <ul className="divide-y divide-border">
                        {events.map((e: any) => (
                          <li key={e.id} className="flex gap-4 px-4 py-3">
                            <span className="w-16 shrink-0 font-mono text-xs text-primary">
                              {e.day}
                            </span>
                            <div>
                              <p className="text-sm text-foreground">{e.title}</p>
                              <p className="text-xs text-muted-foreground">{e.detail}</p>
                              <p className="mt-1 font-mono text-[11px] text-muted-foreground">
                                Source: {e.record}
                              </p>
                            </div>
                          </li>
                        ))}
                        {events.length === 0 && (
                          <li className="px-4 py-6 text-sm text-muted-foreground">
                            No temporal events recorded for this entity.
                          </li>
                        )}
                      </ul>
                    )}
                  </QueryLoader>
                </Panel>
              )}

              {tab === "Cases" && (
                <Panel title="Associated cases" bodyClassName="grid gap-3 sm:grid-cols-3">
                  {(entityQuery.data.cases ?? []).map((c: string) => (
                    <div key={c} className="rounded-md border border-border p-3">
                      <p className="font-mono text-xs text-primary">{c}</p>
                      <p className="mt-1 text-sm text-foreground">View Case Details</p>
                    </div>
                  ))}
                  {(entityQuery.data.cases ?? []).length === 0 && (
                    <p className="text-sm text-muted-foreground">No case associations.</p>
                  )}
                </Panel>
              )}

              {tab === "Evidence" && (
                <Panel title="Supporting records" bodyClassName="p-0 min-h-[200px]">
                  <QueryLoader
                    isLoading={evidenceQuery.isLoading}
                    error={evidenceQuery.error}
                    data={evidenceQuery.data}
                    emptyMessage="No intelligence data available."
                  >
                    {(evidence) => (
                      <ul className="divide-y divide-border">
                        {evidence.map((e: any) => (
                          <li key={e.id} className="space-y-2 px-4 py-3">
                            <p className="text-sm text-foreground">{e.insight}</p>
                            <div className="flex flex-wrap gap-1.5">
                              {e.sources.map((s: any) => (
                                <Tag key={s.id}>{s.id}</Tag>
                              ))}
                            </div>
                            <p className="text-xs text-muted-foreground">Status: {e.status}</p>
                          </li>
                        ))}
                      </ul>
                    )}
                  </QueryLoader>
                </Panel>
              )}

              {tab === "AI Insights" && (
                <Panel title="Explainable AI">
                  <div className="flex flex-col items-center justify-center p-8 text-center text-muted-foreground border border-dashed border-border rounded-md">
                    <p className="mb-4">Real-time explainable AI insights require active Agent analysis.</p>
                    <Link to="/copilot">
                      <ActionButton variant="primary">Ask CIRAN Copilot for AI Analysis</ActionButton>
                    </Link>
                  </div>
                </Panel>
              )}

              <div className="flex flex-wrap gap-2 mt-4">
                <Link to="/network">
                  <ActionButton variant="primary">Open in Network Intelligence</ActionButton>
                </Link>
                <Link to="/timeline">
                  <ActionButton>Temporal Analysis</ActionButton>
                </Link>
                <Link to="/copilot">
                  <ActionButton>Ask CIRAN Copilot</ActionButton>
                </Link>
              </div>
            </>
          )}
        </div>
      </div>
    </AppShell>
  );
}

function Stat({ label, value }: { label: string; value: string }) {
  return (
    <div className="rounded-md border border-border bg-surface-2 p-3">
      <p className="text-[11px] tracking-wider text-muted-foreground uppercase">{label}</p>
      <p className="mt-1 text-sm font-semibold text-foreground">{value}</p>
    </div>
  );
}
