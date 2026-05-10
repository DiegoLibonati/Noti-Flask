import { screen, waitFor } from "@testing-library/dom";
import userEvent from "@testing-library/user-event";

import type { ResponseWithRedirect } from "@/types/responses";

import authService from "@/services/authService";
import noteService from "@/services/noteService";

import "@/index";

const mockAuthService = jest.mocked(authService);
const mockNoteService = jest.mocked(noteService);

const mockRedirect: ResponseWithRedirect = {
  code: "200",
  message: "OK",
  redirect_to: "/dashboard",
};

const user = userEvent.setup();

jest.mock("@/services/authService", () => ({
  __esModule: true,
  default: {
    logout: jest.fn(),
    login: jest.fn(),
    register: jest.fn(),
  },
}));

jest.mock("@/services/noteService", () => ({
  __esModule: true,
  default: {
    create: jest.fn(),
    delete: jest.fn(),
    edit: jest.fn(),
    getAll: jest.fn(),
  },
}));

const dispatchDOMContentLoaded = (): void => {
  document.dispatchEvent(new Event("DOMContentLoaded"));
};

const buildNoteDom = (id: number): string => `
  <div id="note-${id}">
    <div>
      <div>
        <button class="js-btn-edit-note">Edit</button>
        <button class="js-btn-confirm-edit-note">Confirm</button>
        <button class="js-btn-delete-note">Delete</button>
      </div>
    </div>
    <textarea class="js-text-area" disabled></textarea>
  </div>
`;

describe("index", () => {
  afterEach(() => {
    document.body.innerHTML = "";
  });

  describe("onClickCloseAlert", () => {
    it("should remove the alert matching the button id", async () => {
      document.body.innerHTML = `
        <button class="js-close-alert" id="close-alert-1">X</button>
        <li class="js-alert" id="alert-1">Alert message</li>
      `;
      dispatchDOMContentLoaded();

      await user.click(screen.getByRole("button", { name: "X" }));

      expect(screen.queryByText("Alert message")).not.toBeInTheDocument();
    });

    it("should not remove an alert with a different id", async () => {
      document.body.innerHTML = `
        <button class="js-close-alert" id="close-alert-1">X</button>
        <li class="js-alert" id="alert-2">Other alert</li>
      `;
      dispatchDOMContentLoaded();

      await user.click(screen.getByRole("button", { name: "X" }));

      expect(screen.queryByText("Other alert")).toBeInTheDocument();
    });

    it("should remove only the matching alert when multiple alerts exist", async () => {
      document.body.innerHTML = `
        <button class="js-close-alert" id="close-alert-1">X</button>
        <li class="js-alert" id="alert-1">Alert 1</li>
        <li class="js-alert" id="alert-2">Alert 2</li>
      `;
      dispatchDOMContentLoaded();

      await user.click(screen.getByRole("button", { name: "X" }));

      expect(screen.queryByText("Alert 1")).not.toBeInTheDocument();
      expect(screen.queryByText("Alert 2")).toBeInTheDocument();
    });
  });

  describe("onClickOpenNavbar", () => {
    it("should add c-nav--open to the navbar", async () => {
      document.body.innerHTML = `
        <button class="js-open-navbar c-header__action--active">Open</button>
        <button class="js-close-navbar">Close</button>
        <nav class="js-navbar">Navbar</nav>
      `;
      dispatchDOMContentLoaded();

      await user.click(screen.getByRole("button", { name: "Open" }));

      expect(document.querySelector<HTMLElement>(".js-navbar")).toHaveClass(
        "c-nav--open"
      );
    });

    it("should remove c-header__action--active from the open button", async () => {
      document.body.innerHTML = `
        <button class="js-open-navbar c-header__action--active">Open</button>
        <button class="js-close-navbar">Close</button>
        <nav class="js-navbar">Navbar</nav>
      `;
      dispatchDOMContentLoaded();

      await user.click(screen.getByRole("button", { name: "Open" }));

      expect(screen.getByRole("button", { name: "Open" })).not.toHaveClass(
        "c-header__action--active"
      );
    });

    it("should add c-header__action--active to the close button", async () => {
      document.body.innerHTML = `
        <button class="js-open-navbar c-header__action--active">Open</button>
        <button class="js-close-navbar">Close</button>
        <nav class="js-navbar">Navbar</nav>
      `;
      dispatchDOMContentLoaded();

      await user.click(screen.getByRole("button", { name: "Open" }));

      expect(screen.getByRole("button", { name: "Close" })).toHaveClass(
        "c-header__action--active"
      );
    });
  });

  describe("onClickCloseNavbar", () => {
    it("should remove c-nav--open from the navbar", async () => {
      document.body.innerHTML = `
        <button class="js-open-navbar">Open</button>
        <button class="js-close-navbar c-header__action--active">Close</button>
        <nav class="js-navbar c-nav--open">Navbar</nav>
      `;
      dispatchDOMContentLoaded();

      await user.click(screen.getByRole("button", { name: "Close" }));

      expect(document.querySelector<HTMLElement>(".js-navbar")).not.toHaveClass(
        "c-nav--open"
      );
    });

    it("should remove c-header__action--active from the close button", async () => {
      document.body.innerHTML = `
        <button class="js-open-navbar">Open</button>
        <button class="js-close-navbar c-header__action--active">Close</button>
        <nav class="js-navbar c-nav--open">Navbar</nav>
      `;
      dispatchDOMContentLoaded();

      await user.click(screen.getByRole("button", { name: "Close" }));

      expect(screen.getByRole("button", { name: "Close" })).not.toHaveClass(
        "c-header__action--active"
      );
    });

    it("should add c-header__action--active to the open button", async () => {
      document.body.innerHTML = `
        <button class="js-open-navbar">Open</button>
        <button class="js-close-navbar c-header__action--active">Close</button>
        <nav class="js-navbar c-nav--open">Navbar</nav>
      `;
      dispatchDOMContentLoaded();

      await user.click(screen.getByRole("button", { name: "Close" }));

      expect(screen.getByRole("button", { name: "Open" })).toHaveClass(
        "c-header__action--active"
      );
    });
  });

  describe("onClickAddNote", () => {
    it("should call noteService.create with an empty string", async () => {
      mockNoteService.create.mockResolvedValue(mockRedirect);
      document.body.innerHTML = `<button class="js-btn-add-note">Add</button>`;
      dispatchDOMContentLoaded();

      await user.click(screen.getByRole("button", { name: "Add" }));

      await waitFor(() => {
        expect(mockNoteService.create).toHaveBeenCalledWith("");
      });
    });
  });

  describe("onClickEditNote", () => {
    it("should remove the disabled attribute from the textarea", async () => {
      document.body.innerHTML = buildNoteDom(1);
      dispatchDOMContentLoaded();

      await user.click(screen.getByRole("button", { name: "Edit" }));

      expect(
        document.querySelector<HTMLTextAreaElement>(".js-text-area")
      ).not.toHaveAttribute("disabled");
    });

    it("should add is-hidden to the edit button", async () => {
      document.body.innerHTML = buildNoteDom(1);
      dispatchDOMContentLoaded();

      await user.click(screen.getByRole("button", { name: "Edit" }));

      expect(screen.getByRole("button", { name: "Edit" })).toHaveClass(
        "is-hidden"
      );
    });

    it("should add is-visible to the confirm button", async () => {
      document.body.innerHTML = buildNoteDom(1);
      dispatchDOMContentLoaded();

      await user.click(screen.getByRole("button", { name: "Edit" }));

      expect(screen.getByRole("button", { name: "Confirm" })).toHaveClass(
        "is-visible"
      );
    });
  });

  describe("onClickConfirmEditNote", () => {
    it("should call noteService.edit with the note id and trimmed content", async () => {
      mockNoteService.edit.mockResolvedValue(mockRedirect);
      document.body.innerHTML = buildNoteDom(1);
      const textarea =
        document.querySelector<HTMLTextAreaElement>(".js-text-area");
      if (textarea) textarea.value = "  Updated content  ";
      dispatchDOMContentLoaded();

      await user.click(screen.getByRole("button", { name: "Confirm" }));

      await waitFor(() => {
        expect(mockNoteService.edit).toHaveBeenCalledWith(1, "Updated content");
      });
    });

    it("should add the disabled attribute back to the textarea", async () => {
      mockNoteService.edit.mockResolvedValue(mockRedirect);
      document.body.innerHTML = buildNoteDom(1);
      const textarea =
        document.querySelector<HTMLTextAreaElement>(".js-text-area");
      if (textarea) textarea.value = "Some content";
      dispatchDOMContentLoaded();

      await user.click(screen.getByRole("button", { name: "Confirm" }));

      expect(
        document.querySelector<HTMLTextAreaElement>(".js-text-area")
      ).toHaveAttribute("disabled");
    });

    it("should remove is-visible from the confirm button", async () => {
      mockNoteService.edit.mockResolvedValue(mockRedirect);
      document.body.innerHTML = buildNoteDom(1);
      const editBtn =
        document.querySelector<HTMLButtonElement>(".js-btn-edit-note");
      const confirmBtn = document.querySelector<HTMLButtonElement>(
        ".js-btn-confirm-edit-note"
      );
      if (editBtn) editBtn.classList.add("is-hidden");
      if (confirmBtn) confirmBtn.classList.add("is-visible");
      const textarea =
        document.querySelector<HTMLTextAreaElement>(".js-text-area");
      if (textarea) textarea.value = "Some content";
      dispatchDOMContentLoaded();

      await user.click(screen.getByRole("button", { name: "Confirm" }));

      expect(screen.getByRole("button", { name: "Confirm" })).not.toHaveClass(
        "is-visible"
      );
    });

    it("should remove is-hidden from the edit button", async () => {
      mockNoteService.edit.mockResolvedValue(mockRedirect);
      document.body.innerHTML = buildNoteDom(1);
      const editBtn =
        document.querySelector<HTMLButtonElement>(".js-btn-edit-note");
      if (editBtn) editBtn.classList.add("is-hidden");
      const textarea =
        document.querySelector<HTMLTextAreaElement>(".js-text-area");
      if (textarea) textarea.value = "Some content";
      dispatchDOMContentLoaded();

      await user.click(screen.getByRole("button", { name: "Confirm" }));

      expect(screen.getByRole("button", { name: "Edit" })).not.toHaveClass(
        "is-hidden"
      );
    });

    it("should not call noteService.edit when content is empty after trimming", async () => {
      document.body.innerHTML = buildNoteDom(1);
      const textarea =
        document.querySelector<HTMLTextAreaElement>(".js-text-area");
      if (textarea) textarea.value = "   ";
      dispatchDOMContentLoaded();

      await user.click(screen.getByRole("button", { name: "Confirm" }));

      await waitFor(() => {
        expect(mockNoteService.edit).not.toHaveBeenCalled();
      });
    });

    it("should not call noteService.edit when the note id is not a number", async () => {
      document.body.innerHTML = buildNoteDom(1).replace(
        'id="note-1"',
        'id="note-invalid"'
      );
      const textarea =
        document.querySelector<HTMLTextAreaElement>(".js-text-area");
      if (textarea) textarea.value = "Some content";
      dispatchDOMContentLoaded();

      await user.click(screen.getByRole("button", { name: "Confirm" }));

      await waitFor(() => {
        expect(mockNoteService.edit).not.toHaveBeenCalled();
      });
    });
  });

  describe("onClickDeleteNote", () => {
    it("should call noteService.delete with the note id", async () => {
      mockNoteService.delete.mockResolvedValue(mockRedirect);
      document.body.innerHTML = buildNoteDom(5);
      dispatchDOMContentLoaded();

      await user.click(screen.getByRole("button", { name: "Delete" }));

      await waitFor(() => {
        expect(mockNoteService.delete).toHaveBeenCalledWith(5);
      });
    });

    it("should not call noteService.delete when the note id is not a number", async () => {
      document.body.innerHTML = buildNoteDom(1).replace(
        'id="note-1"',
        'id="note-invalid"'
      );
      dispatchDOMContentLoaded();

      await user.click(screen.getByRole("button", { name: "Delete" }));

      await waitFor(() => {
        expect(mockNoteService.delete).not.toHaveBeenCalled();
      });
    });
  });

  describe("onClickLogout", () => {
    it("should call authService.logout when the logout link is clicked", async () => {
      mockAuthService.logout.mockResolvedValue({ redirect_to: "/login" });
      document.body.innerHTML = `<a class="js-btn-logout" href="/logout">Logout</a>`;
      dispatchDOMContentLoaded();

      await user.click(screen.getByRole("link", { name: "Logout" }));

      await waitFor(() => {
        expect(mockAuthService.logout).toHaveBeenCalled();
      });
    });
  });

  describe("onSubmitLogin", () => {
    it("should call authService.login with the username and password from the form", async () => {
      mockAuthService.login.mockResolvedValue({ redirect_to: "/home" });
      document.body.innerHTML = `
        <form class="c-form-auth-login">
          <input id="username" type="text" />
          <input id="password" type="password" />
          <button type="submit">Login</button>
        </form>
      `;
      dispatchDOMContentLoaded();

      const usernameInput =
        document.querySelector<HTMLInputElement>("#username");
      const passwordInput =
        document.querySelector<HTMLInputElement>("#password");
      if (usernameInput) await user.type(usernameInput, "testuser");
      if (passwordInput) await user.type(passwordInput, "testpass");
      await user.click(screen.getByRole("button", { name: "Login" }));

      await waitFor(() => {
        expect(mockAuthService.login).toHaveBeenCalledWith(
          "testuser",
          "testpass"
        );
      });
    });

    it("should call authService.login with empty strings when inputs are blank", async () => {
      mockAuthService.login.mockResolvedValue({ redirect_to: "/home" });
      document.body.innerHTML = `
        <form class="c-form-auth-login">
          <input id="username" type="text" />
          <input id="password" type="password" />
          <button type="submit">Login</button>
        </form>
      `;
      dispatchDOMContentLoaded();

      await user.click(screen.getByRole("button", { name: "Login" }));

      await waitFor(() => {
        expect(mockAuthService.login).toHaveBeenCalledWith("", "");
      });
    });
  });

  describe("onSubmitRegister", () => {
    it("should call authService.register with username, password, and email from the form", async () => {
      mockAuthService.register.mockResolvedValue({ redirect_to: "/home" });
      document.body.innerHTML = `
        <form class="c-form-auth-register">
          <input id="username" type="text" />
          <input id="password" type="password" />
          <input id="email" type="email" />
          <button type="submit">Register</button>
        </form>
      `;
      dispatchDOMContentLoaded();

      const usernameInput =
        document.querySelector<HTMLInputElement>("#username");
      const passwordInput =
        document.querySelector<HTMLInputElement>("#password");
      const emailInput = document.querySelector<HTMLInputElement>("#email");
      if (usernameInput) await user.type(usernameInput, "testuser");
      if (passwordInput) await user.type(passwordInput, "testpass");
      if (emailInput) await user.type(emailInput, "test@example.com");
      await user.click(screen.getByRole("button", { name: "Register" }));

      await waitFor(() => {
        expect(mockAuthService.register).toHaveBeenCalledWith(
          "testuser",
          "testpass",
          "test@example.com"
        );
      });
    });

    it("should call authService.register with empty strings when inputs are blank", async () => {
      mockAuthService.register.mockResolvedValue({ redirect_to: "/home" });
      document.body.innerHTML = `
        <form class="c-form-auth-register">
          <input id="username" type="text" />
          <input id="password" type="password" />
          <input id="email" type="email" />
          <button type="submit">Register</button>
        </form>
      `;
      dispatchDOMContentLoaded();

      await user.click(screen.getByRole("button", { name: "Register" }));

      await waitFor(() => {
        expect(mockAuthService.register).toHaveBeenCalledWith("", "", "");
      });
    });
  });
});
