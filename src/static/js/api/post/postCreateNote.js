import { apiPrefixNotes } from "../../api/notes.js";
export const postCreateNote = async () => {
    try {
        return await fetch(`${apiPrefixNotes}/`, { method: "POST" });
    }
    catch (e) {
        throw new Error(`Error creating note: ${e}.`);
    }
};
