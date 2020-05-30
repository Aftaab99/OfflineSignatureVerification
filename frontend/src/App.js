import React from 'react';
import logo from './logo.svg';
import ActionButton from './Components/ActionButton/ActionButton';
import TextField from './Components/TextField/TextField';
import BrowseImages from './Components/BrowseImages/BrowseImages'
import ThresholdComponent from './Containers/ThresholdContainer/ThresholdContainer'
import UploadImageContainer from './Containers/UploadImageContainer/UploadImageContainer'

import './App.css';

function App() {

  const handleClick = ()=>{console.log("Clicked")}

  return (
    <div>
      
      <UploadImageContainer imgLimit="3" headingText="Upload 3 new signatures of the customer" allowMultiple={true}/>
      <UploadImageContainer imgLimit="1" headingText="Upload a new signature to verify" allowMultiple={false}/>


    </div>
  );
}

export default App;
