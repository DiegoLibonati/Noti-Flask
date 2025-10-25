import { apiPrefixNotes } from "../../api/notes.js";
export const deleteNote = async (id) => {
    try {
        const response = await fetch(`${apiPrefixNotes}/${id}`, {
            method: "DELETE",
        });
        if (!response.ok) {
            throw new Error("Error deleting note.");
        }
        const data = await response.json();
        return data;
    }
    catch (e) {
        throw new Error(`Error deleting note: ${e}.`);
    }
};
