import * as Undici from "undici";

const baseOrigin = "http://localhost";

const resolveUrl = (input: unknown): unknown => {
  if (typeof input === "string" && input.startsWith("/")) {
    return `${baseOrigin}${input}`;
  }
  if (input instanceof URL) {
    return input;
  }
  return input;
};

const fetchWithRelativeUrlSupport = ((
  input: Parameters<typeof Undici.fetch>[0],
  init?: Parameters<typeof Undici.fetch>[1]
) => {
  return Undici.fetch(
    resolveUrl(input) as Parameters<typeof Undici.fetch>[0],
    init
  );
}) as typeof Undici.fetch;

Object.defineProperties(globalThis, {
  fetch: {
    value: fetchWithRelativeUrlSupport,
    writable: true,
    configurable: true,
  },
  FormData: { value: Undici.FormData, writable: true, configurable: true },
  Headers: { value: Undici.Headers, writable: true, configurable: true },
  Request: { value: Undici.Request, writable: true, configurable: true },
  Response: { value: Undici.Response, writable: true, configurable: true },
});
