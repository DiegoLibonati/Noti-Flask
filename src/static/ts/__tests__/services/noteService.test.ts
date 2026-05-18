import { http, HttpResponse } from "msw";

import type { Note } from "@/types/app";
import type { ResponseWithData, ResponseWithRedirect } from "@/types/responses";

import noteService from "@/services/noteService";

import { mockNotes } from "@tests/__mocks__/note.mock";
import { mockMswServer } from "@tests/__mocks__/mswServer.mock";

const mockRedirectResponse: ResponseWithRedirect = {
  code: "200",
  message: "Success",
  redirect_to: "/notes",
};

const mockNotesResponse: ResponseWithData<Note[]> = {
  code: "200",
  message: "Success",
  data: mockNotes,
};

describe("noteService", () => {
  describe("getAll", () => {
    describe("when request succeeds", () => {
      it("should hit GET /api/v1/notes/", async () => {
        let capturedPath: string | undefined;
        let capturedMethod: string | undefined;

        mockMswServer.use(
          http.get("*/api/v1/notes/", ({ request }) => {
            capturedPath = new URL(request.url).pathname;
            capturedMethod = request.method;
            return HttpResponse.json(mockNotesResponse);
          })
        );

        await noteService.getAll();

        expect(capturedPath).toBe("/api/v1/notes/");
        expect(capturedMethod).toBe("GET");
      });

      it("should return the parsed response with notes data", async () => {
        mockMswServer.use(
          http.get("*/api/v1/notes/", () =>
            HttpResponse.json(mockNotesResponse)
          )
        );

        const result = await noteService.getAll();

        expect(result).toEqual(mockNotesResponse);
      });

      it("should return an array of notes in the data field", async () => {
        mockMswServer.use(
          http.get("*/api/v1/notes/", () =>
            HttpResponse.json(mockNotesResponse)
          )
        );

        const result = await noteService.getAll();

        expect(result.data).toEqual(mockNotes);
      });
    });

    describe("when response is not ok", () => {
      it.each([500, 404])(
        "should throw with HTTP status %s",
        async (status: number) => {
          mockMswServer.use(
            http.get(
              "*/api/v1/notes/",
              () => new HttpResponse(null, { status })
            )
          );

          await expect(noteService.getAll()).rejects.toThrow(
            `HTTP error! status: ${status}`
          );
        }
      );
    });

    describe("when fetch fails with a network error", () => {
      it("should propagate the error", async () => {
        mockMswServer.use(
          http.get("*/api/v1/notes/", () => HttpResponse.error())
        );

        await expect(noteService.getAll()).rejects.toThrow();
      });
    });
  });

  describe("create", () => {
    describe("when request succeeds", () => {
      it("should send POST to /api/v1/notes/ with the content body", async () => {
        let capturedPath: string | undefined;
        let capturedMethod: string | undefined;
        let capturedBody: unknown;
        let capturedContentType: string | null | undefined;

        mockMswServer.use(
          http.post("*/api/v1/notes/", async ({ request }) => {
            capturedPath = new URL(request.url).pathname;
            capturedMethod = request.method;
            capturedContentType = request.headers.get("content-type");
            capturedBody = await request.json();
            return HttpResponse.json(mockRedirectResponse, { status: 201 });
          })
        );

        await noteService.create("my note content");

        expect(capturedPath).toBe("/api/v1/notes/");
        expect(capturedMethod).toBe("POST");
        expect(capturedContentType).toContain("application/json");
        expect(capturedBody).toEqual({ content: "my note content" });
      });

      it("should return the redirect response", async () => {
        mockMswServer.use(
          http.post("*/api/v1/notes/", () =>
            HttpResponse.json(mockRedirectResponse, { status: 201 })
          )
        );

        const result = await noteService.create("my note content");

        expect(result).toEqual(mockRedirectResponse);
      });

      it("should send an empty string as content", async () => {
        let capturedBody: unknown;

        mockMswServer.use(
          http.post("*/api/v1/notes/", async ({ request }) => {
            capturedBody = await request.json();
            return HttpResponse.json(mockRedirectResponse, { status: 201 });
          })
        );

        await noteService.create("");

        expect(capturedBody).toEqual({ content: "" });
      });
    });

    describe("when response is not ok", () => {
      it.each([400, 500])(
        "should throw with HTTP status %s",
        async (status: number) => {
          mockMswServer.use(
            http.post(
              "*/api/v1/notes/",
              () => new HttpResponse(null, { status })
            )
          );

          await expect(noteService.create("content")).rejects.toThrow(
            `HTTP error! status: ${status}`
          );
        }
      );
    });

    describe("when fetch fails with a network error", () => {
      it("should propagate the error", async () => {
        mockMswServer.use(
          http.post("*/api/v1/notes/", () => HttpResponse.error())
        );

        await expect(noteService.create("content")).rejects.toThrow();
      });
    });
  });

  describe("delete", () => {
    describe("when request succeeds", () => {
      it("should send DELETE to /api/v1/notes/:id with the id in the path", async () => {
        let capturedPath: string | undefined;
        let capturedMethod: string | undefined;
        let capturedIdParam: string | undefined;

        mockMswServer.use(
          http.delete("*/api/v1/notes/:id", ({ request, params }) => {
            capturedPath = new URL(request.url).pathname;
            capturedMethod = request.method;
            capturedIdParam = params.id as string;
            return HttpResponse.json(mockRedirectResponse);
          })
        );

        await noteService.delete(1);

        expect(capturedPath).toBe("/api/v1/notes/1");
        expect(capturedMethod).toBe("DELETE");
        expect(capturedIdParam).toBe("1");
      });

      it("should return the redirect response", async () => {
        mockMswServer.use(
          http.delete("*/api/v1/notes/:id", () =>
            HttpResponse.json(mockRedirectResponse)
          )
        );

        const result = await noteService.delete(1);

        expect(result).toEqual(mockRedirectResponse);
      });
    });

    describe("when response is not ok", () => {
      it.each([404, 403])(
        "should throw with HTTP status %s",
        async (status: number) => {
          mockMswServer.use(
            http.delete(
              "*/api/v1/notes/:id",
              () => new HttpResponse(null, { status })
            )
          );

          await expect(noteService.delete(1)).rejects.toThrow(
            `HTTP error! status: ${status}`
          );
        }
      );
    });

    describe("when fetch fails with a network error", () => {
      it("should propagate the error", async () => {
        mockMswServer.use(
          http.delete("*/api/v1/notes/:id", () => HttpResponse.error())
        );

        await expect(noteService.delete(1)).rejects.toThrow();
      });
    });
  });

  describe("edit", () => {
    describe("when request succeeds", () => {
      it("should send PATCH to /api/v1/notes/:id with the content body", async () => {
        let capturedPath: string | undefined;
        let capturedMethod: string | undefined;
        let capturedIdParam: string | undefined;
        let capturedBody: unknown;

        mockMswServer.use(
          http.patch("*/api/v1/notes/:id", async ({ request, params }) => {
            capturedPath = new URL(request.url).pathname;
            capturedMethod = request.method;
            capturedIdParam = params.id as string;
            capturedBody = await request.json();
            return HttpResponse.json(mockRedirectResponse);
          })
        );

        await noteService.edit(1, "updated content");

        expect(capturedPath).toBe("/api/v1/notes/1");
        expect(capturedMethod).toBe("PATCH");
        expect(capturedIdParam).toBe("1");
        expect(capturedBody).toEqual({ content: "updated content" });
      });

      it("should return the redirect response", async () => {
        mockMswServer.use(
          http.patch("*/api/v1/notes/:id", () =>
            HttpResponse.json(mockRedirectResponse)
          )
        );

        const result = await noteService.edit(1, "updated content");

        expect(result).toEqual(mockRedirectResponse);
      });
    });

    describe("when response is not ok", () => {
      it.each([403, 404])(
        "should throw with HTTP status %s",
        async (status: number) => {
          mockMswServer.use(
            http.patch(
              "*/api/v1/notes/:id",
              () => new HttpResponse(null, { status })
            )
          );

          await expect(noteService.edit(1, "content")).rejects.toThrow(
            `HTTP error! status: ${status}`
          );
        }
      );
    });

    describe("when fetch fails with a network error", () => {
      it("should propagate the error", async () => {
        mockMswServer.use(
          http.patch("*/api/v1/notes/:id", () => HttpResponse.error())
        );

        await expect(noteService.edit(1, "content")).rejects.toThrow();
      });
    });
  });
});
