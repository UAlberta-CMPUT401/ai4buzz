import { useState } from 'react';
import {
  BrowserRouter as Router,
  Switch,
  Route,
  Redirect,
} from 'react-router-dom';
import AnalyzeImage from './pages/AnalyzeImage/AnalyzeImage';
import Login from './pages/Login/Login';
import Signup from './pages/Signup/Signup';
import Collage from './pages/Collage/Collage';
import Results from './pages/Results/Results';
import Dendrogram from './pages/Dendrogram/Dendrogram';
import './App.css';
import ResultsNav from './components/ResultsNav/ResultsNav';
import AuthenticatedRoute from './components/AuthenticatedRoute/AuthenticatedRoute';

function App() {
  const [images, setImages] = useState([]);
  const [results, setResults] = useState();

  return (
    <Router>
      <Switch>
        <Route exact path="/">
          <Redirect to="/analyze-image" />
        </Route>
        <Route path="/login" exact component={Login} />
        <Route path="/signup" exact component={Signup} />
        <AuthenticatedRoute
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
          <AuthenticatedRoute
            path="/results"
            exact
            component={() => {
              return (
                <Results
                  featureAnalysisResults={results?.feature_analysis_results}
                  images={images}
                />
              );
            }}
          />
          <AuthenticatedRoute
            path="/collage"
            exact
            component={() => {
              return <Collage imgString={results?.collage_image_string} />;
            }}
          />
          <AuthenticatedRoute
            path="/dendrogram"
            exact
            component={() => {
              return <Dendrogram data={results?.dendrogram_image_string} />;
            }}
          />
        </ResultsNav>
      </Switch>
    </Router>
  );
}

export default App;
