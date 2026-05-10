import type { ResponseWithRedirect } from "@/types/responses";

import authService from "@/services/authService";

const mockRedirectResponse: Partial<ResponseWithRedirect> = {
  code: "200",
  message: "Success",
  redirect_to: "/dashboard",
};

const mockFetchSuccess = (data: unknown): void => {
  global.fetch = jest.fn().mockResolvedValue({
    ok: true,
    json: async () => await data,
  });
};

const mockFetchNetworkError = (message = "Network error"): void => {
  global.fetch = jest.fn().mockRejectedValue(new Error(message));
};

describe("authService", () => {
  afterEach(() => {
    jest.restoreAllMocks();
  });

  describe("logout", () => {
    describe("when request succeeds", () => {
      it("should call fetch with the correct URL", async () => {
        mockFetchSuccess(mockRedirectResponse);
        await authService.logout();
        expect(fetch).toHaveBeenCalledWith("/api/v1/auth/logout");
      });

      it("should return the parsed JSON response", async () => {
        mockFetchSuccess(mockRedirectResponse);
        const result = await authService.logout();
        expect(result).toEqual(mockRedirectResponse);
      });

      it("should return a partial response without redirect_to", async () => {
        const partialResponse: Partial<ResponseWithRedirect> = {
          code: "200",
          message: "OK",
        };
        mockFetchSuccess(partialResponse);
        const result = await authService.logout();
        expect(result).toEqual(partialResponse);
      });
    });

    describe("when fetch fails with a network error", () => {
      it("should propagate the error", async () => {
        mockFetchNetworkError("Network error");
        await expect(authService.logout()).rejects.toThrow("Network error");
      });
    });
  });

  describe("login", () => {
    describe("when request succeeds", () => {
      it("should call fetch with the correct URL, method, and body", async () => {
        mockFetchSuccess(mockRedirectResponse);
        await authService.login("testuser", "testpass");
        expect(fetch).toHaveBeenCalledWith("/api/v1/auth/login", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ username: "testuser", password: "testpass" }),
        });
      });

      it("should return the parsed JSON response", async () => {
        mockFetchSuccess(mockRedirectResponse);
        const result = await authService.login("testuser", "testpass");
        expect(result).toEqual(mockRedirectResponse);
      });

      it("should send empty strings when credentials are empty", async () => {
        mockFetchSuccess(mockRedirectResponse);
        await authService.login("", "");
        expect(fetch).toHaveBeenCalledWith("/api/v1/auth/login", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ username: "", password: "" }),
        });
      });
    });

    describe("when fetch fails with a network error", () => {
      it("should propagate the error", async () => {
        mockFetchNetworkError();
        await expect(authService.login("testuser", "testpass")).rejects.toThrow(
          "Network error"
        );
      });
    });
  });

  describe("register", () => {
    describe("when request succeeds", () => {
      it("should call fetch with the correct URL, method, and body", async () => {
        mockFetchSuccess(mockRedirectResponse);
        await authService.register("testuser", "testpass", "test@example.com");
        expect(fetch).toHaveBeenCalledWith("/api/v1/auth/sign_up", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            username: "testuser",
            password: "testpass",
            email: "test@example.com",
          }),
        });
      });

      it("should return the parsed JSON response", async () => {
        mockFetchSuccess(mockRedirectResponse);
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
        mockFetchNetworkError();
        await expect(
          authService.register("testuser", "testpass", "test@example.com")
        ).rejects.toThrow("Network error");
      });
    });
  });
});
