export type Severity =
  | "low"
  | "medium"
  | "high"
  | "critical";

export interface Incident {
  id: string;
  service_name: string;
  description: string;
  logs: string;
  status: string;
  created_at: string;
}

export interface ExtractedSignals {
  error_messages: string[];
  symptoms: string[];
  affected_components: string[];
  severity: Severity;
  concise_summary: string;
}

export interface Evidence {
  source_type:
    | "log"
    | "historical_incident"
    | "runbook"
    | "deployment";
  source_id: string;
  description: string;
}

export interface RootCauseHypothesis {
  cause: string;
  confidence: number;
  evidence: Evidence[];
}

export interface IncidentAnalysis {
  severity: Severity;
  summary: string;
  symptoms: string[];
  hypotheses: RootCauseHypothesis[];
  investigation_steps: string[];
  recommended_next_action: string;
  limitations: string[];
}

export interface HistoricalIncident {
  id: string;
  service_name: string;
  title: string;
  symptoms: string[];
  root_cause: string;
  resolution: string;
  relevance_score: number;
}

export interface Runbook {
  id: string;
  service_name: string;
  title: string;
  keywords: string[];
  steps: string[];
  relevance_score: number;
}

export interface Deployment {
  id: string;
  service_name: string;
  version: string;
  deployed_at: string;
  changes: string[];
}

export interface AnalysisResponse {
  run_id: string;
  incident_id: string;
  status: "completed" | "failed";
  current_step: string;
  signals: ExtractedSignals | null;
  historical_incidents: HistoricalIncident[];
  runbooks: Runbook[];
  deployments: Deployment[];
  analysis: IncidentAnalysis | null;
  error?: string | null;
}