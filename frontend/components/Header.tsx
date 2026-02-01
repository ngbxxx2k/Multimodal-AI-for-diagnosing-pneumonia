
import React from 'react';

const Header: React.FC = () => {
  return (
    <header className="bg-white border-b border-slate-200 h-16 flex-none z-20 px-6 flex items-center justify-between">
      <div className="flex items-center gap-3">
        <div className="bg-sky-500/10 p-2 rounded-lg text-sky-500">
          <span className="material-symbols-outlined text-2xl">pulmonology</span>
        </div>
        <div>
          <h1 className="text-lg font-bold tracking-tight text-slate-900 leading-none">PneumoScan AI</h1>
          <p className="text-xs text-slate-500 font-medium mt-1">Hệ thống Hỗ trợ Chẩn đoán Hình ảnh</p>
        </div>
      </div>

      <div className="flex items-center gap-6">
        <div className="hidden md:flex items-center gap-2 px-3 py-1.5 bg-green-50 rounded-full border border-green-100">
          <span className="relative flex h-2 w-2">
            <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-green-400 opacity-75"></span>
            <span className="relative inline-flex rounded-full h-2 w-2 bg-green-500"></span>
          </span>
          <span className="text-xs font-semibold text-green-700">Hệ thống Sẵn sàng</span>
        </div>


      </div>
    </header>
  );
};

export default Header;
