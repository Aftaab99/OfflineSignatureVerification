import React, { useState } from 'react';
import './Result.css'

function Result(props) {

    // if(props.threshold!==undefined && props.distance <= props.threshold){
    //     setLabelColorState("green")
    // }


    let field = <div></div>;
    let signatureVerdict = (props.threshold !== undefined && props.distance <= props.threshold) ? "Signature is authentic" : "Signature does not match to this customer id";

    if (props.threshold !== undefined)

        field = <div className="ResultContainer">
            <h4>Result</h4>
            <p>Signature threshold: {props.threshold}<br />
                    Image distance to closest database signature: <label style={{ color: (props.distance <= props.threshold ? "green" : "red") }}>{props.distance}</label>
            </p>
            <p style={{ color: (props.distance <= props.threshold ? "green" : "red") }}>{signatureVerdict}</p>
        </div>;
    return (field);
}

export default Result;