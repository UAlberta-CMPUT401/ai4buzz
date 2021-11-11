import { useState } from 'react';
import { BrowserRouter as Router, Switch, Route } from 'react-router-dom';
import AnalyzeImage from './pages/AnalyzeImage/AnalyzeImage';
import Login from './pages/Login/Login';
import Signup from './pages/Signup/Signup';
import Collage from './pages/Collage/Collage';
import Results from './pages/Results/Results';
import Dendrogram from './pages/Dendrogram/Dendrogram';
import './App.css';
import ResultsNav from './components/ResultsNav/ResultsNav';

function App() {
  const [images, setImages] = useState([]);
  const [results, setResults] = useState();

  return (
    <Router>
      <Switch>
        <Route path="/login" exact component={Login} />
        <Route path="/signup" exact component={Signup} />
        <Route
          path="/analyze-image"
          exact
          render={() => {
            return (
              <AnalyzeImage
                setResults={setResults}
                setFiles={setImages}
                files={images}
              />
            );
          }}
        />
        <ResultsNav>
          <Route
            path="/results"
            exact
            component={() => {
              return <Results data={results} images={images} />;
            }}
          />
          <Route
            path="/collage"
            exact
            component={() => {
              return <Collage data={results} />;
            }}
          />
          <Route
            path="/dendrogram"
            exact
            component={() => {
              return <Dendrogram data={results} />;
            }}
          />
        </ResultsNav>
      </Switch>
    </Router>
  );
}

export default App;
