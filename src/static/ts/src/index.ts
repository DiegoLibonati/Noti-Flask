import {
  classBtnConfirmEditNote,
  classBtnEditNote,
  classTextArea,
} from "@src/constants/constants";

import { getElements } from "@src/helpers/getElements";
import { getIdByString } from "@src/helpers/getIdByString";

import { deleteNote } from "@src/services/notes/delete/deleteNote";
import { patchUpdateNote } from "@src/services/notes/patch/patchUpdateNote";
import { postCreateNote } from "@src/services/notes/post/postCreateNote";

const registerEvents = () => {
  const {
    closeAlertBtns,
    openNavbarBtn,
    closeNavbarBtn,
    addNoteBtn,
    deleteNoteBtns,
    editNoteBtns,
    editConfirmNoteBtns,
  } = getElements();

  // Close Alert Btns Events
  if (closeAlertBtns.length !== 0) {
    closeAlertBtns.forEach((closeAlertBtn) =>
      closeAlertBtn.addEventListener("click", onClickCloseAlert)
    );
  }

  // Manage Navbar Btns Events
  if (openNavbarBtn) {
    openNavbarBtn.addEventListener("click", onClickOpenNavbar);
  }

  if (closeNavbarBtn) {
    closeNavbarBtn.addEventListener("click", onClickCloseNavbar);
  }

  // Btns Note Events
  if (addNoteBtn) {
    addNoteBtn.addEventListener("click", onClickAddNote);
  }

  if (editNoteBtns.length !== 0) {
    editNoteBtns.forEach((editNoteBtn) =>
      editNoteBtn.addEventListener("click", onClickEditNote)
    );
  }

  if (deleteNoteBtns.length !== 0) {
    deleteNoteBtns.forEach((deleteNoteBtn) =>
      deleteNoteBtn.addEventListener("click", onClickDeleteNote)
    );
  }

  if (editConfirmNoteBtns.length !== 0) {
    editConfirmNoteBtns.forEach((editConfirmNoteBtn) =>
      editConfirmNoteBtn.addEventListener("click", onClickConfirmEditNote)
    );
  }
};

const onClickCloseAlert = (e: Event) => {
  const btn = e.currentTarget as HTMLButtonElement;
  const idBtn = btn.id;
  const idAlertClicked = getIdByString(idBtn, "-");

  const { alerts } = getElements();

  const alertClicked = Array.from(alerts).find(
    (alert) => getIdByString(alert.id, "-") === idAlertClicked
  );

  alertClicked!.remove();
};

const onClickOpenNavbar = (e: Event) => {
  const btn = e.currentTarget as HTMLButtonElement;

  const { navbar, closeNavbarBtn } = getElements();

  btn.classList.remove("c-header__action--active");
  closeNavbarBtn!.classList.add("c-header__action--active");
  navbar!.classList.add("c-nav--open");
};

const onClickCloseNavbar = (e: Event) => {
  const btn = e.currentTarget as HTMLButtonElement;

  const { navbar, openNavbarBtn } = getElements();

  btn.classList.remove("c-header__action--active");
  openNavbarBtn!.classList.add("c-header__action--active");
  navbar!.classList.remove("c-nav--open");
};

const onClickAddNote = async () => {
  const response = await postCreateNote();

  if (response.redirected) {
    window.location.href = response.url;
  }

  return response;
};

const onClickEditNote = (e: Event) => {
  const btn = e.currentTarget as HTMLButtonElement;
  const noteRoot = btn.parentElement?.parentElement?.parentElement;

  const textArea = noteRoot?.querySelector(
    classTextArea
  ) as HTMLTextAreaElement;
  const btnConfirmEdit = noteRoot?.querySelector(
    classBtnConfirmEditNote
  ) as HTMLButtonElement;

  textArea?.removeAttribute("disabled");
  textArea?.focus();

  btn.classList.add("u-none");
  btnConfirmEdit.classList.add("u-block");
};

const onClickConfirmEditNote = async (e: Event) => {
  const btn = e.currentTarget as HTMLButtonElement;
  const noteRoot = btn.parentElement?.parentElement
    ?.parentElement as HTMLDivElement;
  const idNote = getIdByString(noteRoot.id, "-");

  const textArea = noteRoot.querySelector(classTextArea) as HTMLTextAreaElement;
  const btnEdit = noteRoot.querySelector(classBtnEditNote) as HTMLButtonElement;

  textArea?.setAttribute("disabled", "true");
  btn.classList.remove("u-block");
  btnEdit.classList.remove("u-none");

  const newContent = textArea.value;

  const response = await patchUpdateNote(idNote, newContent);
  const data = response.json() as unknown as Record<string, unknown>;

  const redirectTo = data.redirect_to as string;

  window.location.href = redirectTo;
};

const onClickDeleteNote = async (e: Event) => {
  const btn = e.currentTarget as HTMLButtonElement;
  const noteRoot = btn.parentElement?.parentElement
    ?.parentElement as HTMLDivElement;
  const idNote = getIdByString(noteRoot.id, "-");

  const response = await deleteNote(idNote);
  const data = response.json() as unknown as Record<string, unknown>;

  const redirectTo = data.redirect_to as string;

  window.location.href = redirectTo;
};

const onInit = () => {
  registerEvents();
};

document.addEventListener("DOMContentLoaded", onInit);
