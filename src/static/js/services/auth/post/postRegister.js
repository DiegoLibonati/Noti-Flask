import { apiPrefixAuth } from "../../../constants/constants.js";

export const postRegister = (username, password, email) => {
  const data = {
    username: username,
    password: password,
    email: email
  };

  return fetch(`${apiPrefixAuth}/sign_up`, {
    method: "post",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });
};
