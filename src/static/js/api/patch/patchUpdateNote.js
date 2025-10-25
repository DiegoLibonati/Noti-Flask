import { apiPrefixNotes } from "../../api/notes.js";
export const patchUpdateNote = async (id, content) => {
    try {
        const body = {
            content: content,
        };
        const response = await fetch(`${apiPrefixNotes}/${id}`, {
            method: "PATCH",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(body),
        });
        if (!response.ok) {
            throw new Error("Error patch note.");
        }
        const data = await response.json();
        return data;
    }
    catch (e) {
        throw new Error(`Error patch note: ${e}.`);
    }
};
