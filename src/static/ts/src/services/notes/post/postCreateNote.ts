import { apiPrefixNotes } from "@src/constants/constants";

export const postCreateNote = (): Promise<Response> => {
  return fetch(`${apiPrefixNotes}/`, { method: "POST" });
};
