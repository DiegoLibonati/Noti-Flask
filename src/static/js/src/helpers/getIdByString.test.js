import { getIdByString } from "./getIdByString.js";

describe("getIdByString.js", () => {
  describe("General Tests.", () => {
    test("It must return the last string of a string joined by separators.", () => {
      const id = "alert-2";

      const idByString = getIdByString(id, "-");

      expect(idByString).toEqual("2");
    });
  });
});
