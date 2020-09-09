import React, { Fragment, useState, useEffect } from 'react';
import classes from './VisionPanel.module.css';

const electron = window.require('electron');
const ipcRenderer = electron.ipcRenderer;

function VisionPanel() {

    const [image, setImage] = useState(null);

    useEffect(() => {
        const onGetImage = (event, data) => {
            setImage(data.image)
        }
        ipcRenderer.on('reply_image', onGetImage);
        return () => {
            ipcRenderer.removeListener('reply_image', onGetImage);
        }
    }, [image])

    const snap = () => {
        ipcRenderer.send('snap');
    }
    const grab = () => {
        ipcRenderer.send('grab');
    }
    const grabStop = () => {
        ipcRenderer.send('grabStop');
    }

  return (
    <div className={classes.VisionPanel}>
        <div className={classes.Buttons}>
            <button className={classes.Button} type='button' onClick={grab}>Grab</button>
            <button className={classes.Button} type='button' onClick={snap}>Snap</button>
            <button className={classes.Button} type='button' onClick={grabStop}>Stop</button>
        </div>
        <div className={classes.ImageContainer}>
            <img src={`data:image/jpeg;base64,${image}`} alt='myimg'></img>
        </div>
    </div>
  );
}

export default VisionPanel;
