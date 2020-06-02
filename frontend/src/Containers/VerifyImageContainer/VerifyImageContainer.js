import React, { useState } from 'react';
import TextField from '../../Components/TextField/TextField';
import BrowseImages from '../../Components/BrowseImages/BrowseImages';
import ActionButton from '../../Components/ActionButton/ActionButton';
import Result from '../../Components/Result/Result'
import './VerifyImageContainer.css'

function VerifyImageContainer(props) {
    const [fileUrl, setFileUrl] = useState(new Array(props.imgLimit).fill(null));
    const [filesValid, setFilesValid] = useState(false);
    const [threshold, setThreshold] = useState(undefined);
    const [distance, setDistance] = useState(undefined);
    const [customerID, setCustomerID] = useState("");
    const [file, setFile] = useState(new Array(props.imgLimit).fill(undefined));
    const [errorColor, setErrorColor] = useState("red");
    const [errorText, setErrorText] = useState("");
    const postData = (event) => {
        event.preventDefault();
        if (filesValid) {
            setThreshold(undefined);
            setDistance(undefined);
            setErrorText("Loading..")
            setErrorColor("gray")
            const xhr = new XMLHttpRequest();
            let formdata = new FormData();
            formdata.append("newSignature", file[0]);
            formdata.append("customerID", customerID);

            xhr.open("POST", '/verify', true);
            // xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
            xhr.onreadystatechange = function () {
                if (xhr.readyState === 4 && xhr.status === 200) {
                    let res = JSON.parse(xhr.responseText);
                    if (res.error == true) {
                        setErrorText("Something went wrong the server");
                        setErrorColor("red");
                    }
                    else {
                        setErrorText("");
                        console.log(res.threshold)
                        console.log(res.distance)
                        setThreshold(parseFloat(res.threshold))
                        setDistance(parseFloat(res.distance))
                        
                    }
                }

            };

            xhr.send(formdata);

        }
    }
    return (
        <div className="VerifyImageContainer">
            <p>{props.headingText}</p>
            <TextField hint="Customer ID" customerID={customerID} setCustomerID={setCustomerID} />
            <ActionButton text={props.submitButtonText} handleClick={postData} />
            <BrowseImages imgLimit={props.imgLimit} allowMultiple={props.allowMultiple} fileUrl={fileUrl} setFileUrl={setFileUrl} filesValid={filesValid} setFilesValid={setFilesValid} file={file} setFile={setFile} />
            <label style={{ color: errorColor }}>{errorText}</label>

            <Result style={{ display: (errorText == "") ? "inline" : "none" }} threshold={threshold} setThreshold={setThreshold} distance={distance} setDistance={setDistance} />
        </div>
    )
}
export default VerifyImageContainer;