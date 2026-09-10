import type { ReactNode } from "react";
import { cn } from "@/lib/utils";
import type { EntityType, Severity } from "@/lib/ciran-data";

export function Panel({
  title,
  description,
  action,
  children,
  className,
  bodyClassName,
}: {
  title?: string | undefined;
  description?: string | undefined;
  action?: ReactNode | undefined;
  children: ReactNode;
  className?: string | undefined;
  bodyClassName?: string | undefined;
}) {
  return (
    <section className={cn("panel flex flex-col overflow-hidden", className)}>
      {(title || action) && (
        <header className="flex items-start justify-between gap-4 border-b border-border px-4 py-3">
          <div>
            {title && (
              <h2 className="text-sm font-semibold tracking-wide text-foreground uppercase">
                {title}
              </h2>
            )}
            {description && <p className="mt-0.5 text-xs text-muted-foreground">{description}</p>}
          </div>
          {action}
        </header>
      )}
      <div className={cn("p-4", bodyClassName)}>{children}</div>
    </section>
  );
}

export function PageHeader({
  title,
  subtitle,
  actions,
}: {
  title: string;
  subtitle?: string | undefined;
  actions?: ReactNode | undefined;
}) {
  return (
    <div className="flex flex-wrap items-end justify-between gap-3">
      <div>
        <h1 className="text-xl font-semibold tracking-tight text-foreground">{title}</h1>
        {subtitle && <p className="mt-1 text-sm text-muted-foreground">{subtitle}</p>}
      </div>
      {actions && <div className="flex flex-wrap items-center gap-2">{actions}</div>}
    </div>
  );
}

const severityStyles: Record<Severity | "success", string> = {
  critical: "border-critical/40 bg-critical/12 text-critical",
  high: "border-high/40 bg-high/12 text-high",
  medium: "border-medium/40 bg-medium/12 text-medium",
  info: "border-info/40 bg-info/12 text-info",
  success: "border-success/40 bg-success/12 text-success",
};

export function SeverityBadge({
  severity,
  children,
}: {
  severity: Severity | "success";
  children?: ReactNode;
}) {
  return (
    <span
      className={cn(
        "inline-flex items-center gap-1.5 rounded border px-2 py-0.5 text-[11px] font-semibold tracking-wider uppercase",
        severityStyles[severity],
      )}
    >
      <span className="size-1.5 rounded-full bg-current" />
      {children ?? severity}
    </span>
  );
}

export function Tag({
  children,
  className,
  tone = "default",
}: {
  children: ReactNode;
  className?: string;
  tone?: "default" | "outline";
}) {
  return (
    <span
      className={cn(
        "inline-flex items-center gap-1.5 rounded border px-2 py-0.5 text-xs",
        tone === "default"
          ? "border-border-strong bg-surface-2 text-foreground"
          : "border-border text-muted-foreground",
        className,
      )}
    >
      {children}
    </span>
  );
}

const nodeColor: Record<EntityType, string> = {
  person: "bg-node-person",
  phone: "bg-node-phone",
  vehicle: "bg-node-vehicle",
  account: "bg-node-account",
  location: "bg-node-location",
  case: "bg-node-case",
};

export function EntityChip({
  type,
  label,
  onClick,
}: {
  type?: EntityType | undefined;
  label: string;
  onClick?: (() => void) | undefined;
}) {
  const Comp = onClick ? "button" : "span";
  return (
    <Comp
      onClick={onClick}
      className={cn(
        "inline-flex items-center gap-2 rounded-full border border-border-strong bg-surface-2 px-2.5 py-1 text-xs text-foreground",
        onClick && "transition-colors hover:border-primary/60 hover:bg-accent",
      )}
    >
      {type && <span className={cn("size-2 rounded-full", nodeColor[type])} />}
      {label}
    </Comp>
  );
}

export function Confidence({ value, label = "Confidence" }: { value: number; label?: string }) {
  const tone = value >= 80 ? "bg-success" : value >= 65 ? "bg-medium" : "bg-high";
  return (
    <div className="w-full">
      <div className="flex items-center justify-between text-xs">
        <span className="text-muted-foreground">{label}</span>
        <span className="font-mono font-semibold text-foreground">{value}%</span>
      </div>
      <div className="mt-1.5 h-1.5 w-full overflow-hidden rounded-full bg-muted">
        <div className={cn("h-full rounded-full", tone)} style={{ width: `${value}%` }} />
      </div>
    </div>
  );
}

export function ActionButton({
  children,
  variant = "secondary",
  onClick,
  className,
  type = "button",
  disabled,
}: {
  children: ReactNode;
  variant?: "primary" | "secondary" | "ghost" | "danger" | undefined;
  onClick?: (() => void) | undefined;
  className?: string | undefined;
  type?: "button" | "submit" | undefined;
  disabled?: boolean | undefined;
}) {
  const styles = {
    primary: "bg-primary text-primary-foreground hover:bg-primary/90",
    secondary:
      "border border-border-strong bg-surface-2 text-foreground hover:border-primary/50 hover:bg-accent",
    ghost: "text-muted-foreground hover:bg-surface-2 hover:text-foreground",
    danger: "border border-critical/40 bg-critical/10 text-critical hover:bg-critical/20",
  }[variant];
  return (
    <button
      type={type}
      onClick={onClick}
      disabled={disabled}
      className={cn(
        "inline-flex items-center justify-center gap-2 rounded-md px-3 py-1.5 text-xs font-medium transition-colors disabled:opacity-50",
        styles,
        className,
      )}
    >
      {children}
    </button>
  );
}

export function PathTrail({ steps, dense }: { steps: string[]; dense?: boolean }) {
  return (
    <ol className={cn("flex flex-col", dense ? "gap-0.5" : "gap-1")}>
      {steps.map((s, i) => (
        <li key={`${s}-${i}`} className="flex flex-col">
          <span className="inline-flex w-fit items-center rounded border border-border-strong bg-surface-2 px-2 py-1 text-xs text-foreground">
            {s}
          </span>
          {i < steps.length - 1 && (
            <span className="ml-3 text-xs leading-4 text-muted-foreground">↓</span>
          )}
        </li>
      ))}
    </ol>
  );
}

export function KeyValue({ items }: { items: { label: string; value: string }[] }) {
  return (
    <dl className="grid gap-3 sm:grid-cols-2">
      {items.map((i) => (
        <div key={i.label}>
          <dt className="text-[11px] tracking-wider text-muted-foreground uppercase">{i.label}</dt>
          <dd className="mt-0.5 text-sm text-foreground">{i.value}</dd>
        </div>
      ))}
    </dl>
  );
}

export function Disclaimer({ children }: { children: ReactNode }) {
  return (
    <p className="rounded-md border border-border bg-surface-2 px-3 py-2 text-[11px] leading-relaxed text-muted-foreground">
      {children}
    </p>
  );
}
