import React, { useState } from 'react';
import { useHistory } from 'react-router-dom';
import { uploadImages } from '../../services/imageAnalysis';
import LoadingOverlay from '../../components/LoadingOverlay/LoadingOverlay';
import Cookies from 'js-cookie';

import styles from './AnalyzeImage.module.css';

const AnalyzeImage = ({ setResults, setFiles, files }) => {
  const history = useHistory();
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(false);

  const handleUpload = async (e) => {
    try {
      // prevent page refresh
      setError('');
      e.preventDefault();
      setLoading(true);
      const res = await uploadImages(files, Cookies.get('access_token'));
      setResults(res.data);
      setLoading(false);
      history.push('/results');
    } catch (err) {
      console.error(err);
      setError('There was an error during analysis.');
    } finally {
      setLoading(false);
    }
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
            <div className="error">{error}</div>
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
            accept="image/png, image/jpeg"
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
