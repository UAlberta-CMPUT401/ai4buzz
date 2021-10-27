import { BrowserRouter as Router, Switch, Route } from 'react-router-dom';
import AnalyzeImage from './pages/AnalyzeImage/AnalyzeImage';
import Login from './pages/Login/Login';
import Signup from './pages/Signup/Signup';

import './App.css';

function App() {
  return (
    <Router>
      <Switch>
        <Route path="/analyze-image" exact component={AnalyzeImage} />
        <Route path="/login" exact component={Login} />
        <Route path="/signup" exact component={Signup} />
      </Switch>
    </Router>
  );
}

export default App;
