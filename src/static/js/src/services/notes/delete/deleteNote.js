import { apiPrefixNotes } from "../../../constants/constants.js";

export const deleteNote = (id) => {
  return fetch(`${apiPrefixNotes}/delete/${id}`, { method: "delete" });
};
