import React from 'react';
import TextField from '../../Components/TextField/TextField';
import BrowseImages from '../../Components/BrowseImages/BrowseImages';
import ActionButton from '../../Components/ActionButton/ActionButton';
import './UploadImageContainer.css'

function UploadImageContainer(props) {

    return (
        <div className="UploadImageContainer">
            <p>{props.headingText}</p>
            <TextField hint="Customer ID" />
            <ActionButton text="Upload" />
            <BrowseImages imgLimit={props.imgLimit} allowMultiple={props.allowMultiple}/>
        </div>
    )
}
export default UploadImageContainer;