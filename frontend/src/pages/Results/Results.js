import React from 'react';
import styles from './Results.module.css';

const Results = ({ data, images }) => {
  console.log(data, images);

  return (
    <div className={styles.resultsPage}>
      <h1 className={styles.resultTitle}>Image Results</h1>
      {images.map((image, idx) => {
        return (
          <div key={idx}>
            <div>{image.name}</div>
            <img
              className={styles.image}
              src={URL.createObjectURL(image)}
              alt="results"
            />
            <div>{JSON.stringify(data)}</div>
          </div>
        );
      })}
      <div>
        <div className={styles.results}></div>
      </div>
    </div>
  );
};

export default Results;
