import React from 'react';
import styles from './SentimentClassification.module.css';

const SentimentClassification = ({ results }) => {
  return (
    <div>
      {Object.keys(results).map((sentimentClass, idx) => {
        return (
          <div key={idx} className={styles.sentimentClassificationData}>
            <div>{sentimentClass}</div>
            <div className="value">{results[sentimentClass]}</div>
          </div>
        );
      })}
    </div>
  );
};

export default SentimentClassification;
