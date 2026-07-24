import api from "./api";
import type { Dashboard } from "../types/dashboard";

export async function buscarDashboard(
  data?: string,
): Promise<Dashboard> {
  const response = await api.get<Dashboard>("/dashboard", {
    params: data ? { data } : undefined,
  });

  return response.data;
}