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
      "face_analysis": {
        "count": 2,
        "analysis": {
            "emotion": {
                "angry": 0.2391964688116548,
                "disgust": 0.002045524644826395,
                "fear": 30.837110668357294,
                "happy": 68.77959444718789,
                "sad": 0.008633821044438134,
                "surprise": 0.12629777239686976,
                "neutral": 0.007117449318450958
            },
            "dominant_emotion": "happy",
            "likely age": 32.333333333333336,
            "estimated gender": "male",
            "race": {
                "asian": 18.11004209356997,
                "indian": 3.1135811034670065,
                "black": 0.726972792443863,
                "white": 34.73537395454501,
                "middle eastern": 21.67139240098549,
                "latino hispanic": 21.642636452030526
            },
            "estimated_race": "white"
        }
    },
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
