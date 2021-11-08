import axios from "axios";

/**
 * http post signup user
 */
export const signup = async (email, password) => {
  return await axios.post("http://127.0.0.1:8000/signup", {
    email: email,
    password: password,
  });
};

/**
 * http post login user
 */
export const login = async (email, password) => {
  return await axios.post("http://127.0.0.1:8000/token", {
    email: email,
    password: password,
  });
};
