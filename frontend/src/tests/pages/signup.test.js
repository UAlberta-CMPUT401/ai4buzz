import React from 'react';
import renderer from 'react-test-renderer';
import Signup from '../../pages/Signup/Signup';
import { BrowserRouter } from 'react-router-dom';

it('Renders signup page correctly', () => {
  const tree = renderer
    .create(
      <BrowserRouter>
        <Signup />
      </BrowserRouter>
    )
    .toJSON();
  expect(tree).toMatchSnapshot();
});
