import { getElements } from "./getElements.js";

import { BODY_ELEMENTS } from "../../tests/jest.constants.js";

describe("getElements.js", () => {
  describe("General Tests.", () => {
    beforeEach(() => {
      document.body.innerHTML = BODY_ELEMENTS;
    });

    afterEach(() => {
      document.body.innerHTML = "";
    });

    test("It must render the elements of the document that the 'getElements' function exports.", () => {
      const {
        addNoteBtn,
        alerts,
        closeAlertBtns,
        closeNavbarBtn,
        deleteNoteBtns,
        editConfirmNoteBtns,
        editNoteBtns,
        inputs,
        loginBtn,
        logoutBtn,
        navbar,
        openNavbarBtn,
        registerBtn,
      } = getElements();

      expect(addNoteBtn).toBeInTheDocument();
      expect(closeNavbarBtn).toBeInTheDocument();
      expect(loginBtn).toBeInTheDocument();
      expect(logoutBtn).toBeInTheDocument();
      expect(navbar).toBeInTheDocument();
      expect(openNavbarBtn).toBeInTheDocument();
      expect(registerBtn).toBeInTheDocument();

      alerts.forEach((alert) => {
        expect(alert).toBeInTheDocument();
      });

      closeAlertBtns.forEach((closeAlertBtn) => {
        expect(closeAlertBtn).toBeInTheDocument();
      });

      deleteNoteBtns.forEach((deleteNoteBtn) => {
        expect(deleteNoteBtn).toBeInTheDocument();
      });

      editConfirmNoteBtns.forEach((editConfirmNoteBtn) => {
        expect(editConfirmNoteBtn).toBeInTheDocument();
      });

      editNoteBtns.forEach((editNoteBtn) => {
        expect(editNoteBtn).toBeInTheDocument();
      });

      inputs.forEach((input) => {
        expect(input).toBeInTheDocument();
      });
    });
  });
});
