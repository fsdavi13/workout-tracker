import type {
  Exercicio,
  ExercicioPayload,
} from "../types/academia";
import api from "./api";

export async function listarExercicios(): Promise<
  Exercicio[]
> {
  const resposta = await api.get<Exercicio[]>(
    "/academia/exercicios",
  );

  return resposta.data;
}

export async function criarExercicio(
  dados: ExercicioPayload,
): Promise<Exercicio> {
  const resposta = await api.post<Exercicio>(
    "/academia/exercicios",
    dados,
  );

  return resposta.data;
}