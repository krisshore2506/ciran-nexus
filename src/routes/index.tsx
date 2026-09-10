import { createFileRoute, useNavigate } from "@tanstack/react-router";
import { useState } from "react";
import { Lock, ShieldCheck } from "lucide-react";

export const Route = createFileRoute("/")({
  head: () => ({
    meta: [
      { title: "CIRAN — Secure Investigator Login" },
      {
        name: "description",
        content:
          "Authorized login for CIRAN, the Criminal Intelligence & Relationship Analysis Network intelligence layer.",
      },
      { property: "og:title", content: "CIRAN — Secure Investigator Login" },
      {
        property: "og:description",
        content: "Authorized investigation environment for criminal intelligence analysis.",
      },
    ],
  }),
  component: LoginPage,
});

function LoginPage() {
  const navigate = useNavigate();
  const [officerId, setOfficerId] = useState("TN-INV-4471");
  const [password, setPassword] = useState("••••••••••");

  return (
    <div className="grid min-h-screen bg-background lg:grid-cols-2">
      <div className="relative hidden flex-col justify-between border-r border-border bg-surface p-10 grid-backdrop lg:flex">
        <div className="flex items-center gap-3">
          <div className="flex size-10 items-center justify-center rounded-md border border-primary/40 bg-primary/10">
            <ShieldCheck className="size-5 text-primary" />
          </div>
          <div>
            <p className="text-sm font-semibold tracking-[0.25em]">CIRAN</p>
            <p className="text-[11px] text-muted-foreground">
              Criminal Intelligence &amp; Relationship Analysis Network
            </p>
          </div>
        </div>

        <div className="max-w-md space-y-4">
          <h2 className="text-lg font-semibold text-foreground">
            An intelligence layer over existing investigation systems
          </h2>
          <ol className="space-y-2 text-sm text-muted-foreground">
            {[
              "Existing government records (CCTNS / ICJS)",
              "CIRAN intelligence layer",
              "Entity resolution",
              "Temporal + cross-case correlation",
              "Hidden pattern detection",
              "Explainable AI",
              "Evidence-backed investigative intelligence",
            ].map((s, i, arr) => (
              <li key={s} className="flex flex-col">
                <span className="w-fit rounded border border-border-strong bg-surface-2 px-2.5 py-1 text-xs text-foreground">
                  {s}
                </span>
                {i < arr.length - 1 && (
                  <span className="ml-3 text-xs text-muted-foreground">↓</span>
                )}
              </li>
            ))}
          </ol>
        </div>

        <p className="text-[11px] text-muted-foreground">
          CIRAN does not replace source systems. It consumes structured investigation data and
          returns explainable, evidence-linked intelligence.
        </p>
      </div>

      <div className="flex items-center justify-center p-6">
        <div className="panel w-full max-w-sm p-7">
          <div className="mb-6 text-center">
            <p className="text-2xl font-semibold tracking-[0.3em] text-foreground">CIRAN</p>
            <p className="mt-1 text-[11px] text-muted-foreground">
              Criminal Intelligence &amp; Relationship Analysis Network
            </p>
          </div>

          <form
            className="space-y-4"
            onSubmit={(e) => {
              e.preventDefault();
              void navigate({ to: "/dashboard" });
            }}
          >
            <Field
              label="Officer ID"
              value={officerId}
              onChange={setOfficerId}
              placeholder="TN-INV-0000"
            />
            <Field
              label="Password"
              value={password}
              onChange={setPassword}
              type="password"
              placeholder="Enter secure password"
            />

            <button
              type="submit"
              className="w-full rounded-md bg-primary py-2.5 text-sm font-semibold text-primary-foreground transition-colors hover:bg-primary/90"
            >
              Secure Login
            </button>
          </form>

          <div className="mt-6 flex items-start gap-2 rounded-md border border-border bg-surface-2 px-3 py-2.5">
            <Lock className="mt-0.5 size-3.5 shrink-0 text-primary" />
            <p className="text-[11px] leading-relaxed text-muted-foreground">
              Authorized investigation environment. All access, queries and analyst decisions are
              recorded in the audit trail.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}

function Field({
  label,
  value,
  onChange,
  type = "text",
  placeholder,
}: {
  label: string;
  value: string;
  onChange: (v: string) => void;
  type?: string;
  placeholder?: string;
}) {
  return (
    <label className="block">
      <span className="text-[11px] font-medium tracking-wider text-muted-foreground uppercase">
        {label}
      </span>
      <input
        type={type}
        value={value}
        placeholder={placeholder}
        onChange={(e) => onChange(e.target.value)}
        className="mt-1.5 w-full rounded-md border border-border bg-input px-3 py-2 text-sm text-foreground placeholder:text-muted-foreground focus:border-primary/60 focus:outline-none"
      />
    </label>
  );
}
