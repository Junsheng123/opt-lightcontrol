import React from 'react';
import classes from './App.module.css';

import VisionPanel from './components/VisionPanel/VisionPanel';
import LightControllerPanel from './components/LightControllerPanel/LightControllerPanel';
import FunctionPanel from './components/FunctionPanel/FunctionPanel';

function App() {
  return (
    <div className={classes.App}>
      <div className={classes.ControlPanel}>
        <div className={classes.VisionPanel}><VisionPanel /></div>
        <div className={classes.LightControlPanel}><LightControllerPanel /></div>
      </div>
      <div className={classes.FunctionPanel}><FunctionPanel /></div>
    </div>
    
  );
}

export default App;