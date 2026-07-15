import HypothesisCard from "@/components/HypothesisCard";
import RetrievedContext from "@/components/RetrievedContext";
import SeverityBadge from "@/components/SeverityBadge";
import type {
  AnalysisResponse,
} from "@/lib/types";

interface AnalysisResultProps {
  result: AnalysisResponse;
}

export default function AnalysisResult({
  result,
}: AnalysisResultProps) {
  if (!result.analysis) {
    return (
      <section className="rounded-2xl border border-red-200 bg-red-50 p-6">
        <h2 className="font-semibold text-red-900">
          Analysis unavailable
        </h2>

        <p className="mt-2 text-sm text-red-700">
          {result.error ??
            "The workflow did not return an analysis."}
        </p>
      </section>
    );
  }

  const analysis = result.analysis;

  return (
    <div className="space-y-6">
      <section className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
        <div className="flex flex-wrap items-start justify-between gap-4">
          <div>
            <p className="text-sm font-semibold text-blue-600">
              Analysis completed
            </p>

            <h2 className="mt-1 text-xl font-semibold text-slate-950">
              Incident assessment
            </h2>
          </div>

          <SeverityBadge
            severity={analysis.severity}
          />
        </div>

        <p className="mt-5 leading-7 text-slate-700">
          {analysis.summary}
        </p>

        <div className="mt-6">
          <h3 className="font-semibold text-slate-900">
            Observed symptoms
          </h3>

          <div className="mt-3 flex flex-wrap gap-2">
            {analysis.symptoms.map((symptom) => (
              <span
                key={symptom}
                className="rounded-full bg-slate-100 px-3 py-1 text-sm text-slate-700"
              >
                {symptom}
              </span>
            ))}
          </div>
        </div>
      </section>

      <section className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
        <h2 className="text-xl font-semibold text-slate-950">
          Root-cause hypotheses
        </h2>

        <div className="mt-5 space-y-4">
          {analysis.hypotheses.map(
            (hypothesis, index) => (
              <HypothesisCard
                key={`${hypothesis.cause}-${index}`}
                hypothesis={hypothesis}
                rank={index + 1}
              />
            ),
          )}
        </div>
      </section>

      <section className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
        <h2 className="text-xl font-semibold text-slate-950">
          Investigation plan
        </h2>

        <ol className="mt-5 space-y-3">
          {analysis.investigation_steps.map(
            (step, index) => (
              <li
                key={step}
                className="flex gap-3"
              >
                <span className="flex h-7 w-7 shrink-0 items-center justify-center rounded-full bg-blue-100 text-sm font-semibold text-blue-700">
                  {index + 1}
                </span>

                <p className="pt-0.5 text-slate-700">
                  {step}
                </p>
              </li>
            ),
          )}
        </ol>

        <div className="mt-6 rounded-xl border border-blue-200 bg-blue-50 p-4">
          <h3 className="font-semibold text-blue-900">
            Recommended next action
          </h3>

          <p className="mt-2 text-sm leading-6 text-blue-800">
            {analysis.recommended_next_action}
          </p>
        </div>

        {analysis.limitations.length > 0 ? (
          <div className="mt-6">
            <h3 className="font-semibold text-slate-900">
              Limitations
            </h3>

            <ul className="mt-2 list-disc space-y-1 pl-5 text-sm text-slate-600">
              {analysis.limitations.map(
                (limitation) => (
                  <li key={limitation}>
                    {limitation}
                  </li>
                ),
              )}
            </ul>
          </div>
        ) : null}
      </section>

      <RetrievedContext
        incidents={result.historical_incidents}
        runbooks={result.runbooks}
        deployments={result.deployments}
      />
    </div>
  );
}