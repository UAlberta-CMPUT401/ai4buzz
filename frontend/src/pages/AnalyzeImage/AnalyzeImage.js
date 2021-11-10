import React, { useState } from 'react';
import { uploadImages } from '../../services/imageAnalysis';

const AnalyzeImage = () => {
  const [files, setFiles] = useState();

  const handleUpload = async (e) => {
    e.preventDefault();
    await uploadImages(files);
  };

  const handleChangeFiles = (e) => {
    const fileArray = [];
    for (const [key, value] of Object.entries(e.target.files)) {
      fileArray.push(value);
    }
    console.log(fileArray);
    setFiles(fileArray);
  };

  return (
    <div>
      <form>
        <div>
          <h2>Upload images</h2>
        </div>
        <h3>Images</h3>
        <input type="file" multiple onChange={handleChangeFiles} />
        <button onClick={handleUpload}>Analyze</button>
      </form>
    </div>
  );
};

export default AnalyzeImage;
