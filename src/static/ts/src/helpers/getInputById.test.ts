import { getInputById } from "@src/helpers/getInputById";

import { BODY_ELEMENTS } from "@tests/jest.constants";

describe("getInputById.js", () => {
  describe("General Tests.", () => {
    beforeEach(() => {
      document.body.innerHTML = BODY_ELEMENTS;
    });

    afterEach(() => {
      document.body.innerHTML = "";
    });

    test("It must return the username input.", () => {
      const id = "username";

      const input = getInputById(id);

      expect(input).toBeInTheDocument();
    });

    test("It must NOT return the pepe input because not exists in document.", () => {
        const id = "pepe";
  
        const input = getInputById(id);
  
        expect(input).toBeUndefined()
      });
  });
});