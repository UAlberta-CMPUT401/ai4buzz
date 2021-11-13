import React from 'react';
import Results from '../../pages/Results/Results';
import renderer from 'react-test-renderer';
import { BrowserRouter } from 'react-router-dom';

const mockData = {
  image_1: {
    color_scheme_analysis: {
      count: 2,
      colors: [
        {
          red: 5,
          green: 41,
          blue: 64,
          proportion: 0.5235686765073805,
        },
        {
          red: 253,
          green: 252,
          blue: 252,
          proportion: 0.17823367525644232,
        },
      ],
    },
    object_detection: {
      person: {
        freq: 2,
        confidences: [0.9994099140167236, 0.9985186457633972],
      },
    },
    sentiment_analysis: {
      'sentiment_array[neg,neu,pos]': [
        0.6817643046379089, 0.1544295847415924, 0.16380618512630463,
      ],
      degrees: {
        Negative: '68.18%',
        Neutral: '15.44%',
        Postive: '16.38%',
      },
    },
    image_classification: {
      'web site': 0.9249883890151978,
      'book jacket': 0.01968519203364849,
      'comic book': 0.012182716280221939,
      envelope: 0.0011725202202796936,
      'analog clock': 0.0009474915568716824,
    },
    text_recognition:
      "“Oh you're a software engineer? So you\nhave a rainbow computer with 2\nmonitors?\n\f",
  },
};

const files = [
  new File(['image-bits...'], 'chucknorris.png', {
    type: 'image/png',
  }),
];

global.URL.createObjectURL = jest.fn();

it('Renders Results page correctly', () => {
  const tree = renderer
    .create(
      <BrowserRouter>
        <Results featureAnalysisResults={mockData} images={files} />
      </BrowserRouter>
    )
    .toJSON();
  expect(tree).toMatchSnapshot();
});
