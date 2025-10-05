export const getIdByString = (string: string, separator: string): string => {
  const idArr = string.slice(separator as unknown as number);
  const id = idArr[idArr.length - 1];

  return id;
};
