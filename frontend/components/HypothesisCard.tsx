import type {
  RootCauseHypothesis,
} from "@/lib/types";

interface HypothesisCardProps {
  hypothesis: RootCauseHypothesis;
  rank: number;
}

export default function HypothesisCard({
  hypothesis,
  rank,
}: HypothesisCardProps) {
  const confidencePercentage = Math.round(
    hypothesis.confidence * 100,
  );

  return (
    <article className="rounded-xl border border-slate-200 p-5">
      <div className="flex flex-wrap items-start justify-between gap-3">
        <div>
          <p className="text-xs font-semibold uppercase tracking-wide text-slate-500">
            Hypothesis {rank}
          </p>

          <h3 className="mt-1 font-semibold text-slate-950">
            {hypothesis.cause}
          </h3>
        </div>

        <span className="rounded-full bg-blue-50 px-3 py-1 text-sm font-semibold text-blue-700">
          {confidencePercentage}% confidence
        </span>
      </div>

      <div className="mt-4">
        <h4 className="text-sm font-semibold text-slate-800">
          Evidence
        </h4>

        <ul className="mt-2 space-y-2">
          {hypothesis.evidence.map(
            (evidence, index) => (
              <li
                key={`${evidence.source_id}-${index}`}
                className="rounded-lg bg-slate-50 px-3 py-2 text-sm text-slate-700"
              >
                <span className="font-semibold">
                  {evidence.source_type}
                </span>

                {" · "}

                <code>{evidence.source_id}</code>

                <p className="mt-1">
                  {evidence.description}
                </p>
              </li>
            ),
          )}
        </ul>
      </div>
    </article>
  );
}