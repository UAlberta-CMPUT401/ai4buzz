import axios from 'axios';

export const uploadImages = async (imageFiles, access_token) => {
  const formData = new FormData();
  for (let image of imageFiles) {
    formData.append('files', image);
  }
  return await axios.post(
    `http://localhost:8000/getImageFeatures?access_token=${access_token}`,
    formData,
    {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    }
  );
};
