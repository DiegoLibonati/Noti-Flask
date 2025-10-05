import {
  classAlert,
  classBtnAddNote,
  classBtnConfirmEditNote,
  classBtnDeleteNote,
  classBtnEditNote,
  classCloseAlert,
  classCloseNavbar,
  classInput,
  classNavbar,
  classOpenNavbar,
} from "@src/constants/constants";

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
    inputs: document.querySelectorAll(classInput),
  };
};
