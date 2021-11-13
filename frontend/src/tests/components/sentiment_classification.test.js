import React from 'react';
import SentimentClassification from '../../components/SentimentClassification/SentimentClassification';
import renderer from 'react-test-renderer';

it('Renders ImageClassification component correctly', () => {
  const sentimentClassificationResults = {
    Negative: '68.18%',
    Neutral: '15.44%',
    Postive: '16.38%',
  };
  const tree = renderer
    .create(
      <SentimentClassification results={sentimentClassificationResults} />
    )
    .toJSON();
  expect(tree).toMatchSnapshot();
});
