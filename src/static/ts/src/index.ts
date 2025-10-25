import { getIdByString } from "@src/helpers/getIdByString";

import { postCreateNote } from "@src/api/post/postCreateNote";
import { patchUpdateNote } from "@src/api/patch/patchUpdateNote";
import { deleteNote } from "@src/api/delete/deleteNote";

import {
  classAlert,
  classBtnAddNote,
  classBtnConfirmEditNote,
  classBtnDeleteNote,
  classBtnEditNote,
  classCloseAlert,
  classCloseNavbar,
  classNavbar,
  classOpenNavbar,
  classTextArea,
} from "@src/constants/vars";

const registerEvents = () => {
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

  if (closeAlertBtns.length !== 0) {
    closeAlertBtns.forEach((closeAlertBtn) =>
      closeAlertBtn.addEventListener("click", onClickCloseAlert)
    );
  }

  if (openNavbarBtn) {
    openNavbarBtn.addEventListener("click", onClickOpenNavbar);
  }

  if (closeNavbarBtn) {
    closeNavbarBtn.addEventListener("click", onClickCloseNavbar);
  }

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

  const alerts = document.querySelectorAll<HTMLLIElement>(classAlert);

  const alertClicked = Array.from(alerts).find(
    (alert) => getIdByString(alert.id, "-") === idAlertClicked
  );

  alertClicked!.remove();
};

const onClickOpenNavbar = (e: Event) => {
  const btn = e.currentTarget as HTMLButtonElement;

  const navbar = document.querySelector<HTMLElement>(classNavbar);
  const closeNavbarBtn =
    document.querySelector<HTMLButtonElement>(classCloseNavbar);

  btn.classList.remove("c-header__action--active");
  closeNavbarBtn!.classList.add("c-header__action--active");
  navbar!.classList.add("c-nav--open");
};

const onClickCloseNavbar = (e: Event) => {
  const btn = e.currentTarget as HTMLButtonElement;

  const navbar = document.querySelector<HTMLElement>(classNavbar);
  const openNavbarBtn =
    document.querySelector<HTMLButtonElement>(classOpenNavbar);

  btn.classList.remove("c-header__action--active");
  openNavbarBtn!.classList.add("c-header__action--active");
  navbar!.classList.remove("c-nav--open");
};

const onClickAddNote = async () => {
  const response = await postCreateNote();

  if (response.redirected) window.location.href = response.url;

  return;
};

const onClickEditNote = (e: Event) => {
  const btn = e.currentTarget as HTMLButtonElement;
  const noteRoot = btn.parentElement?.parentElement?.parentElement;

  const textArea = noteRoot?.querySelector<HTMLTextAreaElement>(classTextArea);
  const btnConfirmEdit = noteRoot?.querySelector<HTMLButtonElement>(
    classBtnConfirmEditNote
  );

  textArea?.removeAttribute("disabled");
  textArea?.focus();

  btn.classList.add("u-none");
  btnConfirmEdit!.classList.add("u-block");
};

const onClickConfirmEditNote = async (e: Event) => {
  const btn = e.currentTarget as HTMLButtonElement;
  const noteRoot = btn.parentElement?.parentElement
    ?.parentElement as HTMLDivElement;
  const idNote = getIdByString(noteRoot.id, "-");

  const textArea = noteRoot.querySelector<HTMLTextAreaElement>(classTextArea);
  const btnEdit = noteRoot.querySelector<HTMLButtonElement>(classBtnEditNote);

  textArea?.setAttribute("disabled", "true");
  btn.classList.remove("u-block");
  btnEdit!.classList.remove("u-none");

  const newContent = textArea!.value;

  const response = await patchUpdateNote(idNote, newContent);

  const redirectTo = response.redirect_to;

  window.location.href = redirectTo;
};

const onClickDeleteNote = async (e: Event) => {
  const btn = e.currentTarget as HTMLButtonElement;
  const noteRoot = btn.parentElement?.parentElement
    ?.parentElement as HTMLDivElement;
  const idNote = getIdByString(noteRoot.id, "-");

  const response = await deleteNote(idNote);

  const redirectTo = response.redirect_to;

  window.location.href = redirectTo;
};

const onInit = () => {
  registerEvents();
};

document.addEventListener("DOMContentLoaded", onInit);
