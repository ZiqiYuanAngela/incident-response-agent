import type {
  AnalysisResponse,
  Incident,
} from "@/lib/types";

const API_BASE_URL =
  process.env.NEXT_PUBLIC_API_BASE_URL ??
  "http://localhost:8000";

interface CreateIncidentInput {
  serviceName: string;
  description: string;
  logs: string;
}

async function getErrorMessage(
  response: Response,
): Promise<string> {
  try {
    const body = (await response.json()) as {
      detail?: string;
    };

    return (
      body.detail ??
      `Request failed with status ${response.status}`
    );
  } catch {
    return `Request failed with status ${response.status}`;
  }
}

export async function createIncident(
  input: CreateIncidentInput,
): Promise<Incident> {
  const response = await fetch(
    `${API_BASE_URL}/api/incidents`,
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        service_name: input.serviceName,
        description: input.description,
        logs: input.logs,
      }),
    },
  );

  if (!response.ok) {
    throw new Error(await getErrorMessage(response));
  }

  return (await response.json()) as Incident;
}

export async function analyzeIncident(
  incidentId: string,
): Promise<AnalysisResponse> {
  const response = await fetch(
    `${API_BASE_URL}/api/incidents/${incidentId}/analyze`,
    {
      method: "POST",
    },
  );

  if (!response.ok) {
    throw new Error(await getErrorMessage(response));
  }

  return (await response.json()) as AnalysisResponse;
}