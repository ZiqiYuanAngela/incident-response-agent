"use client";

import {
  FormEvent,
  useState,
} from "react";

interface IncidentFormValue {
  serviceName: string;
  description: string;
  logs: string;
}

interface IncidentFormProps {
  disabled?: boolean;
  onSubmit: (
    value: IncidentFormValue,
  ) => Promise<void>;
}

const SAMPLE_DESCRIPTION =
  "Customers started receiving payment timeout errors shortly after version 2.4.0 was deployed.";

const SAMPLE_LOGS = `2026-07-18T10:02:13Z ERROR Failed to acquire database connection
2026-07-18T10:02:13Z ERROR Database connection timed out after 3000ms
2026-07-18T10:02:14Z WARN Connection pool utilization: 100%
2026-07-18T10:02:15Z ERROR POST /payments returned 503`;

export default function IncidentForm({
  disabled = false,
  onSubmit,
}: IncidentFormProps) {
  const [serviceName, setServiceName] =
    useState("payment-service");

  const [description, setDescription] =
    useState("");

  const [logs, setLogs] =
    useState("");

  const [error, setError] =
    useState<string | null>(null);

  async function handleSubmit(
    event: FormEvent<HTMLFormElement>,
  ): Promise<void> {
    event.preventDefault();

    if (description.trim().length < 5) {
      setError("Enter an incident description.");
      return;
    }

    if (logs.trim().length < 5) {
      setError("Enter incident logs.");
      return;
    }

    setError(null);

    await onSubmit({
      serviceName,
      description: description.trim(),
      logs: logs.trim(),
    });
  }

  function loadSample(): void {
    setServiceName("payment-service");
    setDescription(SAMPLE_DESCRIPTION);
    setLogs(SAMPLE_LOGS);
    setError(null);
  }

  return (
    <section className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
      <div className="mb-6">
        <p className="text-sm font-semibold text-blue-600">
          New incident
        </p>

        <h2 className="mt-1 text-xl font-semibold text-slate-950">
          Analyze operational signals
        </h2>

        <p className="mt-2 text-sm leading-6 text-slate-600">
          Submit a service, incident description, and logs.
          The workflow will search historical incidents,
          runbooks, and deployment history.
        </p>
      </div>

      <form
        onSubmit={handleSubmit}
        className="space-y-5"
      >
        <div>
          <label
            htmlFor="service"
            className="block text-sm font-medium text-slate-700"
          >
            Service
          </label>

          <select
            id="service"
            value={serviceName}
            disabled={disabled}
            onChange={(event) =>
              setServiceName(event.target.value)
            }
            className="mt-2 w-full rounded-lg border border-slate-300 bg-white px-3 py-2 text-sm text-slate-900"
          >
            <option value="payment-service">
              payment-service
            </option>

            <option value="order-service">
              order-service
            </option>

            <option value="notification-service">
              notification-service
            </option>
          </select>
        </div>

        <div>
          <label
            htmlFor="description"
            className="block text-sm font-medium text-slate-700"
          >
            Incident description
          </label>

          <textarea
            id="description"
            value={description}
            disabled={disabled}
            onChange={(event) =>
              setDescription(event.target.value)
            }
            rows={4}
            placeholder="Describe what users or operators are observing."
            className="mt-2 w-full rounded-lg border border-slate-300 px-3 py-3 text-sm text-slate-900 outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-100"
          />
        </div>

        <div>
          <label
            htmlFor="logs"
            className="block text-sm font-medium text-slate-700"
          >
            Logs
          </label>

          <textarea
            id="logs"
            value={logs}
            disabled={disabled}
            onChange={(event) =>
              setLogs(event.target.value)
            }
            rows={12}
            spellCheck={false}
            placeholder="Paste logs or a stack trace."
            className="mt-2 w-full rounded-xl border border-slate-300 bg-slate-950 p-4 font-mono text-sm leading-6 text-slate-100 outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-100"
          />
        </div>

        {error ? (
          <p className="rounded-lg bg-red-50 px-3 py-2 text-sm text-red-700">
            {error}
          </p>
        ) : null}

        <div className="flex flex-wrap gap-3">
          <button
            type="submit"
            disabled={disabled}
            className="rounded-lg bg-blue-600 px-4 py-2 text-sm font-semibold text-white hover:bg-blue-700 disabled:cursor-not-allowed disabled:bg-slate-300"
          >
            {disabled
              ? "Analyzing..."
              : "Analyze incident"}
          </button>

          <button
            type="button"
            disabled={disabled}
            onClick={loadSample}
            className="rounded-lg border border-slate-300 px-4 py-2 text-sm font-semibold text-slate-700 hover:bg-slate-50 disabled:cursor-not-allowed disabled:opacity-50"
          >
            Load sample
          </button>
        </div>
      </form>
    </section>
  );
}