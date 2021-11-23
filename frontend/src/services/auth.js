import axios from 'axios';
import getUrl from '../utils/getUrl';

/**
 * http post signup user
 */
export const signup = async (email, password) => {
  const baseUrl = getUrl()
  return await axios.post(
    `${baseUrl}/users`,
    {
      email: email,
      password: password,
    }
  );
};

/**
 * http post login user
 */
export const login = async (email, password) => {
  const baseUrl = getUrl()
  return await axios.post(
    `${baseUrl}/token`,
    {
      email: email,
      password: password,
    }
  );
};
