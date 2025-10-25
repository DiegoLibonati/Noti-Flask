import { DeleteNoteResponse } from "@src/entities/responses";

import { apiPrefixNotes } from "@src/api/notes";

export const deleteNote = async (id: string): Promise<DeleteNoteResponse> => {
  try {
    const response = await fetch(`${apiPrefixNotes}/${id}`, {
      method: "DELETE",
    });

    if (!response.ok) {
      throw new Error("Error deleting note.");
    }

    const data: DeleteNoteResponse = await response.json();

    return data;
  } catch (e) {
    throw new Error(`Error deleting note: ${e}.`);
  }
};
