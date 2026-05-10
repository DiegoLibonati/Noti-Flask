import {
  classAlert,
  classBtnAddNote,
  classBtnConfirmEditNote,
  classBtnDeleteNote,
  classBtnEditNote,
  classBtnLogout,
  classCloseAlert,
  classCloseNavbar,
  classFormLogin,
  classFormRegister,
  classNavbar,
  classOpenNavbar,
  classTextArea,
} from "@/constants/vars";

import { getIdByString } from "@/helpers/getIdByString";

import authService from "@/services/authService";
import noteService from "@/services/noteService";

const registerEvents = (): void => {
  const closeNavbarBtn =
    document.querySelector<HTMLButtonElement>(classCloseNavbar);
  const closeAlertBtns =
    document.querySelectorAll<HTMLButtonElement>(classCloseAlert);
  const openNavbarBtn =
    document.querySelector<HTMLButtonElement>(classOpenNavbar);
  const addNoteBtn = document.querySelector<HTMLButtonElement>(classBtnAddNote);
  const editNoteBtns =
    document.querySelectorAll<HTMLButtonElement>(classBtnEditNote);
  const deleteNoteBtns =
    document.querySelectorAll<HTMLButtonElement>(classBtnDeleteNote);
  const editConfirmNoteBtns = document.querySelectorAll<HTMLButtonElement>(
    classBtnConfirmEditNote
  );

  const logoutBtn = document.querySelector<HTMLAnchorElement>(classBtnLogout);

  logoutBtn?.addEventListener("click", (e) => {
    e.preventDefault();
    void onClickLogout();
  });

  const loginForm = document.querySelector<HTMLFormElement>(classFormLogin);
  const registerForm =
    document.querySelector<HTMLFormElement>(classFormRegister);

  loginForm?.addEventListener("submit", (e) => {
    e.preventDefault();
    void onSubmitLogin(e);
  });
  registerForm?.addEventListener("submit", (e) => {
    e.preventDefault();
    void onSubmitRegister(e);
  });

  closeAlertBtns.forEach((btn) => {
    btn.addEventListener("click", onClickCloseAlert);
  });
  openNavbarBtn?.addEventListener("click", onClickOpenNavbar);
  closeNavbarBtn?.addEventListener("click", onClickCloseNavbar);
  addNoteBtn?.addEventListener("click", () => {
    void onClickAddNote();
  });
  editNoteBtns.forEach((btn) => {
    btn.addEventListener("click", onClickEditNote);
  });
  deleteNoteBtns.forEach((btn) => {
    btn.addEventListener("click", (e) => {
      void onClickDeleteNote(e);
    });
  });
  editConfirmNoteBtns.forEach((btn) => {
    btn.addEventListener("click", (e) => {
      void onClickConfirmEditNote(e);
    });
  });
};

const onClickCloseAlert = (e: Event): void => {
  const btn = e.currentTarget as HTMLButtonElement;
  const idAlertClicked = getIdByString(btn.id, "-");

  const alerts = document.querySelectorAll<HTMLLIElement>(classAlert);
  const alertClicked = Array.from(alerts).find(
    (alert) => getIdByString(alert.id, "-") === idAlertClicked
  );

  alertClicked?.remove();
};

const onClickOpenNavbar = (e: Event): void => {
  const btn = e.currentTarget as HTMLButtonElement;
  const navbar = document.querySelector<HTMLElement>(classNavbar);
  const closeNavbarBtn =
    document.querySelector<HTMLButtonElement>(classCloseNavbar);

  btn.classList.remove("c-header__action--active");
  closeNavbarBtn?.classList.add("c-header__action--active");
  navbar?.classList.add("c-nav--open");
};

const onClickCloseNavbar = (e: Event): void => {
  const btn = e.currentTarget as HTMLButtonElement;
  const navbar = document.querySelector<HTMLElement>(classNavbar);
  const openNavbarBtn =
    document.querySelector<HTMLButtonElement>(classOpenNavbar);

  btn.classList.remove("c-header__action--active");
  openNavbarBtn?.classList.add("c-header__action--active");
  navbar?.classList.remove("c-nav--open");
};

const onClickAddNote = async (): Promise<void> => {
  const response = await noteService.create("");
  window.location.href = response.redirect_to;
};

const onClickEditNote = (e: Event): void => {
  const btn = e.currentTarget as HTMLButtonElement;
  const noteRoot = btn.parentElement?.parentElement?.parentElement;
  const textArea = noteRoot?.querySelector<HTMLTextAreaElement>(classTextArea);
  const btnConfirmEdit = noteRoot?.querySelector<HTMLButtonElement>(
    classBtnConfirmEditNote
  );

  textArea?.removeAttribute("disabled");
  textArea?.focus();

  btn.classList.add("is-hidden");
  btnConfirmEdit?.classList.add("is-visible");
};

const onClickConfirmEditNote = async (e: Event): Promise<void> => {
  const btn = e.currentTarget as HTMLButtonElement;
  const noteRoot = btn.parentElement?.parentElement
    ?.parentElement as HTMLDivElement;
  const id = parseInt(getIdByString(noteRoot.id, "-"), 10);
  const textArea = noteRoot.querySelector<HTMLTextAreaElement>(classTextArea);
  const btnEdit = noteRoot.querySelector<HTMLButtonElement>(classBtnEditNote);
  const newContent = textArea?.value.trim();

  textArea?.setAttribute("disabled", "true");
  btn.classList.remove("is-visible");
  btnEdit?.classList.remove("is-hidden");

  if (!newContent || isNaN(id)) return;

  const response = await noteService.edit(id, newContent);
  window.location.href = response.redirect_to;
};

const onClickDeleteNote = async (e: Event): Promise<void> => {
  const btn = e.currentTarget as HTMLButtonElement;
  const noteRoot = btn.parentElement?.parentElement
    ?.parentElement as HTMLDivElement;
  const id = parseInt(getIdByString(noteRoot.id, "-"), 10);

  if (isNaN(id)) return;

  const response = await noteService.delete(id);
  window.location.href = response.redirect_to;
};

const onClickLogout = async (): Promise<void> => {
  const data = await authService.logout();
  window.location.href = data.redirect_to ?? window.location.pathname;
};

const onSubmitLogin = async (e: Event): Promise<void> => {
  const form = e.currentTarget as HTMLFormElement;
  const username =
    form.querySelector<HTMLInputElement>("#username")?.value.trim() ?? "";
  const password =
    form.querySelector<HTMLInputElement>("#password")?.value.trim() ?? "";

  const data = await authService.login(username, password);
  window.location.href = data.redirect_to ?? window.location.pathname;
};

const onSubmitRegister = async (e: Event): Promise<void> => {
  const form = e.currentTarget as HTMLFormElement;
  const username =
    form.querySelector<HTMLInputElement>("#username")?.value.trim() ?? "";
  const password =
    form.querySelector<HTMLInputElement>("#password")?.value.trim() ?? "";
  const email =
    form.querySelector<HTMLInputElement>("#email")?.value.trim() ?? "";

  const data = await authService.register(username, password, email);
  window.location.href = data.redirect_to ?? window.location.pathname;
};

document.addEventListener("DOMContentLoaded", registerEvents);
