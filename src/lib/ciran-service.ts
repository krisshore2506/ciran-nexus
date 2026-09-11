import type { Entity, EntityType, Relation, RelationType } from "./ciran-data";

export interface CopilotResponse {
  summary: string;
  facts?: string[];
  derived_findings?: string[];
  limitations?: string[];
  chips: string[];
  path?: string[];
  timeline?: { day: string; title: string }[];
  evidence: string[];
  confidence: number;
  caution?: string;
}

// Helper to fetch from backend
async function fetchApi<T>(path: string, options?: RequestInit): Promise<T> {
  const response = await fetch(path, options);
  if (!response.ok) {
    throw new Error(`API Error: ${response.status} - ${await response.text()}`);
  }
  return response.json();
}

export async function getEntities(query?: string): Promise<Entity[]> {
  const url = query ? `/api/entities?q=${encodeURIComponent(query)}` : "/api/entities";
  return fetchApi<Entity[]>(url);
}

export async function getEntity(id: string): Promise<Entity | undefined> {
  try {
    return await fetchApi<Entity>(`/api/entities/${encodeURIComponent(id)}`);
  } catch (err) {
    return undefined;
  }
}

export async function searchEntities(query: string): Promise<Entity[]> {
  return getEntities(query);
}

export async function getCases(): Promise<Entity[]> {
  return fetchApi<Entity[]>("/api/cases");
}

export async function getNetwork(filters?: {
  entityTypes?: EntityType[];
  relationTypes?: RelationType[];
}): Promise<{ nodes: Entity[]; edges: Relation[] }> {
  // If specific node networks are needed, it would be /api/entities/:id/network.
  // The global network route might be heavy. For now, we query the root /api/network if needed,
  // but ideally we only use the entity-specific one in UI.
  // If we really need global:
  const data = await fetchApi<{ nodes: Entity[]; edges: Relation[] }>("/api/network");

  const et = filters?.entityTypes;
  const rt = filters?.relationTypes;
  const nodes = data.nodes.filter(
    (e) => !et || et.length === 0 || et.includes(e.type as EntityType),
  );
  const ids = new Set(nodes.map((n) => n.id));
  const edges = data.edges.filter(
    (r) =>
      ids.has(r.source) &&
      ids.has(r.target) &&
      (!rt || rt.length === 0 || rt.includes(r.type as RelationType)),
  );
  return { nodes, edges };
}

export async function getEntityNetwork(
  id: string,
): Promise<{ nodes: Entity[]; edges: Relation[] }> {
  return fetchApi<{ nodes: Entity[]; edges: Relation[] }>(
    `/api/entities/${encodeURIComponent(id)}/network`,
  );
}

export async function getNeighbours(id: string): Promise<{ relation: Relation; other: Entity }[]> {
  const { nodes, edges } = await getEntityNetwork(id);
  return edges
    .filter((r) => r.source === id || r.target === id)
    .map((r) => {
      const otherId = r.source === id ? r.target : r.source;
      const other = nodes.find((n) => n.id === otherId);
      return other ? { relation: r, other } : null;
    })
    .filter((x): x is { relation: Relation; other: Entity } => x !== null);
}

export async function getTimeline(id?: string) {
  if (id) {
    return fetchApi<any[]>(`/api/entities/${encodeURIComponent(id)}/timeline`);
  }
  return fetchApi<any[]>("/api/timeline"); // fallback if needed
}

export async function getCrossCaseLinks() {
  return fetchApi<any[]>("/api/cross-case");
}

export async function getIntelligenceAlerts() {
  return fetchApi<any[]>("/api/alerts");
}

export async function getPatterns() {
  return fetchApi<any[]>("/api/patterns");
}

export async function getEvidence(id?: string) {
  if (!id) return [];
  return fetchApi<any>(`/api/evidence/${encodeURIComponent(id)}`);
}

export async function askCopilot(query: string, contextId?: string, history?: {role: string, content: string}[]): Promise<CopilotResponse> {
  return fetchApi<CopilotResponse>("/api/copilot/query", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ query, contextId, conversation_history: history }),
  });
}

// Mocked for Dashboard visual purposes if backend doesn't have it yet,
// but we will implement /api/kpis soon. For now we fetch them if route exists, else fallback.
export async function getKpis() {
  try {
    return await fetchApi<any[]>("/api/kpis");
  } catch {
    return [
      { label: "Active Investigations", value: "-", delta: "Pending", tone: "info" as const },
      { label: "High-Priority Signals", value: "-", delta: "Pending", tone: "critical" as const },
      { label: "Total Entities", value: "-", delta: "Pending", tone: "high" as const },
      { label: "Cross-Case Links", value: "-", delta: "Pending", tone: "medium" as const },
    ];
  }
}

// Activity and trend can be mocked or fetched if we add a route.
export async function getActivity() {
  return [
    {
      investigation: "CASE-101",
      action: "Flagged High Risk",
      officer: "System",
      timestamp: "Just now",
    },
  ];
}

export async function getEntityResolution() {
  // Mocked since backend entity resolution just merges nodes inherently.
  return {
    confidence: 85,
    recordA: {
      title: "CCTNS Record",
      name: "Ravi Kumar",
      fields: [{ label: "Phone", value: "9876543210" }],
    },
    recordB: {
      title: "ICJS Record",
      name: "R. Kumar",
      fields: [{ label: "Phone", value: "9876543210" }],
    },
    matching: ["Phone number matches exactly"],
    nonMatching: ["Name spelling difference"],
  };
}

export async function getTrend() {
  return [
    { month: "Jan", relationships: 40, patterns: 12 },
    { month: "Feb", relationships: 55, patterns: 18 },
  ];
}

export async function ingestDemoData() {
  const res = await fetch("/api/ingestion/load", { method: "POST" });
  if (!res.ok) throw new Error("Failed to load demo data");
  return res.json();
}
