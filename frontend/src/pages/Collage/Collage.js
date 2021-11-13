import styles from './Collage.module.css';

const Collage = ({ imgString }) => {
  return (
    <div className={styles.collagePage}>
      <img
        className={styles.collage}
        src={`data:image/jpeg;base64,${imgString}`}
        alt="collage"
      />
    </div>
  );
};

export default Collage;
