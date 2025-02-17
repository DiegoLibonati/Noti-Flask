import { apiPrefixNotes } from "../../../constants/constants.js";

export const postCreateNote = () => {
  return fetch(`${apiPrefixNotes}/create`, { method: "post" });
};
