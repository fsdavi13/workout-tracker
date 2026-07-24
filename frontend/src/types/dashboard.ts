export interface ResumoAcademia {
  quantidade_series: number;
  quantidade_exercicios: number;
  volume_total: number;
}

export interface ResumoCorrida {
  quantidade_corridas: number;
  distancia_total_km: number;
  tempo_total_segundos: number;
  melhor_pace: string | null;
}

export interface ResumoDieta {
  quantidade_registros: number;
  calorias: number;
  proteinas_g: number;
  carboidratos_g: number;
  gorduras_g: number;
}

export interface Dashboard {
  data: string;
  academia: ResumoAcademia;
  corrida: ResumoCorrida;
  dieta: ResumoDieta;
}