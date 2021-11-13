import React, { useState } from 'react';
import Cookies from 'js-cookie';
import { useHistory } from 'react-router-dom';

import { login } from '../../services/auth';
import SigninForm from '../../components/SigninForm/SigninForm';
import styles from './Login.module.css';

const Login = () => {
  const [email, setEmail] = useState();
  const [password, setPassword] = useState();
  const [error, setError] = useState();
  const history = useHistory();

  const handleSubmit = async () => {
    try {
      const res = await login(email, password);
      Cookies.set('access_token', res.data.access_token, { path: '/' });
      history.push('/analyze-image');
    } catch (e) {
      setError(e.response.data);
    }
  };

  return (
    <div className={styles.loginPage}>
      <h1 className={styles.title}>AI4Buzz</h1>
      <SigninForm
        authType="Login"
        onSubmit={handleSubmit}
        onEmailChange={setEmail}
        onPasswordChange={setPassword}
        error={error}
      />
    </div>
  );
};

export default Login;
