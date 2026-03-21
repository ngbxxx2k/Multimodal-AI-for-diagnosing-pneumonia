import { ClinicalData, AnalysisResult } from "../types";

export async function generateAnalysis(data: ClinicalData, imageFile?: File): Promise<AnalysisResult> {
  const formData = new FormData();
  
  // Create clinical data payload
  formData.append('data', JSON.stringify(data));
  
  if (imageFile) {
    formData.append('file', imageFile);
  } else {
    // If no image provided, we can't run full pipeline.
    // For now, throw error or send dummy.
    throw new Error("X-ray image is required for analysis.");
  }

  try {
    const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';
    const response = await fetch(`${API_URL}/analyze`, {
      method: 'POST',
      body: formData,
    });

    if (!response.ok) {
      throw new Error(`Server error: ${response.statusText}`);
    }

    const result = await response.json();
    return result;
  } catch (error) {
    console.error("API Call failed:", error);
    throw error;
  }
}
