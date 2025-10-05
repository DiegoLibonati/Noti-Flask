import { screen } from "@testing-library/dom";

import { BODY_HOME } from "@tests/jest.constants";

describe("Home Page", () => {
  describe("General Tests.", () => {
    beforeEach(() => {
      document.body.innerHTML = BODY_HOME;

      require("./index.ts");
      document.dispatchEvent(new Event("DOMContentLoaded"));
    });

    afterEach(() => {
      document.body.innerHTML = "";
    });

    test("It must render the main.", () => {
      const main = screen.getByRole("main");

      expect(main).toBeInTheDocument();
      expect(main).toHaveClass(
        "o-main o-main-app"
      );
    });
  });
});
