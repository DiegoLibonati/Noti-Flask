export const getElements = () => {
  return {
    alerts: document.querySelectorAll(".js-alert"),
    closeAlertBtns: document.querySelectorAll(".js-close-alert"),
  };
};
