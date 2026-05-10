import type { ResponseWithRedirect } from "@/types/responses";

const BASE_URL = "/api/v1/auth";

const authService = {
  logout: async (): Promise<Partial<ResponseWithRedirect>> => {
    const res = await fetch(`${BASE_URL}/logout`);
    return (await res.json()) as Partial<ResponseWithRedirect>;
  },

  login: async (
    username: string,
    password: string
  ): Promise<Partial<ResponseWithRedirect>> => {
    const response = await fetch(`${BASE_URL}/login`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ username, password }),
    });
    return (await response.json()) as Partial<ResponseWithRedirect>;
  },

  register: async (
    username: string,
    password: string,
    email: string
  ): Promise<Partial<ResponseWithRedirect>> => {
    const response = await fetch(`${BASE_URL}/sign_up`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ username, password, email }),
    });
    return (await response.json()) as Partial<ResponseWithRedirect>;
  },
};

export default authService;
