import { apiPrefixAuth } from "../../../constants/constants.js";

export const postLogin = (username, password) => {
  const data = {
    username: username,
    password: password,
  };

  return fetch(`${apiPrefixAuth}/login`, {
    method: "post",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });
};
