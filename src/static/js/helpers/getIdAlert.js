export const getIdAlert = (idAlert) => {
  const idArr = idAlert.slice("-");
  const id = idArr[idArr.length - 1];

  return id;
};
