import { PatchUpdateNoteResponse } from "@src/entities/responses";

import { apiPrefixNotes } from "@src/api/notes";

export const patchUpdateNote = async (
  id: string,
  content: string
): Promise<PatchUpdateNoteResponse> => {
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

    const data: PatchUpdateNoteResponse = await response.json();

    return data;
  } catch (e) {
    throw new Error(`Error patch note: ${e}.`);
  }
};
