import React from 'react';
import './App.css';
import {
  BrowserRouter as Router,
  Switch,
  Route,
} from "react-router-dom";
import MainLayout from "./layouts/MainLayout";
import Dashboard from "./pages/Dashboard/Dashboard";
import Batches from "./pages/Batches/Batches";
import {setupAxios} from "./config/axios";
import Steps from "./pages/Steps/Steps";

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
          <Route path={"/batches"}>
            <MainLayout>
                <Batches />
            </MainLayout>
          </Route>
            <Route path={"/steps"}>
                <MainLayout>
                    <Steps />
                </MainLayout>
            </Route>
        </Switch>
      </Router>
  );
}

export default App;
