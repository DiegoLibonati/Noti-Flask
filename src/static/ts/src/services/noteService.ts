import type { Note } from "@/types/app";
import type { ResponseWithData, ResponseWithRedirect } from "@/types/responses";

const BASE_URL = "/api/v1/notes/";

const noteService = {
  getAll: async (): Promise<ResponseWithData<Note[]>> => {
    const response = await fetch(BASE_URL);

    if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);

    return (await response.json()) as ResponseWithData<Note[]>;
  },

  create: async (content: string): Promise<ResponseWithRedirect> => {
    const response = await fetch(BASE_URL, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ content }),
    });

    if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);

    return (await response.json()) as ResponseWithRedirect;
  },

  delete: async (id: number): Promise<ResponseWithRedirect> => {
    const response = await fetch(`${BASE_URL}/${id}`, {
      method: "DELETE",
    });

    if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);

    return (await response.json()) as ResponseWithRedirect;
  },

  edit: async (id: number, content: string): Promise<ResponseWithRedirect> => {
    const response = await fetch(`${BASE_URL}/${id}`, {
      method: "PATCH",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ content }),
    });

    if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);

    return (await response.json()) as ResponseWithRedirect;
  },
};

export default noteService;
