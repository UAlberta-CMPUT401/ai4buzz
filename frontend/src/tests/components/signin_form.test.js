import React from 'react';
import renderer from 'react-test-renderer';
import { BrowserRouter } from 'react-router-dom';
import SigninForm from '../../components/SigninForm/SigninForm';

it("Renders SigninForm for auth type 'SignUp' correctly", () => {
  const tree = renderer
    .create(
      <BrowserRouter>
        <SigninForm
          authType="SignUp"
          onSubmit={() => {}}
          onEmailChange={() => {}}
          onPasswordChange={() => {}}
          error=""
        />
      </BrowserRouter>
    )
    .toJSON();
  expect(tree).toMatchSnapshot();
});

it("Renders SigninForm for auth type 'Login' correctly", () => {
  const tree = renderer
    .create(
      <BrowserRouter>
        <SigninForm
          authType="Login"
          onSubmit={() => {}}
          onEmailChange={() => {}}
          onPasswordChange={() => {}}
          error=""
        />
      </BrowserRouter>
    )
    .toJSON();
  expect(tree).toMatchSnapshot();
});
