import { PostCreateNoteResponse } from "@src/entities/responses";

import { apiPrefixNotes } from "@src/api/notes";

export const postCreateNote = async (): Promise<PostCreateNoteResponse> => {
  try {
    return await fetch(`${apiPrefixNotes}/`, { method: "POST" });
  } catch (e) {
    throw new Error(`Error creating note: ${e}.`);
  }
};
