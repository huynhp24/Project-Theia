import React, { Component } from 'react'
import Objectdetection from './components/Objectdetection';
import TabPanel from './components/TabPanel';

import './App.css';

class App extends Component {
  render() {
    return (
    <div className="App">
      <Objectdetection />
      <TabPanel />
    </div>
    );
  }
  
}

export default App;
