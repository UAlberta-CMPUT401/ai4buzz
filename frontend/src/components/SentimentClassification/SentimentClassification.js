import React from 'react';

const SentimentClassification = ({ results }) => {
  console.log(results);
  return (
    <div>
      {Object.keys(results).map((sentimentClass, idx) => {
        return (
          <div>
            <div>{sentimentClass}</div>
            <div className="value">{results[sentimentClass]}</div>
          </div>
        );
      })}
    </div>
  );
};

export default SentimentClassification;
