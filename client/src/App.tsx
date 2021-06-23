import React from 'react';
import './App.css';
import {
  BrowserRouter as Router,
  Switch,
  Route,
} from "react-router-dom";
import MainLayout from "./layouts/MainLayout";
import Dashboard from "./pages/Dashboard/Dashboard";
import {setupAxios} from "./config/axios";

function App() {
  setupAxios()
  return (
      <Router>
        <Switch>
          <Route path={"/dashboard"}>
            <MainLayout>
              <Dashboard />
            </MainLayout>
          </Route>
        </Switch>
      </Router>
  );
}

export default App;
