import type { Note } from "@/types/app";
import type { ResponseWithData, ResponseWithRedirect } from "@/types/responses";

import noteService from "@/services/noteService";

import { mockNotes } from "@tests/__mocks__/note.mock";

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

const mockFetchSuccess = (data: unknown): void => {
  global.fetch = jest.fn().mockResolvedValue({
    ok: true,
    json: async () => await data,
  });
};

const mockFetchError = (status: number): void => {
  global.fetch = jest.fn().mockResolvedValue({
    ok: false,
    status,
  });
};

const mockFetchNetworkError = (message = "Network error"): void => {
  global.fetch = jest.fn().mockRejectedValue(new Error(message));
};

describe("noteService", () => {
  afterEach(() => {
    jest.restoreAllMocks();
  });

  describe("getAll", () => {
    describe("when request succeeds", () => {
      it("should call fetch with the correct URL", async () => {
        mockFetchSuccess(mockNotesResponse);
        await noteService.getAll();
        expect(fetch).toHaveBeenCalledWith("/api/v1/notes/");
      });

      it("should return the parsed response with notes data", async () => {
        mockFetchSuccess(mockNotesResponse);
        const result = await noteService.getAll();
        expect(result).toEqual(mockNotesResponse);
      });

      it("should return an array of notes in the data field", async () => {
        mockFetchSuccess(mockNotesResponse);
        const result = await noteService.getAll();
        expect(result.data).toEqual(mockNotes);
      });
    });

    describe("when response is not ok", () => {
      it("should throw with the HTTP status on 500", async () => {
        mockFetchError(500);
        await expect(noteService.getAll()).rejects.toThrow(
          "HTTP error! status: 500"
        );
      });

      it("should throw with the HTTP status on 404", async () => {
        mockFetchError(404);
        await expect(noteService.getAll()).rejects.toThrow(
          "HTTP error! status: 404"
        );
      });
    });

    describe("when fetch fails with a network error", () => {
      it("should propagate the error", async () => {
        mockFetchNetworkError();
        await expect(noteService.getAll()).rejects.toThrow("Network error");
      });
    });
  });

  describe("create", () => {
    describe("when request succeeds", () => {
      it("should call fetch with the correct URL, method, and body", async () => {
        mockFetchSuccess(mockRedirectResponse);
        await noteService.create("my note content");
        expect(fetch).toHaveBeenCalledWith("/api/v1/notes/", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ content: "my note content" }),
        });
      });

      it("should return the redirect response", async () => {
        mockFetchSuccess(mockRedirectResponse);
        const result = await noteService.create("my note content");
        expect(result).toEqual(mockRedirectResponse);
      });

      it("should send an empty string as content", async () => {
        mockFetchSuccess(mockRedirectResponse);
        await noteService.create("");
        expect(fetch).toHaveBeenCalledWith("/api/v1/notes/", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ content: "" }),
        });
      });
    });

    describe("when response is not ok", () => {
      it("should throw with the HTTP status on 400", async () => {
        mockFetchError(400);
        await expect(noteService.create("content")).rejects.toThrow(
          "HTTP error! status: 400"
        );
      });

      it("should throw with the HTTP status on 500", async () => {
        mockFetchError(500);
        await expect(noteService.create("content")).rejects.toThrow(
          "HTTP error! status: 500"
        );
      });
    });

    describe("when fetch fails with a network error", () => {
      it("should propagate the error", async () => {
        mockFetchNetworkError();
        await expect(noteService.create("content")).rejects.toThrow(
          "Network error"
        );
      });
    });
  });

  describe("delete", () => {
    describe("when request succeeds", () => {
      it("should call fetch with the correct URL and method", async () => {
        mockFetchSuccess(mockRedirectResponse);
        await noteService.delete(1);
        expect(fetch).toHaveBeenCalledWith("/api/v1/notes//1", {
          method: "DELETE",
        });
      });

      it("should return the redirect response", async () => {
        mockFetchSuccess(mockRedirectResponse);
        const result = await noteService.delete(1);
        expect(result).toEqual(mockRedirectResponse);
      });
    });

    describe("when response is not ok", () => {
      it("should throw with the HTTP status on 404", async () => {
        mockFetchError(404);
        await expect(noteService.delete(999)).rejects.toThrow(
          "HTTP error! status: 404"
        );
      });

      it("should throw with the HTTP status on 403", async () => {
        mockFetchError(403);
        await expect(noteService.delete(1)).rejects.toThrow(
          "HTTP error! status: 403"
        );
      });
    });

    describe("when fetch fails with a network error", () => {
      it("should propagate the error", async () => {
        mockFetchNetworkError();
        await expect(noteService.delete(1)).rejects.toThrow("Network error");
      });
    });
  });

  describe("edit", () => {
    describe("when request succeeds", () => {
      it("should call fetch with the correct URL, method, and body", async () => {
        mockFetchSuccess(mockRedirectResponse);
        await noteService.edit(1, "updated content");
        expect(fetch).toHaveBeenCalledWith("/api/v1/notes//1", {
          method: "PATCH",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ content: "updated content" }),
        });
      });

      it("should return the redirect response", async () => {
        mockFetchSuccess(mockRedirectResponse);
        const result = await noteService.edit(1, "updated content");
        expect(result).toEqual(mockRedirectResponse);
      });
    });

    describe("when response is not ok", () => {
      it("should throw with the HTTP status on 403", async () => {
        mockFetchError(403);
        await expect(noteService.edit(1, "content")).rejects.toThrow(
          "HTTP error! status: 403"
        );
      });

      it("should throw with the HTTP status on 404", async () => {
        mockFetchError(404);
        await expect(noteService.edit(999, "content")).rejects.toThrow(
          "HTTP error! status: 404"
        );
      });
    });

    describe("when fetch fails with a network error", () => {
      it("should propagate the error", async () => {
        mockFetchNetworkError();
        await expect(noteService.edit(1, "content")).rejects.toThrow(
          "Network error"
        );
      });
    });
  });
});
