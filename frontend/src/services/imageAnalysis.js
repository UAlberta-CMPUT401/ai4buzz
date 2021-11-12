import axios from 'axios';

export const uploadImages = async (imageFiles) => {
  const formData = new FormData();
  for (let image of imageFiles) {
    formData.append('files', image);
  }
  return await axios.post('http://localhost:8000/getImageFeatures', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });
};
