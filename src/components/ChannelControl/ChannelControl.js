import React from 'react';
import classes from './ChannelControl.module.css';
import Slider from 'react-input-slider';

const channelControl = props => {
  const enableButtonClass = [classes.Button];
  if (props.chEnabled){
    enableButtonClass.push(classes.GreenBtn)
  }

  return (
    <div className={classes.ControlContainer}>
        <button className={enableButtonClass.join(' ')} type='button' onClick={(e)=>{props.chEnabledChanged(props.chId)}}>{'CH' + props.chId}</button>
        <div className={classes.Slider}>
          <Slider 
          axis="y" 
          ymax={255}
          ymin={0}
          y={props.intensity}
          yreverse={true}
          disabled={!props.chEnabled}
          onChange={({y})=>{props.intensityChanged(props.chId, y)}}
          styles={{
            track: {
              backgroundColor: 'gray',
              height: 400
            },
            active: {
              backgroundColor: 'lightgreen'
            },
            thumb: {
              width: 20,
              height: 20
            },
            disabled: {
              opacity: 0.5
            }
          }} />
        </div>
        <input type='number' value={props.intensity} onChange={(e)=>{props.intensityChanged(props.chId, e.target.value)}} disabled={props.chEnabled} />
    </div>
  );
}

export default channelControl;
