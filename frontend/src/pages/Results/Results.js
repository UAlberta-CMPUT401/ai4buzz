import React from 'react';
import ColorAnalysisResults from '../../components/ColorAnalysisResults/ColorAnalysisResults';
import FacialAnalysisResults from '../../components/FacialAnalysisResults/FacialAnalysisResults';
import ImageClassificationResults from '../../components/ImageClassificationResults/ImageClassificationResults';
import ObjectDetectionResults from '../../components/ObjectDetectionResults/ObjectDetectionResults';
import SentimentClassification from '../../components/SentimentClassification/SentimentClassification';
import styles from './Results.module.css';

const Results = ({ results, images }) => {
  const downloadFile = ({ featureAnalysisResults, fileName, fileType }) => {
    const blob = new Blob([featureAnalysisResults], { type: fileType });

    const a = document.createElement('a');
    a.download = fileName;
    a.href = window.URL.createObjectURL(blob);
    const clickEvt = new MouseEvent('click', {
      view: window,
      bubbles: true,
      cancelable: true,
    });
    a.dispatchEvent(clickEvt);
    a.remove();
  };

  const exportToJson = (e) => {
    e.preventDefault();
    downloadFile({
      featureAnalysisResults: JSON.stringify(results),
      fileName: 'results.json',
      fileType: 'text/json',
    });
  };

  return (
    <div className={styles.resultsPage}>
      <div>
        <h1 className={styles.resultTitle}>Analysis Results</h1>

        <button type="button" onClick={exportToJson}>
          Export to JSON
        </button>

        <div className={styles.resultListContainer}>
          {results.feature_analysis_results.map((imageFeatures, idx) => {
            return (
              <div className={styles.imageFeatureResult} key={idx}>
                <h4>{imageFeatures.id}</h4>
                <div className={styles.imageContainer}>
                  <img
                    className={styles.image}
                    src={`data:image/jpeg;base64,${imageFeatures.object_detection.processes_bounding_boxes_image_as_base64_string}`}
                    alt="results"
                  />
                </div>
                <div>
                  <div className={styles.gradient}>
                    <div className={styles.analysisHeader}>Color Analysis</div>
                  </div>
                  <div>
                    <ColorAnalysisResults results={imageFeatures.color_scheme_analysis} />
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
                    {imageFeatures.text_recognition === '' ? (
                      'No text detected'
                    ) : (
                      <div>
                        Extracted:
                        <div className="value">
                          {imageFeatures.text_recognition}
                        </div>
                      </div>
                    )}
                  </div>
                  <div className={styles.gradient}>
                    <div className={styles.analysisHeader}>Facial Analysis</div>
                  </div>
                  <div>
                    <FacialAnalysisResults
                      facialResults={imageFeatures?.face_analysis?.analysis}
                    />
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
