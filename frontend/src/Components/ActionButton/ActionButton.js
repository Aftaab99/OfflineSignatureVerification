import React from 'react';
import './ActionButton.css';

function ActionButton(props){
    
    return(
         <button className="ActionButton" onClick={props.onClick} onClick={props.handleClick}>{props.text} </button>
    );
}
export default ActionButton;