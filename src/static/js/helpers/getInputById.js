import { classInput } from "../constants/vars.js";
export const getInputById = (id) => {
    const inputs = document.querySelectorAll(classInput);
    return Array.from(inputs).find((input) => input.id === id);
};
