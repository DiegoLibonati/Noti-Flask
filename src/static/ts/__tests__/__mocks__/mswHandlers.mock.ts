import { http, HttpResponse } from "msw";

import type { Note } from "@/types/app";
import type { ResponseWithData, ResponseWithRedirect } from "@/types/responses";

import { mockNotes } from "@tests/__mocks__/note.mock";

const defaultRedirect: ResponseWithRedirect = {
  code: "200",
  message: "OK",
  redirect_to: "/views/v1/app/home",
};

const defaultNotesPayload: ResponseWithData<Note[]> = {
  code: "200",
  message: "OK",
  data: mockNotes,
};

export const mockMswHandlers = [
  http.get("*/api/v1/auth/logout", () => {
    return HttpResponse.json(defaultRedirect);
  }),
  http.post("*/api/v1/auth/login", () => {
    return HttpResponse.json(defaultRedirect);
  }),
  http.post("*/api/v1/auth/sign_up", () => {
    return HttpResponse.json(defaultRedirect, { status: 201 });
  }),
  http.get("*/api/v1/notes/", () => {
    return HttpResponse.json(defaultNotesPayload);
  }),
  http.post("*/api/v1/notes/", () => {
    return HttpResponse.json(defaultRedirect, { status: 201 });
  }),
  http.delete("*/api/v1/notes/:id", () => {
    return HttpResponse.json(defaultRedirect);
  }),
  http.patch("*/api/v1/notes/:id", () => {
    return HttpResponse.json(defaultRedirect);
  }),
];
