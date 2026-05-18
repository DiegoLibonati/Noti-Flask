import "@testing-library/jest-dom";

import { mockMswServer } from "@tests/__mocks__/mswServer.mock";

const originalConsoleError = console.error.bind(console);

console.error = (...args: Parameters<typeof console.error>): void => {
  const err = args[0] as { type?: string; message?: string };
  if (err.type === "not implemented" && err.message?.includes("navigation"))
    return;
  originalConsoleError(...args);
};

beforeAll((): void => {
  mockMswServer.listen({ onUnhandledRequest: "error" });
});

afterEach((): void => {
  mockMswServer.resetHandlers();
});

afterAll((): void => {
  mockMswServer.close();
});
