import React, { useState } from 'react';
import Cookies from 'js-cookie';
import { useHistory } from 'react-router-dom';

import { signup } from '../../services/auth';
import SigninForm from '../../components/SigninForm/SigninForm';
import styles from './Signup.module.css';

const Signup = () => {
  const [email, setEmail] = useState();
  const [password, setPassword] = useState();
  const [error, setError] = useState();
  const history = useHistory();

  const handleSubmit = async () => {
    try {
      const res = await signup(email, password);
      Cookies.set('access_token', res.data.access_token, { path: '/' });
      history.push('/analyze-image');
    } catch (e) {
      setError(e.response.data);
    }
  };

  return (
    <div className={styles.signupPage}>
      <h1 className={styles.title}>AI4Buzz</h1>
      <SigninForm
        authType="Signup"
        onEmailChange={setEmail}
        onPasswordChange={setPassword}
        onSubmit={handleSubmit}
        error={error}
      />
    </div>
  );
};

export default Signup;
