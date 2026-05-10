import { classInput } from "@/constants/vars";

export const getInputById = (id: string): HTMLInputElement | undefined => {
  const inputs = document.querySelectorAll<HTMLInputElement>(classInput);

  return Array.from(inputs).find((input) => input.id === id);
};
