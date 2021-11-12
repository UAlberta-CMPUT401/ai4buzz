import React, { useState } from 'react';
import { Route, useHistory } from 'react-router-dom';
import { uploadImages } from '../../services/imageAnalysis';
import LoadingOverlay from '../../components/LoadingOverlay/LoadingOverlay';

import styles from './AnalyzeImage.module.css';

const AnalyzeImage = ({ setResults, setFiles, files }) => {
  const history = useHistory();
  const [loading, setLoading] = useState(false);

  const handleUpload = async (e) => {
    // prevent page refresh
    e.preventDefault();
    setLoading(true);
    const res = await uploadImages(files);
    setResults(res.data);
    setLoading(false);
    history.push('/results');
  };

  const handleChangeFiles = (e) => {
    const fileArray = [];
    for (const [_, value] of Object.entries(e.target.files)) {
      fileArray.push(value);
    }
    setFiles(fileArray);
  };

  return (
    <>
      {loading ? <LoadingOverlay /> : null}
      <div className={styles.analyzeImagePage}>
        <form>
          <div>
            <h1>Upload Images</h1>
          </div>
          <div className={styles.images}>
            <h3>Images</h3>
            {files.length ? (
              files.map((file, idx) => {
                return (
                  <div className={styles.fileName} key={idx}>
                    {file.name}
                  </div>
                );
              })
            ) : (
              <div>No images selected</div>
            )}
          </div>
          <input
            className={styles.chooseFilesInput}
            type="file"
            multiple
            onChange={handleChangeFiles}
          />
          <div className="buttonGradient">
            <button
              className={styles.uploadImagesButton}
              onClick={handleUpload}
            >
              Analyze
            </button>
          </div>
        </form>
      </div>
    </>
  );
};

export default AnalyzeImage;
