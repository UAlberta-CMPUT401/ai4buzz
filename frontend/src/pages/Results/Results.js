import React from 'react';
import ImageClassificationResults from '../../components/ImageClassificationResults/ImageClassificationResults';
import ObjectDetectionResults from '../../components/ObjectDetectionResults/ObjectDetectionResults';
import SentimentClassification from '../../components/SentimentClassification/SentimentClassification';
import styles from './Results.module.css';

const Results = ({ data, images }) => {
  return (
    <div className={styles.resultsPage}>
      <h1 className={styles.resultTitle}>Analysis Results</h1>
      <div className={styles.resultList}>
        {images.map((image, idx) => {
          return (
            <div key={idx}>
              <h4>{image.name}</h4>
              <div className={styles.imageContainer}>
                <img
                  className={styles.image}
                  src={URL.createObjectURL(image)}
                  alt="results"
                />
              </div>
              <div>
                <div className={styles.gradient}>
                  <div className={styles.analysisHeader}>Color Analysis</div>
                </div>
                <div>{JSON.stringify(data.color_scheme_analysis)}</div>
                <div className={styles.gradient}>
                  <div className={styles.analysisHeader}>Object Detection</div>
                </div>
                <div>
                  <ObjectDetectionResults results={data.object_detection} />
                </div>
                <div className={styles.gradient}>
                  <div className={styles.analysisHeader}>
                    Image Classification
                  </div>
                </div>
                <div>
                  <ImageClassificationResults
                    results={data.image_classification}
                  />
                </div>
                <div className={styles.gradient}>
                  <div className={styles.analysisHeader}>
                    Sentiment Classification
                  </div>
                </div>
                <div>
                  <SentimentClassification
                    results={data.sentiment_analysis.image_1.degrees}
                  />
                </div>
                <div className={styles.gradient}>
                  <div className={styles.analysisHeader}>Text Recognition</div>
                </div>
                <div>
                  Extracted:{' '}
                  <div className="value">{data.text_recognition}</div>
                </div>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
};

export default Results;
