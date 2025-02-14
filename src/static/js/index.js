import { getElements } from "./helpers/getElements.js";
import { getIdByString } from "./helpers/getIdByString.js";
import { getInputById } from "./helpers/getInputById.js";
import { getLogout } from "./services/auth/get/getLogout.js";
import { postLogin } from "./services/auth/post/postLogin.js";
import { postRegister } from "./services/auth/post/postRegister.js";
import { deleteNote } from "./services/notes/delete/deleteNote.js";
import { postCreateNote } from "./services/notes/post/postCreateNote.js";

const registerEvents = () => {
  const {
    closeAlertBtns,
    openNavbarBtn,
    closeNavbarBtn,
    addNoteBtn,
    editNoteBtns,
    deleteNoteBtns,
    loginBtn,
    logoutBtn,
    registerBtn,
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

  // Btns Auth Events
  if (loginBtn) {
    loginBtn.addEventListener("click", onClickLogin);
  }

  if (logoutBtn) {
    logoutBtn.addEventListener("click", onClickLogout);
  }

  if (registerBtn) {
    registerBtn.addEventListener("click", onClickRegister);
  }
};

const onClickCloseAlert = (e) => {
  const btn = e.currentTarget;
  const idBtn = btn.id;
  const idAlertClicked = getIdByString(idBtn, "-");

  const { alerts } = getElements();

  const alertClicked = Array.from(alerts).find(
    (alert) => getIdByString(alert.id, "-") === idAlertClicked
  );

  alertClicked.remove();
};

const onClickOpenNavbar = (e) => {
  const btn = e.currentTarget;

  const { navbar, closeNavbarBtn } = getElements();

  btn.classList.remove("c-header__action--active");
  closeNavbarBtn.classList.add("c-header__action--active");
  navbar.classList.add("c-nav--open");
};

const onClickCloseNavbar = (e) => {
  const btn = e.currentTarget;

  const { navbar, openNavbarBtn } = getElements();

  btn.classList.remove("c-header__action--active");
  openNavbarBtn.classList.add("c-header__action--active");
  navbar.classList.remove("c-nav--open");
};

const onClickAddNote = async () => {
  const response = await postCreateNote();
  const data = await response.json();
  const statusCode = response.status;

  if (statusCode !== 201) return;

  const redirectTo = data.redirect_to;

  window.location.href = redirectTo;
};

const onClickEditNote = () => {};

const onClickDeleteNote = async (e) => {
  const btn = e.currentTarget;
  const noteRoot = btn.parentElement.parentElement.parentElement;
  const idNote = getIdByString(noteRoot.id, "-");

  const response = await deleteNote(idNote);
  const data = await response.json();

  const redirectTo = data.redirect_to;

  window.location.href = redirectTo;
};

const onClickLogout = async () => {
  const response = await getLogout();
  const data = await response.json();

  const redirectTo = data.redirect_to;

  window.location.href = redirectTo;
};

const onClickLogin = async (e) => {
  e.preventDefault();

  const inputUsername = getInputById("username");
  const inputPassword = getInputById("password");

  const response = await postLogin(inputUsername.value, inputPassword.value);
  const data = await response.json();

  const redirectTo = data.redirect_to;

  window.location.href = redirectTo;
};

const onClickRegister = async (e) => {
  e.preventDefault();

  const inputUsername = getInputById("username");
  const inputPassword = getInputById("password");
  const inputEmail = getInputById("email");

  const response = await postRegister(
    inputUsername.value,
    inputPassword.value,
    inputEmail.value
  );
  const data = await response.json();

  const redirectTo = data.redirect_to;

  window.location.href = redirectTo;
};

const onInit = () => {
  registerEvents();
};

document.addEventListener("DOMContentLoaded", onInit);
