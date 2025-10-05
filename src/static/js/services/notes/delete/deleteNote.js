import { apiPrefixNotes } from "../../../constants/constants.js";
export const deleteNote = (id) => {
    return fetch(`${apiPrefixNotes}/${id}`, { method: "DELETE" });
};
