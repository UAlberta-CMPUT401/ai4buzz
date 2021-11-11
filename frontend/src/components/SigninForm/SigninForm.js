import React from 'react';
import { Link } from 'react-router-dom';

import styles from './SigninForm.module.css';

const SigninForm = ({
  authType,
  onSubmit,
  onEmailChange,
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
      <div>
        <label className={styles.labelName}>Email</label>
        <input
          placeholder="email"
          className={styles.signinInput}
          type="email"
          onChange={(e) => onEmailChange(e.target.value)}
        />
      </div>
      <div>
        <label className={styles.labelName}>Password</label>
        <input
          placeholder="password"
          className={styles.signinInput}
          type="password"
          onChange={(e) => onPasswordChange(e.target.value)}
        />
      </div>
      <div className="buttonGradient">
        <button className={styles.submitButton}>{authType}</button>
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
