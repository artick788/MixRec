import logo from './logo.svg';
import './App.css';
import {useState} from "react";
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';

import Downloader from "./Pages/Downloader";
import Overview from "./Pages/Overview";
import Recommendations from "./Pages/Recommendations";
import {AppBar, Toolbar, Tabs, Tab} from "@mui/material";

function App() {
  return (
    <div className="App">
      <AppBar position="static">
        <Toolbar>
          <Tabs>
            <Tab label="Downloader" href="/downloader" />
            <Tab label="Overview" href="/overview" />
            <Tab label="Recommendations" href="/recommendations" />
          </Tabs>
        </Toolbar>
      </AppBar>
      <Router>
        <Routes>
          <Route path="/downloader" element={<Downloader />} />
          <Route path="/overview" element={<Overview />} />
          <Route path="/recommendations" element={<Recommendations />} />
        </Routes>
      </Router>
    </div>
  );
}

export default App;
