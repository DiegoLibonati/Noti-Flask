export const getIdByString = (value: string, separator: string): string => {
  const parts = value.split(separator);
  return parts.at(-1) ?? "";
};
