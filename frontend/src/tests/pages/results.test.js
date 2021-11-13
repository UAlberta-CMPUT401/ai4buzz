import React from 'react';
import Results from '../../pages/Results/Results';
import renderer from 'react-test-renderer';
import { BrowserRouter } from 'react-router-dom';

const mockData = {
  sentiment_analysis: {
    image_1: {
      'sentiment_array[neg,neu,pos]': [
        0.6817643046379089, 0.1544295847415924, 0.16380618512630463,
      ],
      degrees: {
        Negative: '68.18%',
        Neutral: '15.44%',
        Postive: '16.38%',
      },
    },
  },
  color_scheme_analysis: {
    count: 3,
    colors: [
      [5, 41, 64],
      [253, 252, 252],
      [36, 14, 27],
    ],
  },
  object_detection: {
    person: {
      freq: 2,
      confidences: [0.9994099140167236, 0.9985186457633972],
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
};

const files = [
  new File(['image-bits...'], 'chucknorris.png', {
    type: 'image/png',
  }),
];

global.URL.createObjectURL = jest.fn();

// https://developer.mozilla.org/en-US/docs/Web/API/File/File
it('Renders Results page correctly', () => {
  const tree = renderer
    .create(
      <BrowserRouter>
        <Results data={mockData} images={files} />
      </BrowserRouter>
    )
    .toJSON();
  expect(tree).toMatchSnapshot();
});
