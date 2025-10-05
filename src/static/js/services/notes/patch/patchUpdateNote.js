import { apiPrefixNotes } from "../../../constants/constants.js";
export const patchUpdateNote = (id, content) => {
    const data = {
        content: content,
    };
    return fetch(`${apiPrefixNotes}/${id}`, {
        method: "PATCH",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data),
    });
};
