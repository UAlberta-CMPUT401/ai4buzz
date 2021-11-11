import React from 'react';
import Spinner from './spinner.svg';

import styles from './LoadingOverlay.module.css';

const LoadingOverlay = () => {
  return (
    <div className={styles.loadingOverlay}>
      <object type="image/svg+xml" data={Spinner}>
        svg-animation
      </object>
    </div>
  );
};

export default LoadingOverlay;
