import React, { useState } from 'react';
import './BrowseImages.css';

function BrowseImages(props) {

    const [errorText, setErrorText] = useState("")
    const handleChange = (event) => {

        const fileArr = Array.from(event.target.files)
        Promise.all(fileArr.map((f) => {
            return (new Promise((resolve, reject) => {
                const reader = new FileReader();
                reader.addEventListener('load', (ev) => {
                    resolve(ev.target.result);
                });
                reader.addEventListener('error', reject);
                reader.readAsDataURL(f);
            }))
        })).then(images => {
            props.setFileUrl(images)
        })

        props.setFile(event.target.files);

        if (event.target.files.length !== parseInt(props.imgLimit)) {
            props.setFilesValid(false);
            setErrorText("Please select exactly " + props.imgLimit + " images")
            return;
        }

        props.setFilesValid(true);
        setErrorText("");
    }
    let inputField = (props.allowMultiple == true) ?
        <input type="file" onChange={handleChange} multiple accept="image/*" />
        : <input type="file" onChange={handleChange} accept="image/*" />;
    return (
        <div className="BrowseImages">
            {inputField}
            <div>
                {props.fileUrl.map(function (val, index) {

                    return <img src={val} key={index} width="10%" />
                })
                }
            </div>
            <label>{errorText}</label>
        </div>);
}
export default BrowseImages;