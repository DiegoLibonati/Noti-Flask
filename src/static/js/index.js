import { getIdByString } from "./helpers/getIdByString.js";
import { postCreateNote } from "./api/post/postCreateNote.js";
import { patchUpdateNote } from "./api/patch/patchUpdateNote.js";
import { deleteNote } from "./api/delete/deleteNote.js";
import { classAlert, classBtnAddNote, classBtnConfirmEditNote, classBtnDeleteNote, classBtnEditNote, classCloseAlert, classCloseNavbar, classNavbar, classOpenNavbar, classTextArea, } from "./constants/vars.js";
const registerEvents = () => {
    const closeNavbarBtn = document.querySelector(classCloseNavbar);
    const closeAlertBtns = document.querySelectorAll(classCloseAlert);
    const openNavbarBtn = document.querySelector(classOpenNavbar);
    const addNoteBtn = document.querySelector(classBtnAddNote);
    const editNoteBtns = document.querySelectorAll(classBtnEditNote);
    const deleteNoteBtns = document.querySelectorAll(classBtnDeleteNote);
    const editConfirmNoteBtns = document.querySelectorAll(classBtnConfirmEditNote);
    if (closeAlertBtns.length !== 0) {
        closeAlertBtns.forEach((closeAlertBtn) => closeAlertBtn.addEventListener("click", onClickCloseAlert));
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
        editNoteBtns.forEach((editNoteBtn) => editNoteBtn.addEventListener("click", onClickEditNote));
    }
    if (deleteNoteBtns.length !== 0) {
        deleteNoteBtns.forEach((deleteNoteBtn) => deleteNoteBtn.addEventListener("click", onClickDeleteNote));
    }
    if (editConfirmNoteBtns.length !== 0) {
        editConfirmNoteBtns.forEach((editConfirmNoteBtn) => editConfirmNoteBtn.addEventListener("click", onClickConfirmEditNote));
    }
};
const onClickCloseAlert = (e) => {
    const btn = e.currentTarget;
    const idBtn = btn.id;
    const idAlertClicked = getIdByString(idBtn, "-");
    const alerts = document.querySelectorAll(classAlert);
    const alertClicked = Array.from(alerts).find((alert) => getIdByString(alert.id, "-") === idAlertClicked);
    alertClicked.remove();
};
const onClickOpenNavbar = (e) => {
    const btn = e.currentTarget;
    const navbar = document.querySelector(classNavbar);
    const closeNavbarBtn = document.querySelector(classCloseNavbar);
    btn.classList.remove("c-header__action--active");
    closeNavbarBtn.classList.add("c-header__action--active");
    navbar.classList.add("c-nav--open");
};
const onClickCloseNavbar = (e) => {
    const btn = e.currentTarget;
    const navbar = document.querySelector(classNavbar);
    const openNavbarBtn = document.querySelector(classOpenNavbar);
    btn.classList.remove("c-header__action--active");
    openNavbarBtn.classList.add("c-header__action--active");
    navbar.classList.remove("c-nav--open");
};
const onClickAddNote = async () => {
    const response = await postCreateNote();
    if (response.redirected)
        window.location.href = response.url;
    return;
};
const onClickEditNote = (e) => {
    const btn = e.currentTarget;
    const noteRoot = btn.parentElement?.parentElement?.parentElement;
    const textArea = noteRoot?.querySelector(classTextArea);
    const btnConfirmEdit = noteRoot?.querySelector(classBtnConfirmEditNote);
    textArea?.removeAttribute("disabled");
    textArea?.focus();
    btn.classList.add("u-none");
    btnConfirmEdit.classList.add("u-block");
};
const onClickConfirmEditNote = async (e) => {
    const btn = e.currentTarget;
    const noteRoot = btn.parentElement?.parentElement
        ?.parentElement;
    const idNote = getIdByString(noteRoot.id, "-");
    const textArea = noteRoot.querySelector(classTextArea);
    const btnEdit = noteRoot.querySelector(classBtnEditNote);
    textArea?.setAttribute("disabled", "true");
    btn.classList.remove("u-block");
    btnEdit.classList.remove("u-none");
    const newContent = textArea.value;
    const response = await patchUpdateNote(idNote, newContent);
    const redirectTo = response.redirect_to;
    window.location.href = redirectTo;
};
const onClickDeleteNote = async (e) => {
    const btn = e.currentTarget;
    const noteRoot = btn.parentElement?.parentElement
        ?.parentElement;
    const idNote = getIdByString(noteRoot.id, "-");
    const response = await deleteNote(idNote);
    const redirectTo = response.redirect_to;
    window.location.href = redirectTo;
};
const onInit = () => {
    registerEvents();
};
document.addEventListener("DOMContentLoaded", onInit);
