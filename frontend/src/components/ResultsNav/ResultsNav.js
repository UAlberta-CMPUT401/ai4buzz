import React, { useState } from 'react';
import { useHistory, useLocation } from 'react-router-dom';
import styles from './ResultsNav.module.css';

const ResultsNav = ({ children }) => {
  const history = useHistory();
  const location = useLocation();

  const path = location.pathname;

  return (
    <div className="container">
      <div className={styles.navbar}>
        <div
          className={`${styles.navTab} ${
            path === '/results' ? styles.navTabActive : ''
          }`}
          onClick={() => history.push('/results')}
        >
          Results
        </div>
        <div
          className={`${styles.navTab} ${
            path === '/collage' ? styles.navTabActive : ''
          }`}
          onClick={() => history.push('/collage')}
        >
          Collage
        </div>
        <div
          className={`${styles.navTab} ${
            path === '/dendrogram' ? styles.navTabActive : ''
          }`}
          onClick={() => history.push('/dendrogram')}
        >
          Dendrogram
        </div>
      </div>
      {children}
    </div>
  );
};

export default ResultsNav;
