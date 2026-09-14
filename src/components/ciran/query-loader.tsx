import React from "react";
import { Loader2, AlertCircle } from "lucide-react";

interface QueryLoaderProps<T> {
  isLoading: boolean;
  error: Error | null;
  data: T | undefined;
  children: (data: T) => React.ReactNode;
  loadingMessage?: string;
  emptyMessage?: string;
  isEmpty?: (data: T) => boolean;
}

export function QueryLoader<T>({
  isLoading,
  error,
  data,
  children,
  loadingMessage = "Loading data...",
  emptyMessage = "No data found.",
  isEmpty = (d: unknown) => (Array.isArray(d) ? d.length === 0 : !d),
}: QueryLoaderProps<T>) {
  if (isLoading) {
    return (
      <div className="flex flex-col items-center justify-center py-12 text-muted-foreground">
        <Loader2 className="h-8 w-8 animate-spin mb-4 text-primary" />
        <p className="text-sm font-medium">{loadingMessage}</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="flex flex-col items-center justify-center py-12 text-critical border border-critical/20 rounded-md bg-critical/5 p-6">
        <AlertCircle className="h-8 w-8 mb-2" />
        <p className="text-sm font-medium mb-1">Failed to load data</p>
        <p className="text-xs opacity-80">{error.message}</p>
      </div>
    );
  }

  if (!data || isEmpty(data)) {
    return (
      <div className="flex flex-col items-center justify-center py-12 text-muted-foreground border border-border border-dashed rounded-md p-6">
        <p className="text-sm">{emptyMessage}</p>
      </div>
    );
  }

  return <>{children(data)}</>;
}
