import React from 'react';

const SentimentClassification = ({ results }) => {
  return (
    <div>
      {Object.keys(results).map((sentimentClass, idx) => {
        return (
          <div key={idx}>
            <div>{sentimentClass}</div>
            <div className="value">{results[sentimentClass]}</div>
          </div>
        );
      })}
    </div>
  );
};

export default SentimentClassification;
