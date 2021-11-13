import React from 'react';
import LoadingOverlay from '../../components/LoadingOverlay/LoadingOverlay';
import renderer from 'react-test-renderer';

it('Renders loading overlay correctly', () => {
  const tree = renderer.create(<LoadingOverlay />).toJSON();
  expect(tree).toMatchSnapshot();
});
