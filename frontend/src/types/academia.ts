export interface Exercicio {
  id: number;
  nome: string;
  grupo_muscular: string;
}

export interface ExercicioPayload {
  nome: string;
  grupo_muscular: string;
}