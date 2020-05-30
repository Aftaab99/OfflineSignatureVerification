import React, { useState } from 'react';
import './BrowseImages.css';

function BrowseImages(props) {
    const [fileUrl, setFileUrl] = useState(new Array(props.imgLimit).fill(null));
    const [filesValid, setFilesValid] = useState(false);
    const [errorText, setErrorText] = useState("")
    console.log(props.imgLimit)
    const handleChange = (event) => {
        let newFileUrl = []
        for (let i = 0; i < parseInt(event.target.files.length); i++) {
            newFileUrl.push(URL.createObjectURL(event.target.files[i]))
        }
        setFileUrl(newFileUrl);

        if (event.target.files.length !== parseInt(props.imgLimit)) {
            setFilesValid(false);
            setErrorText("Please select exactly " + props.imgLimit + " images")
            return;
        }

        setFilesValid(true);
        setErrorText("");
    }
    let inputField = (props.allowMultiple==true)?
        <input type="file" onChange={handleChange} multiple accept="image/*" />
        :<input type="file" onChange={handleChange} accept="image/*" />;
    return (
        <div className="BrowseImages">
            {inputField}
            <div>
                {fileUrl.map(function (val, index) {
                    return <img src={val} key={index} width="10%" />
                })
                }</div>
            <label>{errorText}</label>
        </div>);
}
export default BrowseImages;