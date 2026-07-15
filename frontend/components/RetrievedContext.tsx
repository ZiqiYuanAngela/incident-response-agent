import type {
  Deployment,
  HistoricalIncident,
  Runbook,
} from "@/lib/types";

interface RetrievedContextProps {
  incidents: HistoricalIncident[];
  runbooks: Runbook[];
  deployments: Deployment[];
}

export default function RetrievedContext({
  incidents,
  runbooks,
  deployments,
}: RetrievedContextProps) {
  return (
    <section className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
      <h2 className="text-xl font-semibold text-slate-950">
        Retrieved operational context
      </h2>

      <div className="mt-6 space-y-7">
        <ContextSection title="Historical incidents">
          {incidents.length === 0 ? (
            <EmptyState />
          ) : (
            incidents.map((incident) => (
              <div
                key={incident.id}
                className="rounded-lg bg-slate-50 p-4"
              >
                <div className="flex justify-between gap-4">
                  <div>
                    <code className="text-xs text-slate-500">
                      {incident.id}
                    </code>

                    <h3 className="mt-1 font-semibold text-slate-900">
                      {incident.title}
                    </h3>
                  </div>

                  <span className="text-sm font-medium text-blue-700">
                    {Math.round(
                      incident.relevance_score * 100,
                    )}
                    %
                  </span>
                </div>

                <p className="mt-2 text-sm text-slate-600">
                  {incident.root_cause}
                </p>
              </div>
            ))
          )}
        </ContextSection>

        <ContextSection title="Runbooks">
          {runbooks.length === 0 ? (
            <EmptyState />
          ) : (
            runbooks.map((runbook) => (
              <div
                key={runbook.id}
                className="rounded-lg bg-slate-50 p-4"
              >
                <code className="text-xs text-slate-500">
                  {runbook.id}
                </code>

                <h3 className="mt-1 font-semibold text-slate-900">
                  {runbook.title}
                </h3>

                <ul className="mt-2 list-disc space-y-1 pl-5 text-sm text-slate-600">
                  {runbook.steps.map((step) => (
                    <li key={step}>{step}</li>
                  ))}
                </ul>
              </div>
            ))
          )}
        </ContextSection>

        <ContextSection title="Recent deployments">
          {deployments.length === 0 ? (
            <EmptyState />
          ) : (
            deployments.map((deployment) => (
              <div
                key={deployment.id}
                className="rounded-lg bg-slate-50 p-4"
              >
                <div className="flex flex-wrap justify-between gap-3">
                  <div>
                    <code className="text-xs text-slate-500">
                      {deployment.id}
                    </code>

                    <h3 className="mt-1 font-semibold text-slate-900">
                      Version {deployment.version}
                    </h3>
                  </div>

                  <time className="text-sm text-slate-500">
                    {new Date(
                      deployment.deployed_at,
                    ).toLocaleString()}
                  </time>
                </div>

                <ul className="mt-2 list-disc space-y-1 pl-5 text-sm text-slate-600">
                  {deployment.changes.map((change) => (
                    <li key={change}>{change}</li>
                  ))}
                </ul>
              </div>
            ))
          )}
        </ContextSection>
      </div>
    </section>
  );
}

interface ContextSectionProps {
  title: string;
  children: React.ReactNode;
}

function ContextSection({
  title,
  children,
}: ContextSectionProps) {
  return (
    <div>
      <h3 className="text-sm font-bold uppercase tracking-wide text-slate-500">
        {title}
      </h3>

      <div className="mt-3 space-y-3">
        {children}
      </div>
    </div>
  );
}

function EmptyState() {
  return (
    <p className="text-sm text-slate-500">
      No matching records were found.
    </p>
  );
}