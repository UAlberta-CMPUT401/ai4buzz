import React from 'react';
import ObjectDetectionResults from '../../components/ObjectDetectionResults/ObjectDetectionResults';
import renderer from 'react-test-renderer';

it('Renders ImageClassification component correctly', () => {
  const objectDetectionResults = {
    person: {
      freq: 2,
      confidences: [0.9994099140167236, 0.9985186457633972],
    },
  };
  const tree = renderer
    .create(<ObjectDetectionResults results={objectDetectionResults} />)
    .toJSON();
  expect(tree).toMatchSnapshot();
});
