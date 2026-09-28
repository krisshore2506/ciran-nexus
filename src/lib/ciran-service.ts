import {
  entities as mockEntities,
  relations as mockRelations,
  timeline as mockTimeline,
  alerts as mockAlerts,
  patterns as mockPatterns,
  crossCaseLinks as mockCrossCaseLinks,
  evidence as mockEvidence,
  type Entity,
  type EntityType,
  type Relation,
  type RelationType,
  type TimelineEvent,
} from "./ciran-data";

export type { Entity, EntityType, Relation, RelationType };

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
  intent?: string;
}

// Configurable Mock Data flag
// Default: false in production/testing unless explicitly overridden
const USE_MOCK = import.meta.env.VITE_USE_MOCK_DATA === "true";

// Helper to fetch from backend
async function fetchApi<T>(path: string, options?: RequestInit): Promise<T> {
  // If API Base URL is configured, prepend it. Otherwise assume same origin proxy.
  const baseUrl = import.meta.env.VITE_API_BASE_URL || "";
  const response = await fetch(`${baseUrl}${path}`, options);
  if (!response.ok) {
    throw new Error(`API Error: ${response.status} - ${await response.text()}`);
  }
  return response.json();
}

export async function getEntities(query?: string): Promise<Entity[]> {
  if (USE_MOCK) {
    if (query) {
      const q = query.toLowerCase();
      return mockEntities.filter(
        (e) => e.label.toLowerCase().includes(q) || e.id.toLowerCase().includes(q),
      );
    }
    return mockEntities;
  }
  const url = query ? `/api/entities?q=${encodeURIComponent(query)}` : "/api/entities";
  return fetchApi<Entity[]>(url);
}

export async function getEntity(id: string): Promise<Entity | undefined> {
  if (USE_MOCK) {
    return mockEntities.find((e) => e.id === id);
  }
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
  if (USE_MOCK) {
    return mockEntities.filter((e) => e.type === "case");
  }
  return fetchApi<Entity[]>("/api/cases");
}

export async function getNetwork(filters?: {
  entityTypes?: EntityType[];
  relationTypes?: RelationType[];
}): Promise<{ nodes: Entity[]; edges: Relation[] }> {
  let data: { nodes: Entity[]; edges: Relation[] };

  if (USE_MOCK) {
    data = { nodes: mockEntities, edges: mockRelations };
  } else {
    data = await fetchApi<{ nodes: Entity[]; edges: Relation[] }>("/api/network");
  }

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
  if (USE_MOCK) {
    const edges = mockRelations.filter((r) => r.source === id || r.target === id);
    const relatedIds = new Set<string>();
    edges.forEach((e) => {
      relatedIds.add(e.source);
      relatedIds.add(e.target);
    });
    relatedIds.add(id);
    const nodes = mockEntities.filter((n) => relatedIds.has(n.id));
    return { nodes, edges };
  }
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

export async function getTimeline(id?: string): Promise<TimelineEvent[]> {
  if (USE_MOCK) {
    if (id) {
      return mockTimeline.filter((t) => t.entities.includes(id));
    }
    return mockTimeline;
  }
  if (id) {
    return fetchApi<TimelineEvent[]>(`/api/entities/${encodeURIComponent(id)}/timeline`);
  }
  return fetchApi<TimelineEvent[]>("/api/timeline"); // fallback if needed
}

export async function getCrossCaseLinks() {
  if (USE_MOCK) return mockCrossCaseLinks;
  return fetchApi<unknown[]>("/api/cross-case");
}

export async function getIntelligenceAlerts() {
  if (USE_MOCK) return mockAlerts;
  return fetchApi<unknown[]>("/api/alerts");
}

export async function getPatterns() {
  if (USE_MOCK) return mockPatterns;
  return fetchApi<unknown[]>("/api/patterns");
}

export async function getEvidence(id?: string) {
  if (USE_MOCK) {
    if (!id) return mockEvidence;
    // Basic mock logic if id provided
    return mockEvidence;
  }
  if (!id) return fetchApi<unknown[]>("/api/evidence");
  return fetchApi<unknown>(`/api/evidence/${encodeURIComponent(id)}`);
}

export async function askCopilot(
  query: string,
  contextId?: string,
  history?: { role: string; content: string }[],
): Promise<CopilotResponse> {
  if (USE_MOCK) {
    return {
      summary: "This is a mock response from CIRAN Copilot.",
      chips: ["Mock Data"],
      confidence: 100,
      evidence: ["MOCK-1"],
    };
  }
  return fetchApi<CopilotResponse>("/api/copilot/query", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ query, contextId, conversation_history: history }),
  });
}

// Mocked for Dashboard visual purposes if backend doesn't have it yet,
// but we will implement /api/kpis soon. For now we fetch them if route exists, else fallback.
export async function getKpis() {
  if (USE_MOCK) {
    return [
      { label: "Active Investigations", value: "14", delta: "+2", tone: "info" as const },
      {
        label: "High-Priority Signals",
        value: "3",
        delta: "Action req",
        tone: "critical" as const,
      },
      { label: "Total Entities", value: "481", delta: "+12", tone: "high" as const },
      { label: "Cross-Case Links", value: "8", delta: "Stable", tone: "medium" as const },
    ];
  }
  try {
    return await fetchApi<unknown[]>("/api/kpis");
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
  if (USE_MOCK) {
    return [
      {
        investigation: "CASE-101",
        action: "Flagged High Risk",
        officer: "System",
        timestamp: "Just now",
      },
    ];
  }
  try {
    return await fetchApi<unknown[]>("/api/activity");
  } catch {
    return [];
  }
}

export async function getEntityResolution() {
  if (USE_MOCK) {
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
  try {
    return await fetchApi<unknown>("/api/entity-resolution");
  } catch {
    return null;
  }
}

export async function getTrend() {
  if (USE_MOCK) {
    return [
      { month: "Jan", relationships: 40, patterns: 12 },
      { month: "Feb", relationships: 55, patterns: 18 },
    ];
  }
  try {
    return await fetchApi<unknown[]>("/api/trend");
  } catch {
    return [];
  }
}

export async function ingestDemoData() {
  const res = await fetch("/api/ingestion/load", { method: "POST" });
  if (!res.ok) throw new Error("Failed to load demo data");
  return res.json();
}
