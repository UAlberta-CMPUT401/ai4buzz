import React from 'react';
import Spinner from './spinner.svg';

import styles from './LoadingOverlay.module.css';

const LoadingOverlay = () => {
  return (
    <div className={styles.loadingOverlay}>
      <div>
        <object type="image/svg+xml" data={Spinner}>
          svg-animation
        </object>
        <div style={{ textAlign: 'center' }}>This might take a bit...</div>
      </div>
    </div>
  );
};

export default LoadingOverlay;
