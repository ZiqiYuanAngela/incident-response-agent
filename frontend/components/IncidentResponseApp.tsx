"use client";

import { useState } from "react";

import AnalysisResult from "@/components/AnalysisResult";
import IncidentForm from "@/components/IncidentForm";
import {
  analyzeIncident,
  createIncident,
} from "@/lib/api";
import type {
  AnalysisResponse,
} from "@/lib/types";

interface IncidentFormValue {
  serviceName: string;
  description: string;
  logs: string;
}

export default function IncidentResponseApp() {
  const [result, setResult] =
    useState<AnalysisResponse | null>(null);

  const [isAnalyzing, setIsAnalyzing] =
    useState(false);

  const [error, setError] =
    useState<string | null>(null);

  async function handleSubmit(
    input: IncidentFormValue,
  ): Promise<void> {
    setIsAnalyzing(true);
    setError(null);
    setResult(null);

    try {
      const incident = await createIncident(input);

      const analysisResult =
        await analyzeIncident(incident.id);

      setResult(analysisResult);
    } catch (requestError) {
      setError(
        requestError instanceof Error
          ? requestError.message
          : "The incident could not be analyzed.",
      );
    } finally {
      setIsAnalyzing(false);
    }
  }

  return (
    <div className="grid gap-6 xl:grid-cols-[420px_1fr]">
      <div>
        <IncidentForm
          disabled={isAnalyzing}
          onSubmit={handleSubmit}
        />

        {isAnalyzing ? (
          <div className="mt-6 rounded-2xl border border-blue-200 bg-blue-50 p-5">
            <p className="font-semibold text-blue-900">
              Analysis is running
            </p>

            <p className="mt-2 text-sm leading-6 text-blue-700">
              Extracting signals, searching historical
              incidents, checking runbooks and deployments,
              and generating evidence-backed hypotheses.
            </p>
          </div>
        ) : null}

        {error ? (
          <div className="mt-6 rounded-2xl border border-red-200 bg-red-50 p-5">
            <p className="font-semibold text-red-900">
              Request failed
            </p>

            <p className="mt-2 text-sm text-red-700">
              {error}
            </p>
          </div>
        ) : null}
      </div>

      <div>
        {result ? (
          <AnalysisResult result={result} />
        ) : (
          <section className="rounded-2xl border border-dashed border-slate-300 bg-white p-12 text-center">
            <h2 className="font-semibold text-slate-900">
              No incident analyzed yet
            </h2>

            <p className="mt-2 text-sm text-slate-500">
              Load the sample scenario or submit your own
              synthetic incident.
            </p>
          </section>
        )}
      </div>
    </div>
  );
}