import React from 'react';
import ImageClassificationResults from '../../components/ImageClassificationResults/ImageClassificationResults';
import renderer from 'react-test-renderer';

it('Renders ImageClassification component correctly', () => {
  const imageClassificationResults = {
    'web site': 0.9249883890151978,
    'book jacket': 0.01968519203364849,
    'comic book': 0.012182716280221939,
    envelope: 0.0011725202202796936,
    'analog clock': 0.0009474915568716824,
  };
  const tree = renderer
    .create(<ImageClassificationResults results={imageClassificationResults} />)
    .toJSON();
  expect(tree).toMatchSnapshot();
});
