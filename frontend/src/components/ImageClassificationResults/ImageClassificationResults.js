import React from 'react';

const ImageClassificationResults = ({ results }) => {
  return (
    <div>
      {Object.keys(results).map((object, idx) => {
        return (
          <div key={idx}>
            <div>{object}</div>
            <div className="value">{results[object].toFixed(7)}</div>
          </div>
        );
      })}
    </div>
  );
};

export default ImageClassificationResults;
