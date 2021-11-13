import React from 'react';
import renderer from 'react-test-renderer';
import Login from '../../pages/Login/Login';
import { BrowserRouter } from 'react-router-dom';

describe('Test Login Page', () => {
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
});
