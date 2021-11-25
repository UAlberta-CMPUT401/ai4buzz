import styles from './Collage.module.css';

const Collage = ({ imgString }) => {
  if (imgString) {

  return (
    <div className={styles.collagePage}>
      <img
        className={styles.collage}
        src={`data:image/jpeg;base64,${imgString}`}
        alt="collage"
      />
    </div>
  );
  }
  return (
    <div className={styles.collagePage}>
      Need more than 1 photo to generate collage
    </div>
  )
};

export default Collage;
