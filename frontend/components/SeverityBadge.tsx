import type { Severity } from "@/lib/types";

interface SeverityBadgeProps {
  severity: Severity;
}

const styles: Record<Severity, string> = {
  low: "bg-emerald-100 text-emerald-800",
  medium: "bg-amber-100 text-amber-800",
  high: "bg-orange-100 text-orange-800",
  critical: "bg-red-100 text-red-800",
};

export default function SeverityBadge({
  severity,
}: SeverityBadgeProps) {
  return (
    <span
      className={`rounded-full px-3 py-1 text-xs font-bold uppercase tracking-wide ${styles[severity]}`}
    >
      {severity}
    </span>
  );
}
