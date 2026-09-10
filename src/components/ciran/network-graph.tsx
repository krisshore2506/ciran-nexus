import { useMemo, useRef, useState } from "react";
import { Minus, Plus, RotateCcw } from "lucide-react";
import { cn } from "@/lib/utils";
import {
  entityTypeLabel,
  nodePositions,
  relationTypeLabel,
  type Entity,
  type EntityType,
  type Relation,
  type RelationType,
} from "@/lib/ciran-data";

const nodeStroke: Record<EntityType, string> = {
  person: "var(--color-node-person)",
  phone: "var(--color-node-phone)",
  vehicle: "var(--color-node-vehicle)",
  account: "var(--color-node-account)",
  location: "var(--color-node-location)",
  case: "var(--color-node-case)",
};

const nodeRadius: Record<EntityType, number> = {
  person: 22,
  case: 20,
  phone: 15,
  vehicle: 15,
  account: 15,
  location: 15,
};

export const entityTypeOrder: EntityType[] = [
  "person",
  "phone",
  "vehicle",
  "account",
  "location",
  "case",
];

export const relationTypeOrder: RelationType[] = [
  "communication",
  "financial",
  "vehicle",
  "location",
  "case",
];

export function NetworkGraph({
  nodes,
  edges,
  selectedId,
  onSelect,
  height = 560,
  compact,
}: {
  nodes: Entity[];
  edges: Relation[];
  selectedId?: string | null;
  onSelect?: (id: string) => void;
  height?: number;
  compact?: boolean;
}) {
  const [zoom, setZoom] = useState(compact ? 0.85 : 1);
  const [pan, setPan] = useState({ x: 0, y: 0 });
  const drag = useRef<{ x: number; y: number; px: number; py: number } | null>(null);

  const connected = useMemo(() => {
    if (!selectedId) return new Set<string>();
    const s = new Set<string>();
    edges.forEach((e) => {
      if (e.source === selectedId) s.add(e.target);
      if (e.target === selectedId) s.add(e.source);
    });
    return s;
  }, [edges, selectedId]);

  const dim = (id: string) => Boolean(selectedId) && id !== selectedId && !connected.has(id);

  return (
    <div className="relative overflow-hidden rounded-md border border-border bg-background grid-backdrop">
      <svg
        width="100%"
        height={height}
        viewBox="0 0 900 700"
        className="cursor-grab active:cursor-grabbing"
        onMouseDown={(e) => {
          drag.current = { x: e.clientX, y: e.clientY, px: pan.x, py: pan.y };
        }}
        onMouseMove={(e) => {
          if (!drag.current) return;
          setPan({
            x: drag.current.px + (e.clientX - drag.current.x),
            y: drag.current.py + (e.clientY - drag.current.y),
          });
        }}
        onMouseUp={() => (drag.current = null)}
        onMouseLeave={() => (drag.current = null)}
      >
        <g transform={`translate(${pan.x} ${pan.y}) scale(${zoom})`}>
          {edges.map((e, i) => {
            const a = nodePositions[e.source];
            const b = nodePositions[e.target];
            if (!a || !b) return null;
            const active = selectedId === e.source || selectedId === e.target;
            return (
              <g key={`${e.source}-${e.target}-${i}`} opacity={selectedId && !active ? 0.15 : 1}>
                <line
                  x1={a.x}
                  y1={a.y}
                  x2={b.x}
                  y2={b.y}
                  stroke={active ? "var(--color-primary)" : "var(--color-border-strong)"}
                  strokeWidth={active ? 2 : 1.2}
                  strokeDasharray={e.type === "financial" ? "5 4" : undefined}
                />
                {active && (
                  <text
                    x={(a.x + b.x) / 2}
                    y={(a.y + b.y) / 2 - 6}
                    textAnchor="middle"
                    fontSize="10"
                    fill="var(--color-muted-foreground)"
                  >
                    {relationTypeLabel[e.type]}
                  </text>
                )}
              </g>
            );
          })}

          {nodes.map((n) => {
            const p = nodePositions[n.id];
            if (!p) return null;
            const r = nodeRadius[n.type];
            const isSelected = selectedId === n.id;
            return (
              <g
                key={n.id}
                transform={`translate(${p.x} ${p.y})`}
                opacity={dim(n.id) ? 0.25 : 1}
                className="cursor-pointer"
                onClick={(ev) => {
                  ev.stopPropagation();
                  onSelect?.(n.id);
                }}
              >
                {isSelected && (
                  <circle r={r + 7} fill="none" stroke="var(--color-primary)" strokeWidth={1.5} />
                )}
                <circle
                  r={r}
                  fill="var(--color-surface)"
                  stroke={nodeStroke[n.type]}
                  strokeWidth={2}
                />
                <circle r={r * 0.38} fill={nodeStroke[n.type]} opacity={0.85} />
                <text
                  y={r + 14}
                  textAnchor="middle"
                  fontSize="11"
                  fill="var(--color-foreground)"
                  fontWeight={n.type === "person" || n.type === "case" ? 600 : 400}
                >
                  {n.label}
                </text>
              </g>
            );
          })}
        </g>
      </svg>

      <div className="absolute top-3 right-3 flex flex-col gap-1 rounded-md border border-border bg-surface/90 p-1">
        <button
          className="rounded p-1.5 text-muted-foreground hover:bg-surface-2 hover:text-foreground"
          onClick={() => setZoom((z) => Math.min(2, z + 0.15))}
          aria-label="Zoom in"
        >
          <Plus className="size-4" />
        </button>
        <button
          className="rounded p-1.5 text-muted-foreground hover:bg-surface-2 hover:text-foreground"
          onClick={() => setZoom((z) => Math.max(0.4, z - 0.15))}
          aria-label="Zoom out"
        >
          <Minus className="size-4" />
        </button>
        <button
          className="rounded p-1.5 text-muted-foreground hover:bg-surface-2 hover:text-foreground"
          onClick={() => {
            setZoom(compact ? 0.85 : 1);
            setPan({ x: 0, y: 0 });
          }}
          aria-label="Reset view"
        >
          <RotateCcw className="size-4" />
        </button>
      </div>

      <div className="absolute bottom-3 left-3 flex flex-wrap gap-2 rounded-md border border-border bg-surface/90 px-3 py-2">
        {entityTypeOrder.map((t) => (
          <span
            key={t}
            className="inline-flex items-center gap-1.5 text-[11px] text-muted-foreground"
          >
            <span className="size-2 rounded-full" style={{ background: nodeStroke[t] }} />
            {entityTypeLabel[t]}
          </span>
        ))}
      </div>
    </div>
  );
}

export function FilterChips<T extends string>({
  options,
  labels,
  active,
  onToggle,
}: {
  options: T[];
  labels: Record<T, string>;
  active: T[];
  onToggle: (v: T) => void;
}) {
  return (
    <div className="flex flex-wrap gap-1.5">
      {options.map((o) => {
        const on = active.includes(o);
        return (
          <button
            key={o}
            onClick={() => onToggle(o)}
            className={cn(
              "rounded-full border px-2.5 py-1 text-xs transition-colors",
              on
                ? "border-primary/60 bg-primary/12 text-foreground"
                : "border-border text-muted-foreground hover:border-border-strong hover:text-foreground",
            )}
          >
            {labels[o]}
          </button>
        );
      })}
    </div>
  );
}
