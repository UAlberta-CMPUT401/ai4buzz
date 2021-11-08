import React from "react";

const SigninForm = ({
  authType,
  onSubmit,
  onEmailChange,
  onPasswordChange,
}) => {
  const handleSubmit = (event) => {
    event.preventDefault();
    onSubmit();
  };

  return (
    <form onSubmit={handleSubmit}>
      <input
        placeholder="email"
        onChange={(e) => onEmailChange(e.target.value)}
      />
      <input
        placeholder="password"
        onChange={(e) => onPasswordChange(e.target.value)}
      />
      <button>{authType}</button>
    </form>
  );
};

export default SigninForm;
