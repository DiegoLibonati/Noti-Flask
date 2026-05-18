import { http, HttpResponse } from "msw";

import type { ResponseWithRedirect } from "@/types/responses";

import authService from "@/services/authService";

import { mockMswServer } from "@tests/__mocks__/mswServer.mock";

const mockRedirectResponse: Partial<ResponseWithRedirect> = {
  code: "200",
  message: "Success",
  redirect_to: "/dashboard",
};

describe("authService", () => {
  describe("logout", () => {
    describe("when request succeeds", () => {
      it("should hit GET /api/v1/auth/logout", async () => {
        let capturedUrl: string | undefined;
        let capturedMethod: string | undefined;

        mockMswServer.use(
          http.get("*/api/v1/auth/logout", ({ request }) => {
            capturedUrl = new URL(request.url).pathname;
            capturedMethod = request.method;
            return HttpResponse.json(mockRedirectResponse);
          })
        );

        await authService.logout();

        expect(capturedUrl).toBe("/api/v1/auth/logout");
        expect(capturedMethod).toBe("GET");
      });

      it("should return the parsed JSON response", async () => {
        mockMswServer.use(
          http.get("*/api/v1/auth/logout", () =>
            HttpResponse.json(mockRedirectResponse)
          )
        );

        const result = await authService.logout();

        expect(result).toEqual(mockRedirectResponse);
      });

      it("should return a partial response without redirect_to", async () => {
        const partialResponse: Partial<ResponseWithRedirect> = {
          code: "200",
          message: "OK",
        };
        mockMswServer.use(
          http.get("*/api/v1/auth/logout", () =>
            HttpResponse.json(partialResponse)
          )
        );

        const result = await authService.logout();

        expect(result).toEqual(partialResponse);
      });
    });

    describe("when fetch fails with a network error", () => {
      it("should propagate the error", async () => {
        mockMswServer.use(
          http.get("*/api/v1/auth/logout", () => HttpResponse.error())
        );

        await expect(authService.logout()).rejects.toThrow();
      });
    });
  });

  describe("login", () => {
    describe("when request succeeds", () => {
      it("should send POST with JSON body containing username and password", async () => {
        let capturedBody: unknown;
        let capturedMethod: string | undefined;
        let capturedContentType: string | null | undefined;

        mockMswServer.use(
          http.post("*/api/v1/auth/login", async ({ request }) => {
            capturedBody = await request.json();
            capturedMethod = request.method;
            capturedContentType = request.headers.get("content-type");
            return HttpResponse.json(mockRedirectResponse);
          })
        );

        await authService.login("testuser", "testpass");

        expect(capturedMethod).toBe("POST");
        expect(capturedContentType).toContain("application/json");
        expect(capturedBody).toEqual({
          username: "testuser",
          password: "testpass",
        });
      });

      it("should return the parsed JSON response", async () => {
        mockMswServer.use(
          http.post("*/api/v1/auth/login", () =>
            HttpResponse.json(mockRedirectResponse)
          )
        );

        const result = await authService.login("testuser", "testpass");

        expect(result).toEqual(mockRedirectResponse);
      });

      it("should send empty strings when credentials are empty", async () => {
        let capturedBody: unknown;

        mockMswServer.use(
          http.post("*/api/v1/auth/login", async ({ request }) => {
            capturedBody = await request.json();
            return HttpResponse.json(mockRedirectResponse);
          })
        );

        await authService.login("", "");

        expect(capturedBody).toEqual({ username: "", password: "" });
      });
    });

    describe("when fetch fails with a network error", () => {
      it("should propagate the error", async () => {
        mockMswServer.use(
          http.post("*/api/v1/auth/login", () => HttpResponse.error())
        );

        await expect(
          authService.login("testuser", "testpass")
        ).rejects.toThrow();
      });
    });
  });

  describe("register", () => {
    describe("when request succeeds", () => {
      it("should send POST to /api/v1/auth/sign_up with username, password and email", async () => {
        let capturedBody: unknown;
        let capturedPath: string | undefined;
        let capturedMethod: string | undefined;

        mockMswServer.use(
          http.post("*/api/v1/auth/sign_up", async ({ request }) => {
            capturedBody = await request.json();
            capturedPath = new URL(request.url).pathname;
            capturedMethod = request.method;
            return HttpResponse.json(mockRedirectResponse, { status: 201 });
          })
        );

        await authService.register("testuser", "testpass", "test@example.com");

        expect(capturedPath).toBe("/api/v1/auth/sign_up");
        expect(capturedMethod).toBe("POST");
        expect(capturedBody).toEqual({
          username: "testuser",
          password: "testpass",
          email: "test@example.com",
        });
      });

      it("should return the parsed JSON response", async () => {
        mockMswServer.use(
          http.post("*/api/v1/auth/sign_up", () =>
            HttpResponse.json(mockRedirectResponse, { status: 201 })
          )
        );

        const result = await authService.register(
          "testuser",
          "testpass",
          "test@example.com"
        );

        expect(result).toEqual(mockRedirectResponse);
      });
    });

    describe("when fetch fails with a network error", () => {
      it("should propagate the error", async () => {
        mockMswServer.use(
          http.post("*/api/v1/auth/sign_up", () => HttpResponse.error())
        );

        await expect(
          authService.register("testuser", "testpass", "test@example.com")
        ).rejects.toThrow();
      });
    });
  });
});
