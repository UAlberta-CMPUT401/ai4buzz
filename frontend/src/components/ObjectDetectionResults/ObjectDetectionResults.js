import React from 'react';

import styles from './ObjectDetectionResults.module.css';

const ObjectDetectionResults = ({ results }) => {
  return (
    <>
      {Object.keys(results).map((object, idx) => {
        return (
          <div key={idx} className={styles.objectDetectionResultsData}>
            <div>{object}</div>
            <div>
              {results[object].confidences.map((confidence, idx) => {
                return (
                  <div className="value" key={idx}>
                    {(confidence * 100).toFixed(3)}%
                  </div>
                );
              })}
            </div>
          </div>
        );
      })}
    </>
  );
};

export default ObjectDetectionResults;
