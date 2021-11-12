import React from 'react';

import styles from './ObjectDetectionResults.module.css';

const ObjectDetectionResults = ({ results }) => {
  console.log(results);
  return (
    <>
      {Object.keys(results).map((object, idx) => {
        return (
          <div>
            <div>{object}</div>
            {results[object].confidences.map((confidence, idx) => {
              return <div className="value">{confidence.toFixed(7)}</div>;
            })}
          </div>
        );
      })}
    </>
  );
};

export default ObjectDetectionResults;
