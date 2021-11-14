import React from 'react';
import styles from './FacialAnalysisResults.module.css';

const FacialAnalysisResults = ({ facialResults }) => {
  console.log(facialResults);
  return (
    <div>
      {facialResults.map((faceData, idx) => {
        return (
          <div key={idx}>
            <div>Emotion</div>
            <div className={styles.tabbedData}>
              <div>angry</div>
              <div className={styles.tabbedData}>{faceData.emotion.angry}</div>
              <div>disgust</div>
              <div className={styles.tabbedData}>
                {faceData.emotion.disgust}
              </div>
              <div>fear</div>
              <div className={styles.tabbedData}>{faceData.emotion.fear}</div>
              <div>happy</div>
              <div className={styles.tabbedData}>{faceData.emotion.happy}</div>
              <div>sad</div>
              <div className={styles.tabbedData}>{faceData.emotion.sad}</div>
              <div>surprise</div>
              <div className={styles.tabbedData}>
                {faceData.emotion.surprise}
              </div>
              <div>neutral</div>
              <div className={styles.tabbedData}>
                {faceData.emotion.neutral}
              </div>
            </div>

            <div>Dominant Emotion</div>
            <div className={styles.tabbedData}>{faceData.dominant_emotion}</div>

            <div>Region</div>
            <div className={styles.tabbedData}>
              <div>x</div>
              <div className={styles.tabbedData}>{faceData.region.x}</div>
              <div>y</div>
              <div className={styles.tabbedData}>{faceData.region.y}</div>
              <div>w</div>
              <div className={styles.tabbedData}>{faceData.region.w}</div>
              <div>h</div>
              <div className={styles.tabbedData}>{faceData.region.h}</div>
            </div>

            <div>Age</div>
            <div className={styles.tabbedData}>{faceData.age}</div>

            <div>Gender</div>
            <div className={styles.tabbedData}>{faceData.gender}</div>

            <div>Race</div>
            <div className={styles.tabbedData}>
              <div>Asian</div>
              <div className={styles.tabbedData}>{faceData.race['asian']}</div>
              <div>Indian</div>
              <div className={styles.tabbedData}>{faceData.race['indian']}</div>

              <div>Middle Eastern</div>
              <div className={styles.tabbedData}>
                {faceData.race['middle eastern']}
              </div>

              <div>White</div>
              <div className={styles.tabbedData}>{faceData.race['white']}</div>

              <div>Latino Hispanic</div>
              <div className={styles.tabbedData}>
                {faceData.race['latino hispanic']}
              </div>

              <div>Black</div>
              <div className={styles.tabbedData}>{faceData.race['black']}</div>
            </div>

            <div>Dominant Race</div>
            <div className={styles.tabbedData}>{faceData.dominant_race}</div>
          </div>
        );
      })}
    </div>
  );
};

export default FacialAnalysisResults;
