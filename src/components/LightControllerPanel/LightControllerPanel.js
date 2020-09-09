import React, { useState, useEffect } from 'react';
import classes from './LightControllerPanel.module.css';

import ChannelControl from '../ChannelControl/ChannelControl';

const electron = window.require('electron');
const ipcRenderer = electron.ipcRenderer;


function LightControllerPanel() {
  let timeout;
  const [ip, setIp] = useState('192.168.1.16');
  const [connected, setConnected] = useState(false);
  const [chEnableStates, setChEnableStates] = useState([false, false, false, false]);
  const [chIntensities, setChIntensities] = useState([0, 0, 0, 0]);

  const changeIpHandler = (e) => {
    setIp(e.target.value)
  }

  const connectControllerHandler = (e) => {
    ipcRenderer.send('connectController', ip);
  }
  const intensityHandler = (chId, value) => {
    const newIntensity = parseInt(value);
    const updatedIntensity = [...chIntensities];
    updatedIntensity.splice(chId - 1, 1, newIntensity);
    setChIntensities(updatedIntensity);
    timeout && clearTimeout(timeout);
    timeout = setTimeout(() => {
      ipcRenderer.send('change_intensity', chId, newIntensity);
    }, 100);

  }
  const enableChannelHandler = (chId) => {
    ipcRenderer.send('enable_channel', chId);
  }

  useEffect(() => {
    const onLoadSetting = (event, data) => {
      setChIntensities(data)
    }
    ipcRenderer.on('reply_loadSetting', onLoadSetting);
    return () => {
      ipcRenderer.removeListener('reply_loadSetting', onLoadSetting);
    }
  }, [chIntensities])

  useEffect(() => {
    const onConnectController = (event, data) => {
      if (data === true) {
        setConnected(true)
      } else {
        setConnected(false)
      }
    }
    ipcRenderer.on('reply_connect_controller', onConnectController);
    return () => {
      ipcRenderer.removeListener('reply_connect_controller', onConnectController);
    }
  }, [connected])

  useEffect(() => {
    const onGetAllIntensity = (event, data) => {
      setChIntensities(data)
    }
    ipcRenderer.on('reply_read_all_intensity', onGetAllIntensity);
    return () => {
      ipcRenderer.removeListener('reply_read_all_intensity', onGetAllIntensity);
    }
  }, [chIntensities])

  useEffect(() => {
    const onGetAllChState = (event, data) => {
      setChEnableStates(data)
    }
    ipcRenderer.on('reply_read_all_ch_state', onGetAllChState);
    return () => {
      ipcRenderer.removeListener('reply_read_all_ch_state', onGetAllChState);
    }
  }, [chEnableStates])

  const connectButtonClass = [classes.Button];
  if (connected) {
    connectButtonClass.push(classes.GreenBtn);
  }

  return (
    <div className={classes.LightcontrolPanel}>
      <div className={classes.ConnectContainer}>
        <label style={{ marginRight: '20px' }}>IP</label>
        <input value={ip} onChange={changeIpHandler} />
        <button className={connectButtonClass.join(' ')} type='button' onClick={connectControllerHandler}>Connect</button>
      </div>
      <div className={classes.ChannelControlContainer}>
        <ChannelControl
          chId={1}
          chEnabled={chEnableStates[0]}
          chEnabledChanged={enableChannelHandler}
          intensity={chIntensities[0]}
          intensityChanged={intensityHandler} />
        <ChannelControl
          chId={2}
          chEnabled={chEnableStates[1]}
          chEnabledChanged={enableChannelHandler}
          intensity={chIntensities[1]}
          intensityChanged={intensityHandler} />
        <ChannelControl
          chId={3}
          chEnabled={chEnableStates[2]}
          chEnabledChanged={enableChannelHandler}
          intensity={chIntensities[2]}
          intensityChanged={intensityHandler} />
        <ChannelControl
          chId={4}
          chEnabled={chEnableStates[3]}
          chEnabledChanged={enableChannelHandler}
          intensity={chIntensities[3]}
          intensityChanged={intensityHandler} />
      </div>
    </div>
  );
}

export default LightControllerPanel;
