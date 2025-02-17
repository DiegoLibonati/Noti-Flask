import {
  classAlert,
  classBtnAddNote,
  classBtnConfirmEditNote,
  classBtnDeleteNote,
  classBtnEditNote,
  classBtnLogin,
  classBtnLogout,
  classBtnRegister,
  classCloseAlert,
  classCloseNavbar,
  classInput,
  classNavbar,
  classOpenNavbar,
} from "../constants/constants.js";

export const getElements = () => {
  return {
    alerts: document.querySelectorAll(classAlert),
    closeAlertBtns: document.querySelectorAll(classCloseAlert),
    navbar: document.querySelector(classNavbar),
    openNavbarBtn: document.querySelector(classOpenNavbar),
    closeNavbarBtn: document.querySelector(classCloseNavbar),
    addNoteBtn: document.querySelector(classBtnAddNote),
    editNoteBtns: document.querySelectorAll(classBtnEditNote),
    editConfirmNoteBtns: document.querySelectorAll(classBtnConfirmEditNote),
    deleteNoteBtns: document.querySelectorAll(classBtnDeleteNote),
    loginBtn: document.querySelector(classBtnLogin),
    logoutBtn: document.querySelector(classBtnLogout),
    registerBtn: document.querySelector(classBtnRegister),
    inputs: document.querySelectorAll(classInput),
  };
};
