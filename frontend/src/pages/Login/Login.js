import React, { useState } from 'react';
import Cookies from 'js-cookie';

import { login } from '../../services/auth';
import SigninForm from '../../components/SigninForm/SigninForm';

const Login = () => {
  const [email, setEmail] = useState();
  const [password, setPassword] = useState();

  const handleSubmit = async () => {
    const res = await login(email, password);
    console.log(res);
    Cookies.set('access_token', res.data.access_token, { path: '/' });
  };

  return (
    <div>
      <SigninForm
        authType="Login"
        onSubmit={handleSubmit}
        onEmailChange={setEmail}
        onPasswordChange={setPassword}
      />
    </div>
  );
};

export default Login;
