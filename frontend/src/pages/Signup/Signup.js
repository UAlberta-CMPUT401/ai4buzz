import React, { useState } from 'react';
import Cookies from 'js-cookie';

import { signup } from '../../services/auth';
import SigninForm from '../../components/SigninForm/SigninForm';

const Signup = () => {
  const [email, setEmail] = useState();
  const [password, setPassword] = useState();

  const handleSubmit = async () => {
    const res = await signup(email, password);
    Cookies.set('access_token', res.data.access_token, { path: '/' });
  };

  return (
    <div>
      <SigninForm
        authType="Signup"
        onEmailChange={setEmail}
        onPasswordChange={setPassword}
        onSubmit={handleSubmit}
      />
    </div>
  );
};

export default Signup;
