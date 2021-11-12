import React from 'react';
import renderer from 'react-test-renderer';
import AnalyzeImage from '../../pages/AnalyzeImage/AnalyzeImage';
import { BrowserRouter } from 'react-router-dom';

//  https://developer.mozilla.org/en-US/docs/Web/API/File/File
it('Renders Analyze Image page correctly', () => {
  Object.defineProperty(window.document, 'cookie', {
    writable: true,
    value: 'access_token=FAKE_TOKEN_VAL',
  });

  const files = [
    new File(['image-bits...'], 'chucknorris.png', {
      type: 'image/png',
    }),
  ];

  const tree = renderer
    .create(
      <BrowserRouter>
        <AnalyzeImage files={files} />
      </BrowserRouter>
    )
    .toJSON();
  expect(tree).toMatchSnapshot();
});
