import React, { useState, useEffect } from 'react';
import classes from './FunctionPanel.module.css';

const electron = window.require('electron');
const ipcRenderer = electron.ipcRenderer;


function FunctionPanel() {

    const saveSettingHandler = ()=>{
      ipcRenderer.send('saveSetting');
    }
    const saveImageHandler = ()=>{
      ipcRenderer.send('saveImage');
    }

    return (
    <div className={classes.FunctionContainer}>
      <button className={classes.Button} type='button' onClick={saveSettingHandler}>Save Setting</button>
      <button className={classes.Button} type='button' onClick={saveImageHandler}>Save Image</button>
    </div>
  );
}

export default FunctionPanel;
