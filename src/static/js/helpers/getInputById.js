import { getElements } from "./getElements.js";

export const getInputById = (id) => {
  const { inputs } = getElements();

  return Array.from(inputs).find((input) => input.id === id);
};
