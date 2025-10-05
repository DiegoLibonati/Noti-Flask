import { getElements } from "@src/helpers/getElements";

export const getInputById = (id: string): Element | undefined => {
  const { inputs } = getElements();

  return Array.from(inputs).find((input) => input.id === id);
};