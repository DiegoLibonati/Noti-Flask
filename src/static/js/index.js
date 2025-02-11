import { getElements } from "./helpers/getElements.js";
import { getIdAlert } from "./helpers/getIdAlert.js";

const onClickCloseAlert = (e) => {
  const btn = e.currentTarget;
  const idBtn = btn.id;
  const idAlertClicked = getIdAlert(idBtn);

  const { alerts } = getElements();

  const alertClicked = Array.from(alerts).find(
    (alert) => getIdAlert(alert.id) === idAlertClicked
  );

  alertClicked.remove();
};

const onInit = () => {
  const { closeAlertBtns } = getElements();

  closeAlertBtns.forEach((closeAlertBtn) =>
    closeAlertBtn.addEventListener("click", onClickCloseAlert)
  );
};

document.addEventListener("DOMContentLoaded", onInit);
