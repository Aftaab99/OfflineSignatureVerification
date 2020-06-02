import React from 'react'
import './TextField.css'

function TextField(props){
    const handleChange = (event)=>{
        props.setCustomerID(event.target.value);
    }

    return (<input className='TextField' type="text"  placeholder={props.hint} onChange={handleChange}/>)
}

export default TextField;
