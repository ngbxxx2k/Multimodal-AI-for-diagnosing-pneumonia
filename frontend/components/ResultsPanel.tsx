
import React, { useState } from 'react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import { AnalysisResult, AppState } from '../types';

interface Props {
  result: AnalysisResult | null;
  appState: AppState;
}

const ResultsPanel: React.FC<Props> = ({ result, appState }) => {
  const [activeTab, setActiveTab] = useState<'visual' | 'report'>('visual');

  if (appState === 'idle') {
    return (
      <div className="lg:col-span-7 flex flex-col h-full bg-white rounded-xl shadow-sm border border-slate-200 items-center justify-center text-center p-12">
        <div className="w-24 h-24 bg-slate-50 rounded-full flex items-center justify-center mb-6">
          <span className="material-symbols-outlined text-5xl text-slate-200">monitoring</span>
        </div>
        <h2 className="text-xl font-bold text-slate-400">Sẵn sàng phân tích</h2>
        <p className="text-slate-400 max-w-xs mt-2">Nhập dữ liệu bệnh nhân và nhấn "Phân tích & Chẩn đoán" để bắt đầu.</p>
      </div>
    );
  }

  if (appState === 'analyzing') {
    return (
      <div className="lg:col-span-7 flex flex-col h-full bg-white rounded-xl shadow-sm border border-slate-200 items-center justify-center p-12 overflow-hidden">
        <div className="relative w-20 h-20 mb-8">
          <div className="absolute inset-0 border-4 border-sky-100 rounded-full"></div>
          <div className="absolute inset-0 border-4 border-sky-500 rounded-full border-t-transparent animate-spin"></div>
        </div>
        <h2 className="text-xl font-bold text-slate-800 animate-pulse">Đang chạy chẩn đoán...</h2>
        <p className="text-slate-500 mt-2">Đang tham vấn với PneumoScan AI Engine</p>
        
        <div className="w-64 h-1.5 bg-slate-100 rounded-full mt-8 overflow-hidden">
          <div className="h-full bg-sky-500 animate-[loading_2s_ease-in-out_infinite]"></div>
        </div>
        <style>{`
          @keyframes loading {
            0% { transform: translateX(-100%); }
            100% { transform: translateX(100%); }
          }
        `}</style>
      </div>
    );
  }

  return (
    <div className="lg:col-span-7 flex flex-col h-full bg-white rounded-xl shadow-sm border border-slate-200 overflow-hidden">
      {/* Header */}
      <div className="px-6 py-4 border-b border-slate-100 bg-white flex items-center justify-between sticky top-0 z-10">
        <div>
          <h2 className="text-lg font-bold text-slate-800">Kết quả Phân tích</h2>
          <p className="text-xs text-slate-400 font-medium">Mã phiên: <span className="font-mono text-slate-600">#992-AX-2023</span></p>
        </div>
        <div className="flex items-center gap-2 bg-green-50 text-green-700 px-3 py-2 rounded-lg border border-green-100">
          <span className="material-symbols-outlined text-lg">check_circle</span>
          <span className="text-xs font-bold uppercase tracking-wider">Hoàn tất</span>
        </div>
      </div>

      {/* Tabs */}
      <div className="flex items-center border-b border-slate-100 bg-slate-50/30">
        <button 
          onClick={() => setActiveTab('visual')}
          className={`flex-1 py-3.5 px-4 text-xs font-bold flex items-center justify-center gap-2 transition-all border-b-2 ${activeTab === 'visual' ? 'text-sky-500 border-sky-500 bg-white' : 'text-slate-400 border-transparent hover:text-slate-600'}`}
        >
          <span className="material-symbols-outlined text-lg">view_in_ar</span>
          PHÂN TÍCH HÌNH ẢNH
        </button>
        <button 
          onClick={() => setActiveTab('report')}
          className={`flex-1 py-3.5 px-4 text-xs font-bold flex items-center justify-center gap-2 transition-all border-b-2 ${activeTab === 'report' ? 'text-sky-500 border-sky-500 bg-white' : 'text-slate-400 border-transparent hover:text-slate-600'}`}
        >
          <span className="material-symbols-outlined text-lg">description</span>
          BÁO CÁO Y KHOA
        </button>
      </div>

      {/* Content Area */}
      <div className="flex-1 overflow-y-auto bg-slate-50 relative">
        {activeTab === 'visual' ? (
          <div className="p-8 flex flex-col items-center">
            <div className="relative w-full max-w-2xl aspect-[4/3] bg-black rounded-2xl shadow-2xl overflow-hidden group">
              <img 
                src={result?.annotatedImage || "https://lh3.googleusercontent.com/aida-public/AB6AXuAJpCwXkUsif2r5xFcGRgSaqWv4nyLA_di2AcnE7v7yTdUjubsWMUb6FvdCVuR7KXfAr3Edsr_UVBzZsucqAPguCysW6GOcgcShkQbIS6eQTNvWbYCDMetF6SiNZBT4nArfm-gqjKARvyQn4Xq5BgO-ZQ8i_2voLliwTRYD8pYU8i4q7GTlCJwggMWKErDpFOCppfxzTzfhLbir5PvM8o2deawKsLS05q8LlE-heToOE32yaPLAoqc4IbvbrN4bl7Aa9R591bJG1sVv"} 
                className="w-full h-full object-contain"
                alt="Chest X-ray analysis"
              />
              
              {/* Grid Decorative Overlay */}
              <div className="absolute inset-0 bg-[linear-gradient(rgba(255,255,255,0.03)_1px,transparent_1px),linear-gradient(90deg,rgba(255,255,255,0.03)_1px,transparent_1px)] bg-[size:30px_30px] pointer-events-none"></div>
            </div>

            {/* Findings Summary */}
            <div className="mt-8 w-full max-w-2xl bg-white border border-slate-200 rounded-2xl p-6 flex gap-6 items-center shadow-sm">
              <div className="bg-red-50 p-4 rounded-2xl text-red-500">
                <span className="material-symbols-outlined text-3xl">coronavirus</span>
              </div>
              <div className="flex-1">
                <h4 className="font-bold text-slate-800 text-lg">Phát hiện Viêm phổi</h4>
                <p className="text-sm text-slate-500 mt-0.5">Quan sát thấy đám mờ đáng kể tại <strong className="text-slate-700">{result?.location || 'Thùy dưới phổi phải'}</strong>.</p>
              </div>
              <div className="text-right border-l border-slate-100 pl-6">
                <p className="text-[10px] text-slate-400 uppercase font-bold tracking-widest mb-1">Độ tin cậy</p>
                <p className="text-3xl font-black text-sky-500">
                  {result?.confidence !== undefined ? Number(result.confidence).toFixed(2) : '--'}%
                </p>
              </div>
            </div>
          </div>
        ) : (
          <div className="p-8 space-y-8">
            <div className="bg-white rounded-2xl border border-slate-200 p-8 shadow-sm">
              <div className="flex items-center gap-3 mb-6 pb-4 border-b border-slate-50">
                <span className="material-symbols-outlined text-slate-300 text-2xl">summarize</span>
                <h3 className="text-sm font-bold text-slate-800 uppercase tracking-widest">BÁO CÁO Y KHOA TỰ ĐỘNG</h3>
              </div>
              
              <div className="prose prose-slate max-w-none">
                <ReactMarkdown 
                  remarkPlugins={[remarkGfm]}
                  components={{
                    h1: ({node, ...props}) => <h1 className="text-2xl font-bold text-slate-900 border-b pb-2 mb-4" {...props} />,
                    h2: ({node, ...props}) => <h2 className="text-xl font-bold text-slate-800 mt-6 mb-3 flex items-center gap-2" {...props} />,
                    h3: ({node, ...props}) => <h3 className="text-lg font-semibold text-slate-700 mt-4 mb-2" {...props} />,
                    p: ({node, ...props}) => <p className="text-slate-600 leading-relaxed mb-4 text-sm" {...props} />,
                    ul: ({node, ...props}) => <ul className="list-disc list-outside ml-5 space-y-1 mb-4 text-sm text-slate-600" {...props} />,
                    ol: ({node, ...props}) => <ol className="list-decimal list-outside ml-5 space-y-1 mb-4 text-sm text-slate-600" {...props} />,
                    li: ({node, ...props}) => <li className="pl-1" {...props} />,
                    strong: ({node, ...props}) => <strong className="font-bold text-slate-800" {...props} />,
                    blockquote: ({node, ...props}) => <blockquote className="border-l-4 border-sky-500 pl-4 py-1 italic bg-sky-50 text-slate-700 my-4 rounded-r" {...props} />,
                  }}
                >
                  {result?.fullReport || "**Chưa có báo cáo.**"}
                </ReactMarkdown>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default ResultsPanel;
