import { screen, within } from "@testing-library/dom";

import { getInputById } from "./helpers/getInputById.js";

import { BODY_REGISTER } from "../tests/jest.constants.js";

describe("Register Page", () => {
  describe("General Tests.", () => {
    beforeEach(() => {
      document.body.innerHTML = BODY_REGISTER;

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
        "c-main-register o-main o-main-center o-main-secondary"
      );
    });

    test("It must render the register form with the register elements.", () => {
      const form = document.querySelector(".qa-form-register");

      const formHeading = within(form).getByRole("heading", {
        name: /member register/i,
      });
      const formInputs = document.querySelectorAll(".qa-input");
      const formInputUsername = getInputById("username");
      const formInputPassword = getInputById("password");
      const formInputEmail = getInputById("email");
      const formRegisterBtn = within(form).getByRole("button", {
        name: /register/i,
      });
      const formDoYouAlreadyHaveAnAccount = within(form).getByRole("link", {
        name: /do you already have an account?/i,
      });
      const formLogo = document.querySelector(".qa-form-icon");

      expect(form).toBeInTheDocument();
      expect(form).toHaveClass("c-form-auth c-form-auth-register");
      expect(formHeading).toBeInTheDocument();
      expect(formInputUsername).toBeInTheDocument();
      expect(formInputPassword).toBeInTheDocument();
      expect(formInputEmail).toBeInTheDocument();
      expect(formRegisterBtn).toBeInTheDocument();
      expect(formDoYouAlreadyHaveAnAccount).toBeInTheDocument();
      expect(formLogo).toBeInTheDocument();

      formInputs.forEach((formInput) => {
        expect(formInput).toBeInTheDocument();
      });
    });
  });
});
