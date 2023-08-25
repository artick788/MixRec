import logo from './logo.svg';
import './App.css';
import {useState} from "react";
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';

import Downloader from "./Pages/Downloader";
import Overview from "./Pages/Overview";
import Searcher from "./Pages/Searcher";
import IndexPage from "./Pages/IndexPage";
import {AppBar, Toolbar, Tabs, Tab, ThemeProvider, createTheme} from "@mui/material";

const theme = createTheme({

});

function App() {
  return (
    <div className="App">
      <ThemeProvider theme={theme}>
        <AppBar position="static">
          <Toolbar>
            <Tabs>
              <Tab label="Downloader" href="/downloader" />
              <Tab label="Overview" href="/overview" />
              <Tab label="Searcher" href="/searcher" />
              <Tab label="Index" href="/index" />
            </Tabs>
          </Toolbar>
        </AppBar>
        <Router>
          <Routes>
            <Route path="/downloader" element={<Downloader />} />
            <Route path="/overview" element={<Overview />} />
            <Route path="/searcher" element={<Searcher />} />
            <Route path="/index" element={<IndexPage />} />
          </Routes>
        </Router>
      </ThemeProvider>
    </div>
  );
}

export default App;
