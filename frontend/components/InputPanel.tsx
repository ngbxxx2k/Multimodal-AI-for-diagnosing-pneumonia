
import React from 'react';
import { ClinicalData, AppState } from '../types';

interface Props {
  file: File | null;
  setFile: React.Dispatch<React.SetStateAction<File | null>>;
  data: ClinicalData;
  setData: React.Dispatch<React.SetStateAction<ClinicalData>>;
  onAnalyze: () => void;
  appState: AppState;
}

const InputPanel: React.FC<Props> = ({ file, setFile, data, setData, onAnalyze, appState }) => {
  const handleVitalsChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setData(prev => ({ ...prev, vitals: { ...prev.vitals, [name]: value } }));
  };

  const handleLabsChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setData(prev => ({ ...prev, labs: { ...prev.labs, [name]: value } }));
  };

  const clearForm = () => {
    setData({
      vitals: { age: '', temp: '', bp: '', respRate: '' },
      confusion: 'No',
      labs: { wbc: '', crp: '', spo2: '', urea: '' },
      notes: ''
    });
    setFile(null);
  };

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      setFile(e.target.files[0]);
    }
  };

  return (
    <div className="flex flex-col gap-4 overflow-y-auto pr-1 pb-4 h-full">
      {/* X-Ray Input Section */}
      <section className="bg-white rounded-xl shadow-sm border border-slate-200 p-5">
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-sm font-bold text-slate-800 flex items-center gap-2">
            <span className="material-symbols-outlined text-sky-500">add_a_photo</span>
            Ảnh X-Quang
          </h2>
          <span className="text-[10px] font-bold text-slate-400 bg-slate-50 px-2 py-1 rounded tracking-wider">DICOM / JPEG / PNG</span>
        </div>
        
        <div className="relative aspect-[16/6] bg-slate-900 rounded-lg overflow-hidden border-2 border-dashed border-slate-200 flex items-center justify-center group">
          {file ? (
             <img 
               src={URL.createObjectURL(file)} 
               className="w-full h-full object-contain opacity-80"
               alt="X-ray preview"
             />
          ) : (
            <div className="text-center">
              <span className="material-symbols-outlined text-slate-500 text-3xl mb-2">cloud_upload</span>
              <p className="text-xs text-slate-400 font-bold">Nhấn để tải ảnh X-Quang</p>
            </div>
          )}
          
          <input 
            type="file" 
            accept="image/*"
            onChange={handleFileChange}
            className="absolute inset-0 opacity-0 cursor-pointer"
          />
          
          {file && (
            <button 
              onClick={(e) => { e.stopPropagation(); setFile(null); }}
              className="absolute top-3 right-3 bg-black/50 hover:bg-red-500/80 text-white text-[10px] font-bold px-2 py-1 rounded backdrop-blur-md transition-all flex items-center gap-1 z-10"
            >
              <span className="material-symbols-outlined text-sm">close</span> Xóa
            </button>
          )}
        </div>
        <p className="text-[11px] text-center text-slate-400 mt-3">{file ? `File: ${file.name} (${(file.size/1024/1024).toFixed(1)} MB)` : 'Chưa chọn file'}</p>
      </section>

      {/* Clinical Data Section */}
      <section className="bg-white rounded-xl shadow-sm border border-slate-200 p-5 flex-1">
        <div className="flex items-center justify-between mb-5">
          <h2 className="text-sm font-bold text-slate-800 flex items-center gap-2">
            <span className="material-symbols-outlined text-sky-500">demography</span>
            Dữ liệu Lâm sàng
          </h2>
          <button onClick={clearForm} className="text-xs text-sky-500 font-semibold hover:underline">Xóa Form</button>
        </div>

        <div className="space-y-6">
          {/* Vitals */}
          <div>
            <h3 className="text-[10px] font-bold text-slate-400 uppercase tracking-widest mb-4">Sinh hiệu & Nhân khẩu học</h3>
            <div className="grid grid-cols-2 gap-4">
              <VInput label="Tuổi" name="age" value={data.vitals.age} onChange={handleVitalsChange} unit="tuổi" />
              <VInput label="Nhiệt độ" name="temp" value={data.vitals.temp} onChange={handleVitalsChange} unit="°C" />
              <VInput label="Huyết áp" name="bp" value={data.vitals.bp} onChange={handleVitalsChange} unit="mmHg" />
              <VInput label="Nhịp thở" name="respRate" value={data.vitals.respRate} onChange={handleVitalsChange} unit="/phút" />
            </div>
          </div>

          {/* Confusion Toggle */}
          <div>
            <span className="text-xs font-semibold text-slate-600 mb-2 block">Mất định hướng / Lú lẫn?</span>
            <div className="flex gap-2">
              <button 
                onClick={() => setData(prev => ({ ...prev, confusion: 'No' }))}
                className={`flex-1 py-2.5 rounded-lg border text-sm font-bold transition-all ${data.confusion === 'No' ? 'bg-sky-50 border-sky-500 text-sky-600' : 'bg-white border-slate-200 text-slate-400 hover:bg-slate-50'}`}
              >
                Không
              </button>
              <button 
                onClick={() => setData(prev => ({ ...prev, confusion: 'Yes' }))}
                className={`flex-1 py-2.5 rounded-lg border text-sm font-bold transition-all ${data.confusion === 'Yes' ? 'bg-red-50 border-red-500 text-red-600' : 'bg-white border-slate-200 text-slate-400 hover:bg-slate-50'}`}
              >
                Có
              </button>
            </div>
          </div>

          {/* Labs */}
          <div>
            <h3 className="text-[10px] font-bold text-slate-400 uppercase tracking-widest mb-4">Kết quả Xét nghiệm</h3>
            <div className="grid grid-cols-2 gap-4">
              <VInput label="WBC Count" name="wbc" value={data.labs.wbc} onChange={handleLabsChange} />
              <VInput label="CRP" name="crp" value={data.labs.crp} onChange={handleLabsChange} />
              <VInput label="SpO2" name="spo2" value={data.labs.spo2} onChange={handleLabsChange} unit="%" />
              <VInput label="Urea" name="urea" value={data.labs.urea} onChange={handleLabsChange} unit="mmol/L" />
            </div>
          </div>

          {/* Notes */}
          <div>
            <span className="text-xs font-semibold text-slate-600 mb-2 block">Ghi chú Lâm sàng</span>
            <textarea 
              value={data.notes}
              onChange={(e) => setData(prev => ({ ...prev, notes: e.target.value }))}
              placeholder="Nhập bệnh sử hoặc triệu chứng..."
              className="w-full rounded-xl border-slate-200 bg-slate-50 text-slate-900 focus:ring-sky-500 focus:border-sky-500 text-sm p-4 min-h-[100px] resize-none placeholder:text-slate-300"
            />
          </div>
        </div>
      </section>

      <button 
        disabled={appState === 'analyzing'}
        onClick={onAnalyze}
        className={`w-full ${appState === 'analyzing' ? 'bg-slate-400' : 'bg-sky-500 hover:bg-sky-600 shadow-sky-200'} text-white font-bold py-5 px-6 rounded-2xl shadow-lg transition-all active:scale-[0.98] flex items-center justify-center gap-3 text-lg mt-2`}
      >
        <span className="material-symbols-outlined text-2xl">
          {appState === 'analyzing' ? 'sync' : 'analytics'}
        </span>
        {appState === 'analyzing' ? 'ĐANG PHÂN TÍCH...' : 'PHÂN TÍCH & CHẨN ĐOÁN'}
      </button>
    </div>
  );
};

const VInput: React.FC<{ label: string, name: string, value: string, onChange: (e: React.ChangeEvent<HTMLInputElement>) => void, unit?: string }> = ({ label, name, value, onChange, unit }) => (
  <label className="block">
    <span className="text-xs font-semibold text-slate-500 mb-1.5 block">{label}</span>
    <div className="relative">
      <input 
        name={name}
        value={value}
        onChange={onChange}
        className="w-full rounded-xl border-slate-200 bg-slate-50 text-slate-900 focus:ring-sky-500 focus:border-sky-500 text-sm py-2.5 px-4 font-bold" 
        type="text" 
      />
      {unit && <span className="absolute right-4 top-2.5 text-[10px] font-bold text-slate-300">{unit}</span>}
    </div>
  </label>
);

export default InputPanel;
