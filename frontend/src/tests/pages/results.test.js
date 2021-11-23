import React from 'react';
import Results from '../../pages/Results/Results';
import renderer from 'react-test-renderer';
import { BrowserRouter } from 'react-router-dom';

const mockData = {
  feature_analysis_results: [
    {
      image_1: "image_id",
      color_scheme_analysis: {
        count: 5,
        colors: [
          { red: 230, green: 226, blue: 216, proportion: 0.4253989209432653 },
          { red: 9, green: 24, blue: 38, proportion: 0.16556650478570417 },
          { red: 172, green: 165, blue: 158, proportion: 0.15257673629119714 },
          { red: 112, green: 96, blue: 78, proportion: 0.09586900439840229 },
          { red: 37, green: 33, blue: 23, proportion: 0.07738628479823256 },
        ],
      },
      object_detection: {
        person: { freq: 1, confidences: [0.9984568357467651] },
        laptop: {
          freq: 2,
          confidences: [0.9387264847755432, 0.6356411576271057],
        },
        cup: { freq: 1, confidences: [0.9060431718826294] },
        processes_bounding_boxes_image_as_base64_string: 'base 64 image string',
      },
      sentiment_analysis: {
        'sentiment_array[neg,neu,pos]': [
          0.5963839888572693, 0.13197453320026398, 0.2716415226459503,
        ],
        degrees: { Negative: '59.64%', Neutral: '13.20%', Postive: '27.16%' },
      },
      image_classification: {
        'cellular telephone': 0.6936329007148743,
        notebook: 0.19310395419597626,
        'hand-held computer': 0.04424683377146721,
        'web site': 0.021844087168574333,
        television: 0.014548316597938538,
      },
      text_recognition: '',
      face_analysis: {
        analysis: [
          {age: 22,
dominant_emotion: "happy",
dominant_race: "white",
emotion: {angry: 5.888953067055257e-8,
  disgust: 9.406594389845943e-11,
  fear: 5.528744358280318e-7,
  happy: 99.98632669611851,
  neutral: 0.013652960306425654,
  sad: 5.4525238929900076e-8,
  surprise: 0.00001572425628773115},
gender: "Man",
race: {asian: 0.0007496751550206682,
  black: 0.00015141853282329976,
  indian: 0.017956600640900433,
  'latino hispanic': 1.8069805577397346,
  'middle eastern': 11.54509037733078,
  white: 86.62906885147095},
region: {x: 17, y: 16, w: 169, h: 169}}
        ],
        count: 1
      }
    },
  ],
  collage_image_string: 'base 64 string',
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
        <Results results={mockData} images={files} />
      </BrowserRouter>
    )
    .toJSON();
  expect(tree).toMatchSnapshot();
});
