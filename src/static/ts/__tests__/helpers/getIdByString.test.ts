import { getIdByString } from "@/helpers/getIdByString";

describe("getIdByString", () => {
  describe("when separator is found", () => {
    it("should return the last part after splitting", () => {
      expect(getIdByString("note-1", "-")).toBe("1");
    });

    it("should return the last part when multiple separators exist", () => {
      expect(getIdByString("close-alert-42", "-")).toBe("42");
    });

    it("should return the last part with a different separator", () => {
      expect(getIdByString("note/items/5", "/")).toBe("5");
    });

    it("should return an empty string when the string ends with the separator", () => {
      expect(getIdByString("note-", "-")).toBe("");
    });
  });

  describe("when separator is not found", () => {
    it("should return the whole string", () => {
      expect(getIdByString("note", "-")).toBe("note");
    });

    it("should return the whole string for a single character", () => {
      expect(getIdByString("1", "-")).toBe("1");
    });
  });

  describe("edge cases", () => {
    it("should return an empty string for an empty input", () => {
      expect(getIdByString("", "-")).toBe("");
    });

    it("should work with a multi-character separator", () => {
      expect(getIdByString("note--1", "--")).toBe("1");
    });
  });
});
