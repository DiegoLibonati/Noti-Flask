import type { Note } from "@/types/app";

export const mockNote: Note = {
  id: 1,
  content: "Test note",
  created_at: "2026-01-01T00:00:00",
};

export const mockNotes: Note[] = [mockNote];
