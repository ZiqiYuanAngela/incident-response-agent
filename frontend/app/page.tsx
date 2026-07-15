import IncidentResponseApp from "@/components/IncidentResponseApp";

export default function Home() {
  return (
    <main className="min-h-screen bg-slate-50">
      <header className="border-b border-slate-200 bg-white">
        <div className="mx-auto max-w-7xl px-6 py-8">
          <p className="text-sm font-semibold uppercase tracking-widest text-blue-600">
            AI operations workflow
          </p>

          <h1 className="mt-3 text-3xl font-bold tracking-tight text-slate-950 sm:text-4xl">
            Incident Response Agent
          </h1>

          <p className="mt-3 max-w-3xl text-base leading-7 text-slate-600">
            Analyze logs, retrieve relevant operational
            context, and generate evidence-backed root-cause
            hypotheses and investigation steps.
          </p>
        </div>
      </header>

      <div className="mx-auto max-w-7xl px-6 py-8">
        <IncidentResponseApp />
      </div>
    </main>
  );
}