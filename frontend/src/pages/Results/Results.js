import React from 'react';
import ImageClassificationResults from '../../components/ImageClassificationResults/ImageClassificationResults';
import ObjectDetectionResults from '../../components/ObjectDetectionResults/ObjectDetectionResults';
import SentimentClassification from '../../components/SentimentClassification/SentimentClassification';
import styles from './Results.module.css';

const Results = ({ featureAnalysisResults, images }) => {
  
  return (
    <div className={styles.resultsPage}>
      <div>
        <h1 className={styles.resultTitle}>Analysis Results</h1>
        <div className={styles.resultListContainer}>
          {images.map((image, idx) => {
            const imageFeatures = featureAnalysisResults[`image_${idx + 1}`];
            return (
              <div className={styles.imageFeatureResult} key={idx}>
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
                  <div>
                    {JSON.stringify(imageFeatures.color_scheme_analysis)}
                  </div>
                  <div className={styles.gradient}>
                    <div className={styles.analysisHeader}>
                      Object Detection
                    </div>
                  </div>
                  <div>
                    <ObjectDetectionResults
                      results={imageFeatures.object_detection}
                    />
                  </div>
                  <div className={styles.gradient}>
                    <div className={styles.analysisHeader}>
                      Image Classification
                    </div>
                  </div>
                  <div>
                    <ImageClassificationResults
                      results={imageFeatures.image_classification}
                    />
                  </div>
                  <div className={styles.gradient}>
                    <div className={styles.analysisHeader}>
                      Sentiment Classification
                    </div>
                  </div>
                  <div>
                    <SentimentClassification
                      results={imageFeatures.sentiment_analysis.degrees}
                    />
                  </div>
                  <div className={styles.gradient}>
                    <div className={styles.analysisHeader}>
                      Text Recognition
                    </div>
                  </div>
                  <div>
                    Extracted:
                    <div className="value">
                      {imageFeatures.text_recognition}
                    </div>
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
};

export default Results;