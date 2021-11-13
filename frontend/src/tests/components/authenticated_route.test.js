import React from 'react';
import renderer from 'react-test-renderer';
import { BrowserRouter, Switch, Route } from 'react-router-dom';

import Login from '../../pages/Login/Login';
import AuthenticatedRoute from '../../components/AuthenticatedRoute/AuthenticatedRoute';

it('Renders authenticated route page correctly if access token is available', () => {
  Object.defineProperty(window.document, 'cookie', {
    writable: true,
    value: 'access_token=FAKE_TOKEN_VAL',
  });

  const tree = renderer
    .create(
      <BrowserRouter>
        <AuthenticatedRoute>
          <></>
        </AuthenticatedRoute>
      </BrowserRouter>
    )
    .toJSON();
  expect(tree).toMatchSnapshot();
});

it('Redirects authenticated route page to login page if access token is not there', () => {
  Object.defineProperty(window.document, 'cookie', {
    writable: true,
    value: undefined,
  });

  const tree = renderer
    .create(
      <BrowserRouter>
        <Switch>
          <Route path="/login" exact component={Login} />
          <AuthenticatedRoute>
            <></>
          </AuthenticatedRoute>
        </Switch>
      </BrowserRouter>
    )
    .toJSON();
  expect(tree).toMatchSnapshot();
});
