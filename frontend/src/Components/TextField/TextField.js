import React from 'react'
import './TextField.css'

function TextField(props){
    return (<input className='TextField' type="text" placeholder={props.hint}/>)
}

export default TextField;
