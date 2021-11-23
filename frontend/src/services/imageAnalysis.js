import axios from 'axios';
import getUrl from '../utils/getUrl';

export const uploadImages = async (imageFiles, access_token) => {
  const formData = new FormData();
  for (let image of imageFiles) {
    formData.append('files', image);
  }
  const baseUrl = getUrl();
  return await axios.post(
    `${baseUrl}/getImageFeatures?access_token=${access_token}`,
    formData,
    {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    }
  );
};
