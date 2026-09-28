import { createFileRoute } from "@tanstack/react-router";
import { AppShell } from "@/components/ciran/app-shell";
import { PageHeader, Panel, ActionButton } from "@/components/ciran/ui-kit";
import { TimelineView } from "@/components/ciran/timeline-view";
import { useQuery } from "@tanstack/react-query";
import { useState, useMemo } from "react";
import { Search, X } from "lucide-react";
import { getTimeline } from "@/lib/ciran-service";
import { QueryLoader } from "@/components/ciran/query-loader";

export const Route = createFileRoute("/timeline")({
  head: () => ({ meta: [{ title: "Global Timeline — CIRAN" }] }),
  component: GlobalTimelinePage,
});

function GlobalTimelinePage() {
  const query = useQuery({
    queryKey: ["global-timeline"],
    queryFn: () => getTimeline(),
  });

  const events = query.data;

  const [searchQuery, setSearchQuery] = useState("");
  const [categoryFilter, setCategoryFilter] = useState("");
  const [entityFilter, setEntityFilter] = useState("");
  const [fromDate, setFromDate] = useState("");
  const [toDate, setToDate] = useState("");

  const categories = useMemo(() => {
    if (!events) return [];
    return Array.from(new Set(events.map((e) => e.category))).sort();
  }, [events]);

  const entities = useMemo(() => {
    if (!events) return [];
    return Array.from(new Set(events.flatMap((e) => e.entities))).sort();
  }, [events]);

  const filteredEvents = useMemo(() => {
    if (!events) return [];
    return events.filter((event) => {
      if (searchQuery) {
        const q = searchQuery.toLowerCase().trim();
        if (
          !event.title.toLowerCase().includes(q) &&
          !event.detail.toLowerCase().includes(q) &&
          !event.category.toLowerCase().includes(q) &&
          !event.record.toLowerCase().includes(q) &&
          !event.entities.some((e) => e.toLowerCase().includes(q))
        ) {
          return false;
        }
      }

      if (categoryFilter && event.category !== categoryFilter) {
        return false;
      }

      if (entityFilter && !event.entities.includes(entityFilter)) {
        return false;
      }

      if (fromDate || toDate) {
        const eventTime = new Date(event.date).getTime();
        if (fromDate) {
          const fromTime = new Date(fromDate).getTime();
          if (eventTime < fromTime) return false;
        }
        if (toDate) {
          const toDateObj = new Date(toDate);
          toDateObj.setHours(23, 59, 59, 999);
          if (eventTime > toDateObj.getTime()) return false;
        }
      }

      return true;
    });
  }, [events, searchQuery, categoryFilter, entityFilter, fromDate, toDate]);

  const hasFilters = searchQuery || categoryFilter || entityFilter || fromDate || toDate;

  const clearFilters = () => {
    setSearchQuery("");
    setCategoryFilter("");
    setEntityFilter("");
    setFromDate("");
    setToDate("");
  };

  return (
    <AppShell>
      <PageHeader
        title="Global Temporal Analysis"
        subtitle="Chronological sequence of connected events across all investigations."
      />

      <Panel className="mb-4">
        <div className="flex flex-col gap-4 p-4 lg:flex-row lg:items-end">
          <div className="flex-1 space-y-1.5">
            <label htmlFor="search" className="text-xs font-medium text-foreground">
              Search
            </label>
            <div className="relative">
              <Search className="absolute left-2.5 top-2.5 size-4 text-muted-foreground" />
              <input
                id="search"
                type="text"
                placeholder="Search events, entities, sources..."
                className="w-full rounded-md border border-input bg-background pl-9 pr-3 py-2 text-sm placeholder:text-muted-foreground focus:outline-none focus:ring-1 focus:ring-primary"
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
              />
            </div>
          </div>

          <div className="w-full lg:w-48 space-y-1.5">
            <label htmlFor="category" className="text-xs font-medium text-foreground">
              Category
            </label>
            <select
              id="category"
              className="w-full rounded-md border border-input bg-background px-3 py-2 text-sm focus:outline-none focus:ring-1 focus:ring-primary"
              value={categoryFilter}
              onChange={(e) => setCategoryFilter(e.target.value)}
            >
              <option value="">All Categories</option>
              {categories.map((c) => (
                <option key={c} value={c}>
                  {c}
                </option>
              ))}
            </select>
          </div>

          <div className="w-full lg:w-48 space-y-1.5">
            <label htmlFor="entity" className="text-xs font-medium text-foreground">
              Entity
            </label>
            <select
              id="entity"
              className="w-full rounded-md border border-input bg-background px-3 py-2 text-sm focus:outline-none focus:ring-1 focus:ring-primary"
              value={entityFilter}
              onChange={(e) => setEntityFilter(e.target.value)}
            >
              <option value="">All Entities</option>
              {entities.map((e) => (
                <option key={e} value={e}>
                  {e}
                </option>
              ))}
            </select>
          </div>

          <div className="w-full lg:w-[320px] space-y-1.5">
            <label className="text-xs font-medium text-foreground">Date Range</label>
            <div className="flex items-center gap-2">
              <input
                type="date"
                className="w-full rounded-md border border-input bg-background px-2 py-2 text-sm focus:outline-none focus:ring-1 focus:ring-primary"
                value={fromDate}
                onChange={(e) => setFromDate(e.target.value)}
                aria-label="From date"
              />
              <span className="text-muted-foreground text-xs">-</span>
              <input
                type="date"
                className="w-full rounded-md border border-input bg-background px-2 py-2 text-sm focus:outline-none focus:ring-1 focus:ring-primary"
                value={toDate}
                onChange={(e) => setToDate(e.target.value)}
                aria-label="To date"
              />
            </div>
          </div>

          {hasFilters && (
            <ActionButton variant="ghost" onClick={clearFilters} className="h-9 px-3 shrink-0">
              <X className="mr-1.5 size-4" />
              Clear
            </ActionButton>
          )}
        </div>
      </Panel>

      <Panel title="Timeline Events" bodyClassName="p-4">
        <QueryLoader
          isLoading={query.isLoading}
          error={query.error}
          data={query.data}
          emptyMessage="No intelligence data available."
        >
          {() => (
            <>
              <div className="mb-4 text-sm text-muted-foreground">
                {filteredEvents.length === 0
                  ? "No timeline events match the selected filters."
                  : `Showing ${filteredEvents.length} of ${events?.length || 0} event${events?.length === 1 ? "" : "s"}`}
              </div>
              <TimelineView events={filteredEvents} />
            </>
          )}
        </QueryLoader>
      </Panel>
    </AppShell>
  );
}
