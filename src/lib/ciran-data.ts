// CIRAN synthetic intelligence dataset.
// All records are fictional and generated for prototype demonstration only.

export type EntityType = "person" | "phone" | "vehicle" | "account" | "location" | "case";

export type Severity = "critical" | "high" | "medium" | "info";

export interface Entity {
  id: string;
  type: EntityType;
  label: string;
  subtitle: string;
  priority?: number;
  priorityBand?: "HIGH" | "MEDIUM" | "LOW";
  cases?: string[];
  relationships?: number;
  recentEvents?: number;
  attributes?: { label: string; value: string }[];
  priorityFactors?: { label: string; weight: number }[];
}

export type RelationType = "communication" | "financial" | "vehicle" | "location" | "case";

export interface Relation {
  source: string;
  target: string;
  type: RelationType;
  label: string;
  confidence: number;
  sourceRecord: string;
}

export interface TimelineEvent {
  id: string;
  date: string;
  day: string;
  category: RelationType;
  title: string;
  detail: string;
  entities: string[];
  record: string;
}

export interface Alert {
  id: string;
  severity: Severity;
  title: string;
  explanation: string;
  case: string;
  timestamp: string;
  confidence: number;
  entities: string[];
}

export interface EvidenceItem {
  id: string;
  insight: string;
  sources: { id: string; type: string; timestamp: string }[];
  analysis: string;
  relationship: string;
  status: "Pending Analyst Review" | "Accepted" | "Rejected";
  audit: { stage: string; actor: string; timestamp: string; note?: string }[];
}

export interface CrossCaseLink {
  cases: string[];
  shared: { type: string; value: string }[];
  path: string[];
  confidence: number;
  evidence: string[];
  summary: string;
}

export interface PatternInsight {
  id: string;
  category:
    | "Emerging Network Clusters"
    | "Indirect Relationships"
    | "Repeated Entity Associations"
    | "Unusual Activity Patterns"
    | "Cross-Case Similarities";
  title: string;
  entities: string[];
  path?: string[];
  confidence: number;
  why: string;
  evidence: string[];
}

export const entities: Entity[] = [
  {
    id: "P-RAVI",
    type: "person",
    label: "Ravi Kumar",
    subtitle: "Person of interest · 8 associated cases",
    priority: 91,
    priorityBand: "HIGH",
    cases: ["CASE-101", "CASE-156", "CASE-203"],
    relationships: 14,
    recentEvents: 7,
    attributes: [
      { label: "Entity Type", value: "Person" },
      { label: "Registered Phone", value: "XXXXX1234" },
      { label: "Linked Vehicle", value: "TN-XX-1234" },
      { label: "Last Known Location", value: "Location A" },
      { label: "Source Systems", value: "CCTNS · ICJS" },
    ],
    priorityFactors: [
      { label: "Cross-case links", weight: 34 },
      { label: "Network connectivity", weight: 27 },
      { label: "Recent activity", weight: 18 },
      { label: "Pattern recurrence", weight: 12 },
    ],
  },
  {
    id: "P-ARJUN",
    type: "person",
    label: "Arjun Kumar",
    subtitle: "Person of interest · 8 associated cases",
    priority: 84,
    priorityBand: "HIGH",
    cases: ["CASE-156", "CASE-203", "CASE-247"],
    relationships: 14,
    recentEvents: 7,
    attributes: [
      { label: "Entity Type", value: "Person" },
      { label: "Registered Phone", value: "XXXXX5678" },
      { label: "Linked Vehicle", value: "TN-XX-1234" },
      { label: "Last Known Location", value: "Location B" },
      { label: "Source Systems", value: "CCTNS" },
    ],
    priorityFactors: [
      { label: "Cross-case links", weight: 30 },
      { label: "Network connectivity", weight: 24 },
      { label: "Recent activity", weight: 16 },
      { label: "Pattern recurrence", weight: 14 },
    ],
  },
  {
    id: "P-KARTHIK",
    type: "person",
    label: "Karthik Raj",
    subtitle: "Associate · 3 associated cases",
    priority: 62,
    priorityBand: "MEDIUM",
    cases: ["CASE-101", "CASE-247"],
    relationships: 9,
    recentEvents: 4,
    attributes: [
      { label: "Entity Type", value: "Person" },
      { label: "Registered Phone", value: "XXXXX5678" },
      { label: "Last Known Location", value: "Location C" },
      { label: "Source Systems", value: "ICJS" },
    ],
    priorityFactors: [
      { label: "Network connectivity", weight: 22 },
      { label: "Recent activity", weight: 20 },
      { label: "Cross-case links", weight: 12 },
      { label: "Pattern recurrence", weight: 8 },
    ],
  },
  {
    id: "P-MOHAN",
    type: "person",
    label: "Mohan Das",
    subtitle: "Associate · 2 associated cases",
    priority: 48,
    priorityBand: "MEDIUM",
    cases: ["CASE-156"],
    relationships: 6,
    recentEvents: 3,
    attributes: [
      { label: "Entity Type", value: "Person" },
      { label: "Linked Account", value: "AC-XXXX-204" },
      { label: "Source Systems", value: "CCTNS" },
    ],
    priorityFactors: [
      { label: "Recent activity", weight: 18 },
      { label: "Network connectivity", weight: 16 },
      { label: "Cross-case links", weight: 8 },
      { label: "Pattern recurrence", weight: 6 },
    ],
  },
  {
    id: "P-PRIYA",
    type: "person",
    label: "Priya Shah",
    subtitle: "Witness record · 1 associated case",
    priority: 31,
    priorityBand: "LOW",
    cases: ["CASE-247"],
    relationships: 4,
    recentEvents: 2,
    attributes: [
      { label: "Entity Type", value: "Person" },
      { label: "Last Known Location", value: "Location C" },
      { label: "Source Systems", value: "ICJS" },
    ],
    priorityFactors: [
      { label: "Recent activity", weight: 12 },
      { label: "Network connectivity", weight: 10 },
      { label: "Cross-case links", weight: 5 },
      { label: "Pattern recurrence", weight: 4 },
    ],
  },
  {
    id: "PH-1234",
    type: "phone",
    label: "XXXXX1234",
    subtitle: "Subscriber record · CDR available",
    cases: ["CASE-101", "CASE-203"],
    relationships: 5,
    attributes: [
      { label: "Entity Type", value: "Phone" },
      { label: "Source", value: "CDR-1023" },
    ],
  },
  {
    id: "PH-5678",
    type: "phone",
    label: "XXXXX5678",
    subtitle: "Subscriber record · CDR available",
    cases: ["CASE-156", "CASE-247"],
    relationships: 4,
    attributes: [
      { label: "Entity Type", value: "Phone" },
      { label: "Source", value: "CDR-1188" },
    ],
  },
  {
    id: "V-1234",
    type: "vehicle",
    label: "TN-XX-1234",
    subtitle: "Vehicle record · shared usage detected",
    cases: ["CASE-101", "CASE-203"],
    relationships: 6,
    attributes: [
      { label: "Entity Type", value: "Vehicle" },
      { label: "Source", value: "Vehicle-445" },
    ],
  },
  {
    id: "V-5678",
    type: "vehicle",
    label: "TN-XX-5678",
    subtitle: "Vehicle record",
    cases: ["CASE-247"],
    relationships: 3,
    attributes: [
      { label: "Entity Type", value: "Vehicle" },
      { label: "Source", value: "Vehicle-512" },
    ],
  },
  {
    id: "AC-102",
    type: "account",
    label: "AC-XXXX-102",
    subtitle: "Financial record · 3 flagged transfers",
    cases: ["CASE-156"],
    relationships: 4,
    attributes: [
      { label: "Entity Type", value: "Bank Account" },
      { label: "Source", value: "FIN-3301" },
    ],
  },
  {
    id: "AC-204",
    type: "account",
    label: "AC-XXXX-204",
    subtitle: "Financial record · 1 flagged transfer",
    cases: ["CASE-156", "CASE-203"],
    relationships: 3,
    attributes: [
      { label: "Entity Type", value: "Bank Account" },
      { label: "Source", value: "FIN-3345" },
    ],
  },
  {
    id: "L-A",
    type: "location",
    label: "Location A",
    subtitle: "Geo record · repeated presence",
    cases: ["CASE-101", "CASE-203"],
    relationships: 5,
    attributes: [{ label: "Entity Type", value: "Location" }],
  },
  {
    id: "L-B",
    type: "location",
    label: "Location B",
    subtitle: "Geo record",
    cases: ["CASE-156"],
    relationships: 3,
    attributes: [{ label: "Entity Type", value: "Location" }],
  },
  {
    id: "L-C",
    type: "location",
    label: "Location C",
    subtitle: "Geo record",
    cases: ["CASE-247"],
    relationships: 3,
    attributes: [{ label: "Entity Type", value: "Location" }],
  },
  {
    id: "CASE-101",
    type: "case",
    label: "Case 101",
    subtitle: "Property offence · Active",
    relationships: 6,
    attributes: [
      { label: "Entity Type", value: "Case" },
      { label: "Status", value: "Active" },
      { label: "Registered", value: "10 Jan 2026" },
    ],
  },
  {
    id: "CASE-156",
    type: "case",
    label: "Case 156",
    subtitle: "Financial offence · Active",
    relationships: 7,
    attributes: [
      { label: "Entity Type", value: "Case" },
      { label: "Status", value: "Active" },
      { label: "Registered", value: "18 Jan 2026" },
    ],
  },
  {
    id: "CASE-203",
    type: "case",
    label: "Case 203",
    subtitle: "Organised activity · Active",
    relationships: 9,
    attributes: [
      { label: "Entity Type", value: "Case" },
      { label: "Status", value: "Active" },
      { label: "Registered", value: "22 Jan 2026" },
    ],
  },
  {
    id: "CASE-247",
    type: "case",
    label: "Case 247",
    subtitle: "Vehicle offence · Under review",
    relationships: 5,
    attributes: [
      { label: "Entity Type", value: "Case" },
      { label: "Status", value: "Under review" },
      { label: "Registered", value: "02 Feb 2026" },
    ],
  },
];

export const relations: Relation[] = [
  {
    source: "P-RAVI",
    target: "PH-1234",
    type: "communication",
    label: "Registered subscriber",
    confidence: 96,
    sourceRecord: "CDR-1023",
  },
  {
    source: "P-ARJUN",
    target: "PH-5678",
    type: "communication",
    label: "Registered subscriber",
    confidence: 93,
    sourceRecord: "CDR-1188",
  },
  {
    source: "PH-1234",
    target: "PH-5678",
    type: "communication",
    label: "14 calls in 30 days",
    confidence: 88,
    sourceRecord: "CDR-1023",
  },
  {
    source: "P-RAVI",
    target: "V-1234",
    type: "vehicle",
    label: "Vehicle usage recorded",
    confidence: 87,
    sourceRecord: "Vehicle-445",
  },
  {
    source: "P-ARJUN",
    target: "V-1234",
    type: "vehicle",
    label: "Vehicle usage recorded",
    confidence: 82,
    sourceRecord: "Vehicle-445",
  },
  {
    source: "P-KARTHIK",
    target: "PH-5678",
    type: "communication",
    label: "Contact record",
    confidence: 74,
    sourceRecord: "CDR-1188",
  },
  {
    source: "P-KARTHIK",
    target: "V-5678",
    type: "vehicle",
    label: "Vehicle usage recorded",
    confidence: 70,
    sourceRecord: "Vehicle-512",
  },
  {
    source: "P-MOHAN",
    target: "AC-204",
    type: "financial",
    label: "Account holder",
    confidence: 90,
    sourceRecord: "FIN-3345",
  },
  {
    source: "AC-102",
    target: "AC-204",
    type: "financial",
    label: "3 transfers detected",
    confidence: 79,
    sourceRecord: "FIN-3301",
  },
  {
    source: "P-RAVI",
    target: "AC-102",
    type: "financial",
    label: "Transaction reference",
    confidence: 68,
    sourceRecord: "FIN-3301",
  },
  {
    source: "P-RAVI",
    target: "L-A",
    type: "location",
    label: "Presence recorded 4 times",
    confidence: 85,
    sourceRecord: "GEO-771",
  },
  {
    source: "P-ARJUN",
    target: "L-B",
    type: "location",
    label: "Presence recorded 2 times",
    confidence: 72,
    sourceRecord: "GEO-802",
  },
  {
    source: "V-1234",
    target: "L-A",
    type: "location",
    label: "Vehicle sighting",
    confidence: 80,
    sourceRecord: "GEO-771",
  },
  {
    source: "P-PRIYA",
    target: "L-C",
    type: "location",
    label: "Statement location",
    confidence: 65,
    sourceRecord: "GEO-844",
  },
  {
    source: "P-RAVI",
    target: "CASE-101",
    type: "case",
    label: "Named in record",
    confidence: 99,
    sourceRecord: "Case-101",
  },
  {
    source: "P-RAVI",
    target: "CASE-203",
    type: "case",
    label: "Named in record",
    confidence: 99,
    sourceRecord: "Case-203",
  },
  {
    source: "P-ARJUN",
    target: "CASE-203",
    type: "case",
    label: "Named in record",
    confidence: 99,
    sourceRecord: "Case-203",
  },
  {
    source: "P-ARJUN",
    target: "CASE-247",
    type: "case",
    label: "Named in record",
    confidence: 99,
    sourceRecord: "Case-247",
  },
  {
    source: "P-KARTHIK",
    target: "CASE-101",
    type: "case",
    label: "Named in record",
    confidence: 99,
    sourceRecord: "Case-101",
  },
  {
    source: "P-MOHAN",
    target: "CASE-156",
    type: "case",
    label: "Named in record",
    confidence: 99,
    sourceRecord: "Case-156",
  },
  {
    source: "P-PRIYA",
    target: "CASE-247",
    type: "case",
    label: "Named in record",
    confidence: 99,
    sourceRecord: "Case-247",
  },
  {
    source: "V-1234",
    target: "CASE-203",
    type: "case",
    label: "Evidence item",
    confidence: 92,
    sourceRecord: "Vehicle-445",
  },
  {
    source: "AC-204",
    target: "CASE-156",
    type: "case",
    label: "Evidence item",
    confidence: 91,
    sourceRecord: "FIN-3345",
  },
  {
    source: "L-A",
    target: "CASE-101",
    type: "case",
    label: "Scene reference",
    confidence: 88,
    sourceRecord: "GEO-771",
  },
];

export const timeline: TimelineEvent[] = [
  {
    id: "T1",
    date: "2026-01-10",
    day: "JAN 10",
    category: "communication",
    title: "Ravi Kumar contacts Karthik Raj",
    detail: "14-minute call recorded between XXXXX1234 and XXXXX5678.",
    entities: ["P-RAVI", "P-KARTHIK"],
    record: "CDR-1023",
  },
  {
    id: "T2",
    date: "2026-01-15",
    day: "JAN 15",
    category: "location",
    title: "Karthik Raj appears at Location A",
    detail: "Presence recorded within 900m of Case 101 scene reference.",
    entities: ["P-KARTHIK", "L-A"],
    record: "GEO-771",
  },
  {
    id: "T3",
    date: "2026-01-18",
    day: "JAN 18",
    category: "financial",
    title: "Financial transaction detected",
    detail: "Transfer between AC-XXXX-102 and AC-XXXX-204 flagged for review.",
    entities: ["AC-102", "AC-204"],
    record: "FIN-3301",
  },
  {
    id: "T4",
    date: "2026-01-20",
    day: "JAN 20",
    category: "vehicle",
    title: "Vehicle TN-XX-1234 sighted at Location A",
    detail: "Shared vehicle usage between two separate person records.",
    entities: ["V-1234", "L-A"],
    record: "Vehicle-445",
  },
  {
    id: "T5",
    date: "2026-01-22",
    day: "JAN 22",
    category: "case",
    title: "Case 203 registered",
    detail: "Case registered in source system with two named person records.",
    entities: ["CASE-203", "P-RAVI", "P-ARJUN"],
    record: "Case-203",
  },
  {
    id: "T6",
    date: "2026-01-25",
    day: "JAN 25",
    category: "communication",
    title: "Ravi Kumar contacts Karthik Raj again",
    detail: "Third contact within a 15-day window following case registration.",
    entities: ["P-RAVI", "P-KARTHIK"],
    record: "CDR-1023",
  },
  {
    id: "T7",
    date: "2026-02-02",
    day: "FEB 02",
    category: "case",
    title: "Case 247 registered",
    detail: "Vehicle offence record naming Arjun Kumar and Priya Shah.",
    entities: ["CASE-247", "P-ARJUN"],
    record: "Case-247",
  },
  {
    id: "T8",
    date: "2026-02-06",
    day: "FEB 06",
    category: "financial",
    title: "Second transfer detected",
    detail: "Repeat transfer pattern involving AC-XXXX-204.",
    entities: ["AC-204", "P-MOHAN"],
    record: "FIN-3345",
  },
];

export const alerts: Alert[] = [
  {
    id: "AL-1",
    severity: "critical",
    title: "Potential cross-case relationship detected",
    explanation: "Shared vehicle record links person entities appearing in Case 101 and Case 203.",
    case: "CASE-203",
    timestamp: "12 min ago",
    confidence: 84,
    entities: ["P-RAVI", "P-ARJUN", "V-1234"],
  },
  {
    id: "AL-2",
    severity: "high",
    title: "New high-connectivity entity identified",
    explanation: "Phone XXXXX5678 now connects four separate person records across three cases.",
    case: "CASE-156",
    timestamp: "48 min ago",
    confidence: 78,
    entities: ["PH-5678"],
  },
  {
    id: "AL-3",
    severity: "high",
    title: "Unusual transaction pattern detected",
    explanation:
      "Repeated transfers between AC-XXXX-102 and AC-XXXX-204 outside the historical baseline.",
    case: "CASE-156",
    timestamp: "3 hrs ago",
    confidence: 76,
    entities: ["AC-102", "AC-204"],
  },
  {
    id: "AL-4",
    severity: "medium",
    title: "Emerging network cluster detected",
    explanation: "A four-entity cluster formed around Location A within the last 14 days.",
    case: "CASE-101",
    timestamp: "6 hrs ago",
    confidence: 69,
    entities: ["L-A", "P-KARTHIK"],
  },
  {
    id: "AL-5",
    severity: "medium",
    title: "Entity match requires review",
    explanation: "Two person records share phone and vehicle attributes with high name similarity.",
    case: "CASE-203",
    timestamp: "9 hrs ago",
    confidence: 92,
    entities: ["P-RAVI"],
  },
  {
    id: "AL-6",
    severity: "info",
    title: "Investigation evidence updated",
    explanation: "New CDR extract ingested from the connected source system for Case 247.",
    case: "CASE-247",
    timestamp: "1 day ago",
    confidence: 100,
    entities: ["CASE-247"],
  },
];

export const crossCaseLinks: CrossCaseLink[] = [
  {
    cases: ["CASE-101", "CASE-156", "CASE-203"],
    shared: [
      { type: "Shared Person", value: "Ravi Kumar" },
      { type: "Shared Phone", value: "XXXXX1234" },
      { type: "Shared Vehicle", value: "TN-XX-1234" },
      { type: "Shared Location", value: "Location A" },
      { type: "Shared Associate", value: "Karthik Raj" },
    ],
    path: ["Case 101", "Karthik Raj", "Case 156", "Ravi Kumar", "Case 203"],
    confidence: 84,
    evidence: ["CDR-1023", "Vehicle-445", "GEO-771", "Case-203"],
    summary:
      "Three investigation records share intermediary entities that do not appear connected inside any single case file.",
  },
  {
    cases: ["CASE-203", "CASE-247"],
    shared: [
      { type: "Shared Person", value: "Arjun Kumar" },
      { type: "Shared Vehicle", value: "TN-XX-1234" },
    ],
    path: ["Case 203", "Arjun Kumar", "Case 247"],
    confidence: 71,
    evidence: ["Vehicle-445", "Case-247"],
    summary:
      "A person record named in Case 203 also appears in a later vehicle offence record with an overlapping vehicle attribute.",
  },
];

export const patterns: PatternInsight[] = [
  {
    id: "PT-1",
    category: "Indirect Relationships",
    title: "Indirect relationship detected",
    entities: ["Ravi Kumar", "Arjun Kumar"],
    path: ["Ravi Kumar", "Karthik Raj", "Vehicle TN-XX-1234", "Arjun Kumar"],
    confidence: 84,
    why: "This relationship connects entities appearing in separate investigation records.",
    evidence: ["CDR-1023", "Vehicle-445", "Case-203"],
  },
  {
    id: "PT-2",
    category: "Emerging Network Clusters",
    title: "Four-entity cluster forming around Location A",
    entities: ["Ravi Kumar", "Karthik Raj", "TN-XX-1234", "Location A"],
    confidence: 69,
    why: "Cluster density around a single location increased sharply within 14 days.",
    evidence: ["GEO-771", "Vehicle-445"],
  },
  {
    id: "PT-3",
    category: "Repeated Entity Associations",
    title: "Recurring contact pattern between two person records",
    entities: ["Ravi Kumar", "Karthik Raj"],
    confidence: 77,
    why: "Three contacts recorded in a 15-day window, clustered around case registration.",
    evidence: ["CDR-1023"],
  },
  {
    id: "PT-4",
    category: "Unusual Activity Patterns",
    title: "Transaction pattern outside historical baseline",
    entities: ["AC-XXXX-102", "AC-XXXX-204"],
    confidence: 76,
    why: "Transfer frequency and timing deviate from the account's prior 90-day behaviour.",
    evidence: ["FIN-3301", "FIN-3345"],
  },
  {
    id: "PT-5",
    category: "Cross-Case Similarities",
    title: "Similar entity composition across Case 156 and Case 203",
    entities: ["Case 156", "Case 203"],
    confidence: 66,
    why: "Both records share account, phone and person attribute overlaps.",
    evidence: ["FIN-3345", "CDR-1023", "Case-203"],
  },
];

export const evidence: EvidenceItem[] = [
  {
    id: "EV-1",
    insight: "Potential association between Ravi Kumar and Arjun Kumar",
    sources: [
      { id: "CDR-1023", type: "Call detail record", timestamp: "10 Jan 2026, 21:14" },
      { id: "Vehicle-445", type: "Vehicle record", timestamp: "20 Jan 2026, 08:02" },
      { id: "Case-203", type: "Case record", timestamp: "22 Jan 2026, 11:30" },
    ],
    analysis: "Temporal + relational correlation across three source systems",
    relationship: "Indirect association via shared vehicle and intermediary contact",
    status: "Pending Analyst Review",
    audit: [
      { stage: "Detected", actor: "CIRAN Intelligence Layer", timestamp: "22 Jan 2026, 11:42" },
      {
        stage: "Reviewed",
        actor: "Insp. S. Menon",
        timestamp: "22 Jan 2026, 16:05",
        note: "Vehicle ownership chain being verified with source system.",
      },
      { stage: "Pending decision", actor: "—", timestamp: "Awaiting analyst action" },
    ],
  },
  {
    id: "EV-2",
    insight: "Unusual transaction pattern involving AC-XXXX-102",
    sources: [
      { id: "FIN-3301", type: "Financial record", timestamp: "18 Jan 2026, 13:20" },
      { id: "FIN-3345", type: "Financial record", timestamp: "06 Feb 2026, 10:11" },
    ],
    analysis: "Behavioural deviation from 90-day account baseline",
    relationship: "Repeated transfers between two linked accounts",
    status: "Accepted",
    audit: [
      { stage: "Detected", actor: "CIRAN Intelligence Layer", timestamp: "06 Feb 2026, 10:18" },
      { stage: "Reviewed", actor: "SI. R. Devi", timestamp: "06 Feb 2026, 12:40" },
      {
        stage: "Accepted",
        actor: "SI. R. Devi",
        timestamp: "06 Feb 2026, 12:44",
        note: "Added to Case 156 investigation notes.",
      },
    ],
  },
  {
    id: "EV-3",
    insight: "Possible entity match between two person records",
    sources: [
      { id: "CDR-1023", type: "Call detail record", timestamp: "10 Jan 2026, 21:14" },
      { id: "Vehicle-445", type: "Vehicle record", timestamp: "20 Jan 2026, 08:02" },
    ],
    analysis: "Attribute overlap: phone, vehicle, name similarity",
    relationship: "Requires review — potential duplicate record",
    status: "Pending Analyst Review",
    audit: [
      { stage: "Detected", actor: "CIRAN Intelligence Layer", timestamp: "23 Jan 2026, 09:02" },
      { stage: "Pending review", actor: "—", timestamp: "Awaiting analyst action" },
    ],
  },
];

export const activity = [
  {
    investigation: "CASE-203",
    action: "Network expanded around Ravi Kumar",
    officer: "Insp. S. Menon",
    timestamp: "12 min ago",
  },
  {
    investigation: "CASE-156",
    action: "Financial pattern accepted as investigative signal",
    officer: "SI. R. Devi",
    timestamp: "1 hr ago",
  },
  {
    investigation: "CASE-101",
    action: "Evidence record CDR-1023 reviewed",
    officer: "Insp. S. Menon",
    timestamp: "3 hrs ago",
  },
  {
    investigation: "CASE-247",
    action: "New source extract ingested from connected system",
    officer: "System",
    timestamp: "6 hrs ago",
  },
  {
    investigation: "CASE-203",
    action: "Entity match flagged for analyst review",
    officer: "CIRAN",
    timestamp: "9 hrs ago",
  },
];

export const trend = [
  { month: "Sep", relationships: 18, patterns: 4 },
  { month: "Oct", relationships: 26, patterns: 7 },
  { month: "Nov", relationships: 31, patterns: 9 },
  { month: "Dec", relationships: 44, patterns: 12 },
  { month: "Jan", relationships: 58, patterns: 17 },
  { month: "Feb", relationships: 73, patterns: 23 },
];

export const entityResolution = {
  recordA: {
    title: "Record A · CCTNS",
    name: "Ravi Kumar",
    fields: [
      { label: "Phone", value: "XXXXX1234" },
      { label: "Vehicle", value: "TN-XX-1234" },
      { label: "Case", value: "Case 101" },
    ],
  },
  recordB: {
    title: "Record B · ICJS",
    name: "R. Kumar",
    fields: [
      { label: "Phone", value: "XXXXX1234" },
      { label: "Vehicle", value: "TN-XX-1234" },
      { label: "Case", value: "Case 203" },
    ],
  },
  confidence: 92,
  matching: ["Phone", "Vehicle", "Name similarity"],
  nonMatching: ["Address field absent in Record B"],
};

export const nodePositions: Record<string, { x: number; y: number }> = {
  "P-RAVI": { x: 300, y: 300 },
  "P-ARJUN": { x: 640, y: 300 },
  "P-KARTHIK": { x: 300, y: 520 },
  "P-MOHAN": { x: 150, y: 130 },
  "P-PRIYA": { x: 800, y: 520 },
  "PH-1234": { x: 180, y: 380 },
  "PH-5678": { x: 470, y: 470 },
  "V-1234": { x: 470, y: 240 },
  "V-5678": { x: 200, y: 620 },
  "AC-102": { x: 130, y: 240 },
  "AC-204": { x: 60, y: 380 },
  "L-A": { x: 470, y: 120 },
  "L-B": { x: 760, y: 180 },
  "L-C": { x: 820, y: 420 },
  "CASE-101": { x: 620, y: 60 },
  "CASE-156": { x: 60, y: 60 },
  "CASE-203": { x: 800, y: 300 },
  "CASE-247": { x: 640, y: 610 },
};

export const entityTypeLabel: Record<EntityType, string> = {
  person: "Person",
  phone: "Phone",
  vehicle: "Vehicle",
  account: "Bank Account",
  location: "Location",
  case: "Case",
};

export const relationTypeLabel: Record<RelationType, string> = {
  communication: "Communication",
  financial: "Financial transaction",
  vehicle: "Shared vehicle",
  location: "Shared location",
  case: "Case association",
};
