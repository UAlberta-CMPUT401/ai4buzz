import React from 'react';
import Cookies from 'js-cookie';
import { Redirect, Route } from 'react-router-dom';

const AuthenticatedRoute = (props) => {
  if (Cookies.get('access_token')) {
    return <Route {...props} />;
  }
  return <Redirect to="/login" />;
};

export default AuthenticatedRoute;
