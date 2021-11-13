const Dendrogram = ({ imgString }) => {
  return (
    <div>
      <img src={`data:image/jpeg;base64,${imgString}`} alt="collage" />
    </div>
  );
};

export default Dendrogram;
