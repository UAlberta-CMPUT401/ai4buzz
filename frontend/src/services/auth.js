import axios from 'axios';

/**
 * http post signup user
 */
export const signup = async (email, password) => {
  return await axios.post(
    'http://[2605:fd00:4:1001:f816:3eff:fe26:70dd]/users',
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
  return await axios.post(
    'http://[2605:fd00:4:1001:f816:3eff:fe26:70dd]/token',
    {
      email: email,
      password: password,
    }
  );
};
