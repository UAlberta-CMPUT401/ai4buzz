const Dendrogram = ({ imageBytes }) => {
  return (
    <div>
      <img src={`data:image/jpeg;base64,${imageBytes.collage}`} alt="collage" />
    </div>
  );
};

export default Dendrogram;
