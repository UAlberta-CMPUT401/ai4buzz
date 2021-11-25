import React from 'react';
import styles from './Dendrogram.module.css';

const Dendrogram = ({ imgString }) => {
  if (imgString) {
    return (
      <div className={styles.dendrogramPage}>
        <img className={styles.dendrogram} src={`data:image/jpeg;base64,${imgString}`} alt="collage" />
      </div>
    );
  }
  return (
    <div className={styles.dendrogramPage}>
      Need more than 1 photo to generate dendrogram
    </div>
  )
};

export default Dendrogram;
