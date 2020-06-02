import React, {useState} from 'react';
import UploadImageContainer from './Containers/UploadImageContainer/UploadImageContainer'
import VerifyImageContainer from './Containers/VerifyImageContainer/VerifyImageContainer'

import './App.css';

function App() {


  return (
    <div className="App">
        <h1>Signature Verification web demo</h1>
        <UploadImageContainer imgLimit="3" submitButtonText="Upload" headingText="Upload 3 new signatures of the customer" allowMultiple={true}/>
        <VerifyImageContainer imgLimit="1" submitButtonText="Verify" headingText="Upload a new signature of the customer to verify" allowMultiple={false}/>

    </div>
  );
}

export default App;
