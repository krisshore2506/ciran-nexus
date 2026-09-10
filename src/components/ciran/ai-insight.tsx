import { Sparkle } from "lucide-react";
import { ActionButton, Confidence, Disclaimer, Tag } from "./ui-kit";

export interface AiInsightProps {
  title: string;
  what: string;
  why: string[];
  evidence: string[];
  confidence: number;
  review: string;
  actions?: { label: string; onClick?: () => void; primary?: boolean }[];
}

export function AiInsight({
  title,
  what,
  why,
  evidence,
  confidence,
  review,
  actions,
}: AiInsightProps) {
  return (
    <div className="space-y-4">
      <div className="flex items-start gap-2">
        <span className="mt-0.5 flex size-6 shrink-0 items-center justify-center rounded border border-primary/40 bg-primary/10">
          <Sparkle className="size-3.5 text-primary" />
        </span>
        <div>
          <p className="text-xs font-semibold tracking-wider text-primary uppercase">AI Insight</p>
          <p className="text-sm font-medium text-foreground">{title}</p>
        </div>
      </div>

      <Block label="What was detected?">
        <p className="text-sm text-foreground">{what}</p>
      </Block>

      <Block label="Why was it detected?">
        <ul className="space-y-1">
          {why.map((w) => (
            <li key={w} className="flex gap-2 text-sm text-foreground">
              <span className="text-success">✓</span>
              {w}
            </li>
          ))}
        </ul>
      </Block>

      <Block label="What evidence supports it?">
        <div className="flex flex-wrap gap-1.5">
          {evidence.map((e) => (
            <Tag key={e}>{e}</Tag>
          ))}
        </div>
      </Block>

      <Block label="How confident is the system?">
        <Confidence value={confidence} />
      </Block>

      <Block label="What should the investigator review?">
        <p className="text-sm text-foreground">{review}</p>
      </Block>

      {actions && (
        <div className="flex flex-wrap gap-2">
          {actions.map((a) => (
            <ActionButton
              key={a.label}
              variant={a.primary ? "primary" : "secondary"}
              onClick={a.onClick}
            >
              {a.label}
            </ActionButton>
          ))}
        </div>
      )}

      <Disclaimer>
        AI output is an investigative signal derived from connected source records. It does not
        represent guilt, criminality or a confirmed identity, and requires analyst review.
      </Disclaimer>
    </div>
  );
}

function Block({ label, children }: { label: string; children: React.ReactNode }) {
  return (
    <div className="space-y-1.5">
      <p className="text-[11px] font-semibold tracking-wider text-muted-foreground uppercase">
        {label}
      </p>
      {children}
    </div>
  );
}
