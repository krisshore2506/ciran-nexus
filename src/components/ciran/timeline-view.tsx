import { useState } from "react";
import { Clock } from "lucide-react";
import { SeverityBadge } from "./ui-kit";
import type { TimelineEvent } from "@/lib/ciran-data";

export function TimelineView({ events }: { events: TimelineEvent[] }) {
  const [expandedId, setExpandedId] = useState<string | null>(null);

  if (events.length === 0) {
    return (
      <div className="py-8 text-center text-sm text-muted-foreground">
        No timeline events found.
      </div>
    );
  }

  return (
    <div className="relative ml-3 space-y-6 border-l border-border pl-6">
      {events.map((event) => (
        <div key={event.id} className="relative group">
          <div className="absolute -left-[31px] top-1.5 flex size-4 items-center justify-center rounded-full bg-surface border border-border-strong ring-4 ring-background group-hover:border-primary transition-colors">
            <Clock className="size-2 text-muted-foreground group-hover:text-primary transition-colors" />
          </div>
          <div
            className="rounded-md border border-transparent p-3 -ml-3 transition-colors hover:bg-surface-2 hover:border-border cursor-pointer"
            onClick={() => setExpandedId(expandedId === event.id ? null : event.id)}
            role="button"
            tabIndex={0}
            onKeyDown={(e) => {
              if (e.key === "Enter" || e.key === " ") {
                e.preventDefault();
                setExpandedId(expandedId === event.id ? null : event.id);
              }
            }}
          >
            <div className="flex flex-wrap items-center gap-2 mb-1">
              <span className="font-mono text-xs font-semibold text-primary">{event.day}</span>
              <SeverityBadge severity="info">{event.category}</SeverityBadge>
            </div>
            <p className="text-sm font-semibold text-foreground">{event.title}</p>
            <p className="mt-1.5 max-w-2xl text-sm leading-relaxed text-muted-foreground line-clamp-2">
              {event.detail}
            </p>

            {expandedId !== event.id && (
              <div className="mt-3 flex items-center gap-2 font-mono text-[10px] text-muted-foreground">
                <span className="rounded bg-background border border-border px-1.5 py-0.5">
                  Source: {event.record}
                </span>
                {event.entities && event.entities.length > 0 && (
                  <span className="text-muted-foreground/60">
                    +{event.entities.length} entities
                  </span>
                )}
              </div>
            )}

            {expandedId === event.id && (
              <div className="mt-4 pt-4 border-t border-border space-y-4">
                <div>
                  <span className="text-xs font-medium text-muted-foreground block mb-1">
                    Date & Time
                  </span>
                  <span className="font-mono text-xs text-foreground">{event.date}</span>
                </div>

                <div>
                  <span className="text-xs font-medium text-muted-foreground block mb-1">
                    Source Record
                  </span>
                  <span className="font-mono text-xs rounded bg-background border border-border px-1.5 py-0.5 text-muted-foreground">
                    {event.record}
                  </span>
                </div>

                {event.entities && event.entities.length > 0 && (
                  <div>
                    <span className="text-xs font-medium text-muted-foreground block mb-2">
                      Associated Entities
                    </span>
                    <div className="flex flex-wrap gap-1.5">
                      {event.entities.map((e) => (
                        <span
                          key={e}
                          className="inline-flex items-center rounded border border-border bg-surface-2 px-1.5 py-0.5 text-[11px] font-mono text-foreground"
                        >
                          {e}
                        </span>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            )}
          </div>
        </div>
      ))}
    </div>
  );
}
