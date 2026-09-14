import { createFileRoute } from "@tanstack/react-router";
import { useState, useRef, useEffect } from "react";
import { Bot, Send, Sparkles, AlertTriangle } from "lucide-react";
import { AppShell } from "@/components/ciran/app-shell";
import { PageHeader } from "@/components/ciran/ui-kit";

export const Route = createFileRoute("/copilot")({
  head: () => ({
    meta: [{ title: "Investigator Copilot — CIRAN" }],
  }),
  component: CopilotPage,
});

function CopilotPage() {
  const [query, setQuery] = useState("");
  const [messages, setMessages] = useState<{ role: "user" | "copilot"; content: any }[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const scrollRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [messages]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!query.trim()) return;

    const userQuery = query.trim();
    setMessages((prev) => [...prev, { role: "user", content: userQuery }]);
    setQuery("");
    setIsLoading(true);

    try {
      const history = messages.map(m => ({
        role: m.role === "copilot" ? "assistant" : "user",
        content: m.role === "copilot" ? (m.content.summary || "") : m.content
      }));

      const res = await fetch("/api/copilot/query", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query: userQuery, conversation_history: history }),
      });
      const data = await res.json();
      setMessages((prev) => [...prev, { role: "copilot", content: data }]);
    } catch (err) {
      setMessages((prev) => [
        ...prev,
        { role: "copilot", content: { summary: "I couldn't process that query. Please try again.", chips: [] } },
      ]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <AppShell>
      <PageHeader
        title="Investigator Copilot"
        subtitle="Natural language queries across the unified intelligence graph."
      />

      <div className="flex flex-col h-[calc(100vh-180px)] max-h-[800px] border border-border rounded-lg bg-surface overflow-hidden">
        <div ref={scrollRef} className="flex-1 overflow-y-auto p-6 space-y-6">
          {messages.length === 0 ? (
            <div className="flex flex-col items-center justify-center h-full text-center text-muted-foreground">
              <Bot className="size-12 mb-4 text-primary/40" />
              <p className="text-sm font-medium text-foreground mb-2">
                How can I assist your investigation?
              </p>
              <p className="text-xs max-w-sm">
                Try asking: "Show all connections between Ravi and Case 203" or "What changed in
                this network during the last 30 days?"
              </p>
            </div>
          ) : (
            messages.map((m, i) => (
              <div
                key={i}
                className={`flex ${m.role === "user" ? "justify-end" : "justify-start"}`}
              >
                {m.role === "copilot" && (
                  <div className="flex-shrink-0 mr-3 mt-1">
                    <div className="flex size-8 items-center justify-center rounded-full bg-primary/10 border border-primary/20 text-primary">
                      <Sparkles className="size-4" />
                    </div>
                  </div>
                )}

                <div
                  className={
                    m.role === "user"
                      ? "max-w-[85%] rounded-lg p-3 bg-primary text-primary-foreground ml-auto"
                      : "w-full rounded-lg p-5 bg-surface/40 border border-border/50 shadow-sm"
                  }
                >
                  {m.role === "user" ? (
                    <p className="text-sm">{m.content}</p>
                  ) : (
                    <div className="space-y-4">
                      {m.content.summary && (
                        <p className="text-sm text-foreground leading-relaxed">{m.content.summary}</p>
                      )}

                      {m.content.facts && m.content.facts.length > 0 && (
                        <div className="bg-surface-2 p-3 rounded border border-border/50">
                          <div className="flex items-center justify-between mb-2">
                            <p className="text-[10px] font-semibold uppercase tracking-wider text-muted-foreground">
                              Facts
                            </p>
                            {m.content.intent && (
                              <span className="text-[10px] font-mono bg-primary/10 text-primary px-1.5 py-0.5 rounded">
                                Intent: {m.content.intent}
                              </span>
                            )}
                          </div>
                          <ul className="list-disc list-outside ml-4 space-y-1">
                            {m.content.facts.map((fact: string, j: number) => (
                              <li key={j} className="text-xs text-foreground">
                                {fact}
                              </li>
                            ))}
                          </ul>
                        </div>
                      )}

                      {m.content.derived_findings && m.content.derived_findings.length > 0 && (
                        <div className="bg-primary/5 p-3 rounded border border-primary/20">
                          <p className="text-[10px] font-semibold uppercase tracking-wider text-primary mb-2 flex items-center gap-1">
                            <Sparkles className="size-3" /> Derived Findings
                          </p>
                          <ul className="list-disc list-outside ml-4 space-y-1">
                            {m.content.derived_findings.map((finding: string, j: number) => (
                              <li key={j} className="text-xs text-foreground">
                                {finding}
                              </li>
                            ))}
                          </ul>
                        </div>
                      )}

                      {(m.content.caution || (m.content.limitations && m.content.limitations.length > 0)) && (
                        <div className="flex flex-col gap-2 bg-background p-3 rounded border border-border-strong">
                          {m.content.caution && (
                            <div className="flex items-start gap-2">
                              <AlertTriangle className="size-4 text-high shrink-0 mt-0.5" />
                              <p className="text-xs text-muted-foreground">Automated analysis based on CIRAN intelligence records. Verify all source records.</p>
                            </div>
                          )}
                          {m.content.limitations && m.content.limitations.length > 0 && (
                            <ul className="list-disc list-outside ml-6 space-y-1">
                              {m.content.limitations.map((lim: string, j: number) => (
                                <li key={j} className="text-xs text-muted-foreground">
                                  {lim}
                                </li>
                              ))}
                            </ul>
                          )}
                        </div>
                      )}

                      {m.content.path && (
                        <div className="bg-surface p-4 rounded border border-border/50">
                          <p className="text-[10px] font-semibold uppercase tracking-wider text-muted-foreground mb-3">
                            Connection Path
                          </p>
                          <div className="flex flex-wrap items-center gap-2">
                            {m.content.path.map((node: string, j: number) => (
                              <div key={j} className="flex items-center gap-2 text-xs">
                                <span className="px-1.5 py-0.5 bg-surface-2 border border-border rounded text-foreground">
                                  {node}
                                </span>
                                {j < m.content.path.length - 1 && (
                                  <span className="text-muted-foreground">→</span>
                                )}
                              </div>
                            ))}
                          </div>
                        </div>
                      )}

                      {m.content.timeline && (
                        <div className="bg-surface p-4 rounded border border-border/50">
                          <p className="text-[10px] font-semibold uppercase tracking-wider text-muted-foreground mb-3">
                            Event Timeline
                          </p>
                          <ul className="space-y-2">
                            {m.content.timeline.map((event: any, j: number) => (
                              <li key={j} className="flex gap-3 text-xs">
                                <span className="font-mono text-primary font-medium">
                                  {event.day}
                                </span>
                                <span className="text-foreground">{event.title}</span>
                              </li>
                            ))}
                          </ul>
                        </div>
                      )}

                      {m.content.evidence && (
                        <div className="flex flex-col gap-2 pt-2 border-t border-border mt-2">
                          <div className="flex flex-wrap items-center gap-2">
                            <span className="text-xs text-muted-foreground py-0.5">Sources:</span>
                            {m.content.evidence.map((ev: string, j: number) => (
                              <span
                                key={j}
                                className="text-[10px] font-mono px-1.5 py-0.5 rounded bg-background border border-border-strong text-muted-foreground"
                              >
                                {ev}
                              </span>
                            ))}
                          </div>
                          {m.content.source_count !== undefined && (
                            <p className="text-[10px] text-muted-foreground">
                              Aggregated from {m.content.source_count} explicit source records.
                            </p>
                          )}
                        </div>
                      )}
                    </div>
                  )}
                </div>
              </div>
            ))
          )}
          {isLoading && (
            <div className="flex justify-start">
              <div className="flex-shrink-0 mr-3 mt-1">
                <div className="flex size-8 items-center justify-center rounded-full bg-primary/10 border border-primary/20 text-primary">
                  <Sparkles className="size-4 animate-pulse" />
                </div>
              </div>
              <div className="bg-surface-2 border border-border rounded-lg p-4 flex items-center gap-2">
                <div className="flex gap-1">
                  <span
                    className="size-1.5 rounded-full bg-muted-foreground animate-bounce"
                    style={{ animationDelay: "0ms" }}
                  />
                  <span
                    className="size-1.5 rounded-full bg-muted-foreground animate-bounce"
                    style={{ animationDelay: "150ms" }}
                  />
                  <span
                    className="size-1.5 rounded-full bg-muted-foreground animate-bounce"
                    style={{ animationDelay: "300ms" }}
                  />
                </div>
              </div>
            </div>
          )}
        </div>

        <div className="p-4 border-t border-border bg-surface-2">
          <form onSubmit={handleSubmit} className="relative">
            <input
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="Ask Copilot a question about this investigation..."
              className="w-full bg-input border border-border rounded-md pl-4 pr-12 py-3 text-sm focus:outline-none focus:border-primary/50 text-foreground placeholder:text-muted-foreground"
              disabled={isLoading}
            />
            <button
              type="submit"
              disabled={isLoading || !query.trim()}
              className="absolute right-2 top-1/2 -translate-y-1/2 p-1.5 rounded text-primary hover:bg-primary/10 disabled:opacity-50 disabled:hover:bg-transparent"
            >
              <Send className="size-4" />
            </button>
          </form>
        </div>
      </div>
    </AppShell>
  );
}
