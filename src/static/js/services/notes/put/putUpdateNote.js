import { apiPrefixNotes } from "../../../constants/constants.js";

export const putUpdateNote = (id, content) => {
  const data = {
    content: content,
  };

  return fetch(`${apiPrefixNotes}/edit/${id}`, {
    method: "put",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });
};
