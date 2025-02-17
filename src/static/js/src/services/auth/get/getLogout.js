import { apiPrefixAuth } from "../../../constants/constants.js";

export const getLogout = () => {
  return fetch(`${apiPrefixAuth}/logout`, { method: "get" });
};
