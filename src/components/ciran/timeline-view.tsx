import { Clock } from "lucide-react";
import { SeverityBadge } from "./ui-kit";
import type { TimelineEvent } from "@/lib/ciran-data";

export function TimelineView({ events }: { events: TimelineEvent[] }) {
  if (events.length === 0) {
    return (
      <div className="py-8 text-center text-sm text-muted-foreground">
        No timeline events found.
      </div>
    );
  }

  return (
    <div className="relative ml-3 space-y-6 border-l border-border pl-6">
      {events.map((event, i) => (
        <div key={event.id} className="relative group">
          <div className="absolute -left-[31px] top-1.5 flex size-4 items-center justify-center rounded-full bg-surface border border-border-strong ring-4 ring-background group-hover:border-primary transition-colors">
            <Clock className="size-2 text-muted-foreground group-hover:text-primary transition-colors" />
          </div>
          <div className="rounded-md border border-transparent p-3 -ml-3 transition-colors hover:bg-surface-2 hover:border-border">
            <div className="flex flex-wrap items-center gap-2 mb-1">
              <span className="font-mono text-xs font-semibold text-primary">{event.day}</span>
              <SeverityBadge severity="info">{event.category}</SeverityBadge>
            </div>
            <p className="text-sm font-semibold text-foreground">{event.title}</p>
            <p className="mt-1.5 max-w-2xl text-sm leading-relaxed text-muted-foreground">
              {event.detail}
            </p>
            <div className="mt-3 flex items-center gap-2 font-mono text-[10px] text-muted-foreground">
              <span className="rounded bg-background border border-border px-1.5 py-0.5">
                Source: {event.record}
              </span>
            </div>
          </div>
        </div>
      ))}
    </div>
  );
}
