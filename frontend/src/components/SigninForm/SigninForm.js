import React from 'react';
import { Link } from 'react-router-dom';

import styles from './SigninForm.module.css';

const SigninForm = ({
  authType,
  onSubmit,
  onEmailChange,
  email, 
  password,
  onPasswordChange,
  error,
}) => {
  const handleSubmit = (event) => {
    event.preventDefault();
    onSubmit();
  };

  return (
    <form onSubmit={handleSubmit} className={styles.signinForm}>
      <h1>{authType}</h1>
      {error ? <div className="error">{error}</div> : null}

      <label className={styles.labelName}>Email</label>
      <input
        id="signin__email__input"
        placeholder="email"
        className={styles.signinInputEmail}
        type="email"
        onChange={(e) => onEmailChange(e.target.value)}
      />

      <label className={styles.labelName}>Password</label>
      <input
        id="signin__password__input"
        placeholder="password"
        className={styles.signinInputPassword}
        type="password"
        onChange={(e) => onPasswordChange(e.target.value)}
      />

      <div className="buttonGradient">
        <button className={styles.submitButton} disabled={password?.length === 0 || email?.length === 0}>{authType}</button>
      </div>
      <Link
        to={`/${authType === 'Login' ? 'signup' : 'login'}`}
        className={styles.switchAuth}
      >
        {`${authType === 'Login' ? 'Signup' : 'Login'}`}
      </Link>
    </form>
  );
};

export default SigninForm;
