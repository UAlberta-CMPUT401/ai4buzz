import React from 'react';

import styles from './ObjectDetectionResults.module.css';

const ObjectDetectionResults = ({ results }) => {
  return (
    <>
      {Object.keys(results).map((object, idx) => {
        // ignore the bounding box image string
        if (object === 'processes_bounding_boxes_image_as_base64_string')
          return null;
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
