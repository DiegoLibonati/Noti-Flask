import { apiPrefixNotes } from "@src/constants/constants";

export const patchUpdateNote = (
  id: string,
  content: string
): Promise<Response> => {
  const data = {
    content: content,
  };

  return fetch(`${apiPrefixNotes}/${id}`, {
    method: "PATCH",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });
};
