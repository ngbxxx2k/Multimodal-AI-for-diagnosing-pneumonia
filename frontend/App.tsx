
import React, { useState } from 'react';
import Header from './components/Header';
import InputPanel from './components/InputPanel';
import ResultsPanel from './components/ResultsPanel';
import { ClinicalData, AnalysisResult, AppState } from './types';
import { generateAnalysis } from './services/geminiService';
import { INITIAL_CLINICAL_DATA } from './constants';

const App: React.FC = () => {
  const [appState, setAppState] = useState<AppState>('idle');
  const [file, setFile] = useState<File | null>(null);
  const [clinicalData, setClinicalData] = useState<ClinicalData>(INITIAL_CLINICAL_DATA);
  const [result, setResult] = useState<AnalysisResult | null>(null);

  const handleAnalyze = async () => {
    if (!file) {
      alert("Vui lòng tải lên ảnh X-Quang.");
      return;
    }
    try {
      setAppState('analyzing');
      const analysis = await generateAnalysis(clinicalData, file);
      setResult(analysis);
      setAppState('completed');
    } catch (error) {
      console.error("Analysis failed:", error);
      setAppState('error');
    }
  };

  return (
    <div className="flex flex-col h-screen">
      <Header />
      
      <main className="flex-1 overflow-hidden p-6 bg-slate-50">
        <div className="h-full max-w-[1600px] mx-auto grid grid-cols-1 lg:grid-cols-12 gap-6">
          <div className="lg:col-span-5 h-full overflow-hidden">
            <InputPanel 
              file={file}
              setFile={setFile}
              data={clinicalData} 
              setData={setClinicalData} 
              onAnalyze={handleAnalyze}
              appState={appState}
            />
          </div>
          
          <div className="lg:col-span-7 h-full overflow-hidden">
            <ResultsPanel result={result} appState={appState} />
          </div>
        </div>
      </main>

      {appState === 'error' && (
        <div className="fixed bottom-6 right-6 bg-red-600 text-white px-6 py-3 rounded-xl shadow-2xl flex items-center gap-3 animate-bounce">
          <span className="material-symbols-outlined">error</span>
          <span className="font-bold">Phân tích thất bại. Vui lòng thử lại.</span>
          <button onClick={() => setAppState('idle')} className="ml-4 opacity-50 hover:opacity-100 transition-opacity">
            <span className="material-symbols-outlined">close</span>
          </button>
        </div>
      )}
    </div>
  );
};

export default App;
