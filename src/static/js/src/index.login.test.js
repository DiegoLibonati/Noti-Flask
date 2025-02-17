import { screen, within } from "@testing-library/dom";

import { getInputById } from "./helpers/getInputById.js";

import { BODY_LOGIN } from "./tests/jest.constants.js";

describe("Login Page", () => {
  describe("General Tests.", () => {
    beforeEach(() => {
      document.body.innerHTML = BODY_LOGIN;

      require("./index.js");
      document.dispatchEvent(new Event("DOMContentLoaded"));
    });

    afterEach(() => {
      document.body.innerHTML = "";
    });

    test("It must render the main.", () => {
      const main = screen.getByRole("main");

      expect(main).toBeInTheDocument();
      expect(main).toHaveClass(
        "c-main-login o-main o-main-center o-main-secondary"
      );
    });

    test("It must render the login form with the login elements.", () => {
      const form = document.querySelector(".qa-form-login");

      const formHeading = within(form).getByRole("heading", {
        name: /member login/i,
      });
      const formInputs = document.querySelectorAll(".qa-input");
      const formInputUsername = getInputById("username");
      const formInputPassword = getInputById("password");
      const formLoginBtn = within(form).getByRole("button", { name: /login/i });
      const formCreateAnAccount = within(form).getByRole("link", {
        name: /create an account/i,
      });
      const formLogo = document.querySelector(".qa-form-icon");

      expect(form).toBeInTheDocument();
      expect(form).toHaveClass("c-form-auth c-form-auth-login");
      expect(formHeading).toBeInTheDocument();
      expect(formInputUsername).toBeInTheDocument();
      expect(formInputPassword).toBeInTheDocument();
      expect(formLoginBtn).toBeInTheDocument();
      expect(formCreateAnAccount).toBeInTheDocument();
      expect(formLogo).toBeInTheDocument();

      formInputs.forEach((formInput) => {
        expect(formInput).toBeInTheDocument();
      });
    });
  });
});
