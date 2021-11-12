import React from 'react';
import ReactDOM from 'react-dom';
import renderer from 'react-test-renderer';
import Login from '../../pages/Login/Login';
import App from '../../App';
import { BrowserRouter } from 'react-router-dom';

it('Renders login page correctly', () => {
  const tree = renderer
    .create(
      <BrowserRouter>
        <Login />
      </BrowserRouter>
    )
    .toJSON();
  expect(tree).toMatchSnapshot();
});
