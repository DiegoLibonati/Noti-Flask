import { classBtnConfirmEditNote, classBtnEditNote, classTextArea, } from "./constants/constants.js";
import { getElements } from "./helpers/getElements.js";
import { getIdByString } from "./helpers/getIdByString.js";
import { deleteNote } from "./services/notes/delete/deleteNote.js";
import { patchUpdateNote } from "./services/notes/patch/patchUpdateNote.js";
import { postCreateNote } from "./services/notes/post/postCreateNote.js";
const registerEvents = () => {
    const { closeAlertBtns, openNavbarBtn, closeNavbarBtn, addNoteBtn, deleteNoteBtns, editNoteBtns, editConfirmNoteBtns, } = getElements();
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
    const { alerts } = getElements();
    const alertClicked = Array.from(alerts).find((alert) => getIdByString(alert.id, "-") === idAlertClicked);
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
    if (response.redirected) {
        window.location.href = response.url;
    }
    return response;
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
    const data = response.json();
    const redirectTo = data.redirect_to;
    window.location.href = redirectTo;
};
const onClickDeleteNote = async (e) => {
    const btn = e.currentTarget;
    const noteRoot = btn.parentElement?.parentElement
        ?.parentElement;
    const idNote = getIdByString(noteRoot.id, "-");
    const response = await deleteNote(idNote);
    const data = response.json();
    const redirectTo = data.redirect_to;
    window.location.href = redirectTo;
};
const onInit = () => {
    registerEvents();
};
document.addEventListener("DOMContentLoaded", onInit);
