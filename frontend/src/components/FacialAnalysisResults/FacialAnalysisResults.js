import React from 'react';
import styles from './FacialAnalysisResults.module.css';

const FacialAnalysisResults = ({ facialResults }) => {
  return (
    <div>
      {facialResults.length
        ? facialResults.map((faceData, idx) => {
            return (
              <div key={idx}>
                <div className={styles.faceResults}>
                  <div>Age</div>
                  <div className="value">{faceData.age}</div>
                </div>

                <div className={styles.faceResults}>
                  <div>Gender</div>
                  <div className="value">{faceData.gender}</div>
                </div>

                <div className={styles.faceResults}>
                  <div>Dominant Emotion</div>
                  <div className="value">{faceData.dominant_emotion}</div>
                </div>

                <div>Emotion</div>
                <div className={styles.tabbedData}>
                  <div className={styles.faceResults}>
                    <div>angry</div>
                    <div className="value">
                      {faceData.emotion.angry.toFixed(3)}%
                    </div>
                  </div>
                  <div className={styles.faceResults}>
                    <div>disgust</div>
                    <div className="value">
                      {faceData.emotion.disgust.toFixed(3)}%
                    </div>
                  </div>
                  <div className={styles.faceResults}>
                    <div>fear</div>
                    <div className="value">
                      {faceData.emotion.fear.toFixed(3)}%
                    </div>
                  </div>
                  <div className={styles.faceResults}>
                    <div>happy</div>
                    <div className="value">
                      {faceData.emotion.happy.toFixed(3)}%
                    </div>
                  </div>
                  <div className={styles.faceResults}>
                    <div>sad</div>
                    <div className="value">
                      {faceData.emotion.sad.toFixed(3)}%
                    </div>
                  </div>
                  <div className={styles.faceResults}>
                    <div>surprise</div>
                    <div className="value">
                      {faceData.emotion.surprise.toFixed(3)}%
                    </div>
                  </div>
                  <div className={styles.faceResults}>
                    <div>neutral</div>
                    <div className="value">
                      {faceData.emotion.neutral.toFixed(3)}%
                    </div>
                  </div>
                </div>

                <div className={styles.faceResults}>
                  <div>Dominant Race</div>
                  <div className="value">{faceData.dominant_race}</div>
                </div>

                <div>Race</div>
                <div className={styles.tabbedData}>
                  <div className={styles.faceResults}>
                    <div>Asian</div>
                    <div className="value">
                      {faceData.race['asian'].toFixed(3)}%
                    </div>
                  </div>
                  <div className={styles.faceResults}>
                    <div>Indian</div>
                    <div className="value">
                      {faceData.race['indian'].toFixed(3)}%
                    </div>
                  </div>
                  <div className={styles.faceResults}>
                    <div>Middle Eastern</div>
                    <div className="value">
                      {faceData.race['middle eastern'].toFixed(3)}%
                    </div>
                  </div>
                  <div className={styles.faceResults}>
                    <div>White</div>
                    <div className="value">
                      {faceData.race['white'].toFixed(3)}%
                    </div>
                  </div>
                  <div className={styles.faceResults}>
                    <div>Latino Hispanic</div>
                    <div className="value">
                      {faceData.race['latino hispanic'].toFixed(3)}%
                    </div>
                  </div>
                  <div className={styles.faceResults}>
                    <div>Black</div>
                    <div className="value">
                      {faceData.race['black'].toFixed(3)}%
                    </div>
                  </div>
                </div>

                <div>Region</div>
                <div className={styles.tabbedData}>
                  <div className={styles.faceResults}>
                    <div>x</div>
                    <div className="value">{faceData.region.x}</div>
                  </div>
                  <div className={styles.faceResults}>
                    <div>y</div>
                    <div className="value">{faceData.region.y}</div>
                  </div>
                  <div className={styles.faceResults}>
                    <div>w</div>
                    <div className="value">{faceData.region.w}</div>
                  </div>
                  <div className={styles.faceResults}>
                    <div>h</div>
                    <div className="value">{faceData.region.h}</div>
                  </div>
                </div>
              </div>
            );
          })
        : 'No faces detected'}
    </div>
  );
};

export default FacialAnalysisResults;
