
export interface Vitals {
  age: string;
  temp: string;
  bp: string;
  respRate: string;
}

export interface Labs {
  wbc: string;
  crp: string;
  spo2: string;
  urea: string;
}

export interface ClinicalData {
  vitals: Vitals;
  confusion: 'Yes' | 'No';
  labs: Labs;
  notes: string;
}

export interface AnalysisResult {
  diagnosis: string;
  severity: string;
  curbScore: number;
  criteria: string[];
  recommendation: string;
  confidence: number;
  location: string;
  fullReport: string;
  annotatedImage?: string;
}

export type AppState = 'idle' | 'analyzing' | 'completed' | 'error';
