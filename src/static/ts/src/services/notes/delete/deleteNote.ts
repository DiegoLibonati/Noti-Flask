import { apiPrefixNotes } from "@src/constants/constants";

export const deleteNote = (id: string): Promise<Response> => {
  return fetch(`${apiPrefixNotes}/${id}`, { method: "DELETE" });
};
