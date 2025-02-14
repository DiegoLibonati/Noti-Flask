export const getElements = () => {
  return {
    alerts: document.querySelectorAll(".js-alert"),
    closeAlertBtns: document.querySelectorAll(".js-close-alert"),
    navbar: document.querySelector(".js-navbar"),
    openNavbarBtn: document.querySelector(".js-open-navbar"),
    closeNavbarBtn: document.querySelector(".js-close-navbar"),
    addNoteBtn: document.querySelector(".js-btn-add-note"),
    editNoteBtns: document.querySelectorAll(".js-btn-edit-note"),
    deleteNoteBtns: document.querySelectorAll(".js-btn-delete-note"),
    loginBtn: document.querySelector(".js-btn-login"),
    logoutBtn: document.querySelector(".js-btn-logout"),
    registerBtn: document.querySelector(".js-btn-register"),
    inputs: document.querySelectorAll(".js-input")
  };
};
