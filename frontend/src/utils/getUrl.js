const getUrl = () => {
    let baseUrl = process.env.REACT_APP_LOCAL_URL;
    if (process.env.NODE_ENV === 'production') {
      baseUrl = process.env.REACT_APP_PROD_URL;
    }
    return baseUrl;
}

export default getUrl