import React from 'react';
import ResultsNav from '../../components/ResultsNav/ResultsNav';
import renderer from 'react-test-renderer';

jest.mock('react-router-dom', () => ({
  ...jest.requireActual('react-router-dom'),
  useLocation: () => ({
    pathname: '/results',
  }),
}));

it('Renders Results Nav', () => {
  const tree = renderer
    .create(
      <ResultsNav>
        <></>
      </ResultsNav>
    )
    .toJSON();
  expect(tree).toMatchSnapshot();
});
