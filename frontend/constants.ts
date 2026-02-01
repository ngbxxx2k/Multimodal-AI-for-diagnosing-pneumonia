import { ClinicalData } from './types';

export const INITIAL_CLINICAL_DATA: ClinicalData = {
  vitals: {
    age: '68',
    temp: '38.5',
    bp: '110/70',
    respRate: '24'
  },
  confusion: 'Yes',
  labs: {
    wbc: '14.2',
    crp: '85',
    spo2: '92',
    urea: '8.5'
  },
  notes: 'Patient presents with productive cough for 4 days, fever, and shortness of breath.'
};
