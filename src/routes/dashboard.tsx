import { createFileRoute, Link } from "@tanstack/react-router";
import { useQuery, useQueryClient } from "@tanstack/react-query";
import { useState } from "react";
import {
  CartesianGrid,
  Line,
  LineChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";
import { AppShell } from "@/components/ciran/app-shell";
import { NetworkGraph } from "@/components/ciran/network-graph";
import { ActionButton, PageHeader, Panel, SeverityBadge, Tag } from "@/components/ciran/ui-kit";
import { QueryLoader } from "@/components/ciran/query-loader";
import {
  getActivity,
  getIntelligenceAlerts,
  getKpis,
  getNetwork,
  getTrend,
  ingestDemoData,
} from "@/lib/ciran-service";

export const Route = createFileRoute("/dashboard")({
  head: () => ({
    meta: [
      { title: "Intelligence Overview — CIRAN" },
      {
        name: "description",
        content:
          "Unified intelligence overview: priority signals, network activity, cross-case connections and detection trends.",
      },
      { property: "og:title", content: "Intelligence Overview — CIRAN" },
      {
        property: "og:description",
        content: "Unified intelligence from connected investigation records.",
      },
    ],
  }),
  component: DashboardPage,
});

function DashboardPage() {
  const queryClient = useQueryClient();
  const [isIngesting, setIsIngesting] = useState(false);

  const kpisQuery = useQuery({ queryKey: ["kpis"], queryFn: getKpis });
  const alertsQuery = useQuery({ queryKey: ["alerts"], queryFn: getIntelligenceAlerts });
  const activityQuery = useQuery({ queryKey: ["activity"], queryFn: getActivity });
  const trendQuery = useQuery({ queryKey: ["trend"], queryFn: getTrend });
  const networkQuery = useQuery({
    queryKey: ["network", "dashboard"],
    queryFn: () => getNetwork({ entityTypes: ["person", "phone", "vehicle", "location", "case"] }),
  });

  const handleIngest = async () => {
    setIsIngesting(true);
    try {
      await ingestDemoData();
      queryClient.invalidateQueries();
    } finally {
      setIsIngesting(false);
    }
  };

  return (
    <AppShell>
      <PageHeader
        title="Intelligence Overview"
        subtitle="Unified intelligence from connected investigation records"
        actions={
          <>
            <Tag tone="outline">Source systems: CCTNS · ICJS</Tag>
            <ActionButton onClick={handleIngest} disabled={isIngesting}>
              {isIngesting ? "Loading Demo Data..." : "Load Demo Data"}
            </ActionButton>
            <Link to="/network">
              <ActionButton variant="primary">Open Network Intelligence</ActionButton>
            </Link>
          </>
        }
      />

      <div className="grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
        <QueryLoader isLoading={kpisQuery.isLoading} error={kpisQuery.error} data={kpisQuery.data}>
          {(kpis) => (
            <>
              {kpis.map((k) => (
                <div key={k.label} className="panel p-5 bg-surface/50 border-border/50">
                  <div className="flex justify-between items-start">
                    <p className="text-[11px] font-semibold tracking-wider text-muted-foreground uppercase">
                      {k.label}
                    </p>
                  </div>
                  <p className="mt-3 font-mono text-2xl font-medium text-foreground">{k.value}</p>
                  <div className="mt-3">
                    <SeverityBadge severity={k.tone}>{k.delta}</SeverityBadge>
                  </div>
                </div>
              ))}
            </>
          )}
        </QueryLoader>
      </div>

      <div className="grid gap-5 xl:grid-cols-[1.1fr_1fr]">
        <Panel
          title="Intelligence Alerts"
          description="Signals detected across connected records"
          action={
            <Link to="/alerts" className="text-xs text-primary hover:underline">
              View all
            </Link>
          }
          bodyClassName="divide-y divide-border p-0 min-h-[380px]"
        >
          <QueryLoader
            isLoading={alertsQuery.isLoading}
            error={alertsQuery.error}
            data={alertsQuery.data?.slice(0, 4)}
          >
            {(alerts) => (
              <>
                {alerts.map((a) => (
                  <div
                    key={a.id}
                    className="flex flex-col gap-2 p-5 hover:bg-surface-2 transition-colors"
                  >
                    <div className="flex items-center justify-between">
                      <div className="flex items-center gap-2">
                        <SeverityBadge severity={a.severity} />
                        <span className="font-mono text-[11px] text-muted-foreground">
                          {a.case}
                        </span>
                      </div>
                      <span className="text-[10px] text-muted-foreground/80">{a.timestamp}</span>
                    </div>
                    <p className="text-sm font-semibold text-foreground mt-1">{a.title}</p>
                    <p className="text-xs leading-relaxed text-muted-foreground max-w-lg">
                      {a.explanation}
                    </p>
                    <div className="flex items-center justify-between mt-2 pt-2 border-t border-border/50">
                      <span className="font-mono text-[11px] text-muted-foreground">
                        Confidence: {a.confidence}%
                      </span>
                      <Link to="/network">
                        <ActionButton variant="primary">Review Signal</ActionButton>
                      </Link>
                    </div>
                  </div>
                ))}
              </>
            )}
          </QueryLoader>
        </Panel>

        <Panel
          title="Network Activity"
          description="Persons → Phones → Vehicles → Locations → Cases"
          bodyClassName="p-2 min-h-[380px]"
        >
          <QueryLoader
            isLoading={networkQuery.isLoading}
            error={networkQuery.error}
            data={networkQuery.data}
            isEmpty={(data) => data.nodes.length === 0}
          >
            {({ nodes, edges }) => (
              <NetworkGraph nodes={nodes} edges={edges} height={380} compact />
            )}
          </QueryLoader>
        </Panel>
      </div>

      <div className="grid gap-5 xl:grid-cols-[1fr_1fr]">
        <Panel title="Recent Investigation Activity" bodyClassName="p-0 min-h-[240px]">
          <QueryLoader
            isLoading={activityQuery.isLoading}
            error={activityQuery.error}
            data={activityQuery.data}
          >
            {(activity) => (
              <table className="w-full text-sm">
                <thead>
                  <tr className="border-b border-border text-left text-[11px] tracking-wider text-muted-foreground uppercase">
                    <th className="px-4 py-2 font-medium">Investigation</th>
                    <th className="px-4 py-2 font-medium">Action</th>
                    <th className="px-4 py-2 font-medium">Officer</th>
                    <th className="px-4 py-2 font-medium">Time</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-border">
                  {activity.map((a, i) => (
                    <tr key={i} className="hover:bg-surface-2">
                      <td className="px-4 py-2.5 font-mono text-xs text-primary">
                        {a.investigation}
                      </td>
                      <td className="px-4 py-2.5 text-foreground">{a.action}</td>
                      <td className="px-4 py-2.5 text-muted-foreground">{a.officer}</td>
                      <td className="px-4 py-2.5 text-xs text-muted-foreground">{a.timestamp}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            )}
          </QueryLoader>
        </Panel>

        <Panel
          title="Intelligence Trend"
          description="Detected relationships and patterns over time"
          bodyClassName="min-h-[240px]"
        >
          <QueryLoader
            isLoading={trendQuery.isLoading}
            error={trendQuery.error}
            data={trendQuery.data}
          >
            {(trend) => (
              <div className="h-[240px] w-full">
                <ResponsiveContainer width="100%" height="100%">
                  <LineChart data={trend} margin={{ top: 8, right: 8, bottom: 0, left: -18 }}>
                    <CartesianGrid stroke="var(--color-border)" vertical={false} />
                    <XAxis
                      dataKey="month"
                      stroke="var(--color-muted-foreground)"
                      fontSize={11}
                      tickLine={false}
                      axisLine={false}
                    />
                    <YAxis
                      stroke="var(--color-muted-foreground)"
                      fontSize={11}
                      tickLine={false}
                      axisLine={false}
                    />
                    <Tooltip
                      contentStyle={{
                        background: "var(--color-popover)",
                        border: "1px solid var(--color-border-strong)",
                        borderRadius: 8,
                        fontSize: 12,
                        color: "var(--color-foreground)",
                      }}
                    />
                    <Line
                      type="monotone"
                      dataKey="relationships"
                      stroke="var(--color-primary)"
                      strokeWidth={2}
                      dot={false}
                      name="Relationships"
                    />
                    <Line
                      type="monotone"
                      dataKey="patterns"
                      stroke="var(--color-high)"
                      strokeWidth={2}
                      dot={false}
                      name="Patterns"
                    />
                  </LineChart>
                </ResponsiveContainer>
              </div>
            )}
          </QueryLoader>
        </Panel>
      </div>
    </AppShell>
  );
}
