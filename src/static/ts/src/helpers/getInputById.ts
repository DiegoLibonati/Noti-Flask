import { classInput } from "@src/constants/vars";

export const getInputById = (id: string): Element | undefined => {
  const inputs = document.querySelectorAll<HTMLInputElement>(classInput);

  return Array.from(inputs).find((input) => input.id === id);
};
