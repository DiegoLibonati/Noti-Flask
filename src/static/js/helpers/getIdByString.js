export const getIdByString = (string, separator) => {
    const idArr = string.slice(separator);
    const id = idArr[idArr.length - 1];
    return id;
};
