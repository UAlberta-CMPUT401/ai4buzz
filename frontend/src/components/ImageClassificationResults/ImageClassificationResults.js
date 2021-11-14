import React from 'react';
import styles from './ImageClassificationResults.module.css';

const ImageClassificationResults = ({ results }) => {
  return (
    <div>
      {Object.keys(results).map((object, idx) => {
        return (
          <div key={idx} className={styles.imageClassificationResultsData}>
            <div>{object}</div>
            <div className="value">{(results[object] * 100).toFixed(3)}%</div>
          </div>
        );
      })}
    </div>
  );
};

export default ImageClassificationResults;
