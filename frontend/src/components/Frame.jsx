import Header from './Header';
import Breadcrumb from './Breadcrumb.jsx';
import Deck from './Deck';
import React from 'react';

var imageData ={  // Adjust the structure based on your actual imageData properties
    text: "HEADER TEXT",
    imageUrl: "/img/logo.png"
}
const Frame = () => {
    return (
      <div>
        {/*====== Scroll To Top Area Start ======*/}
        <div id="scrollUp" title="Scroll To Top">
          <i className="fas fa-arrow-up" />
        </div>
        {/*====== Scroll To Top Area End ======*/}
        <div className="main">
        <Header 
                    imageData={imageData}  />    
          <Breadcrumb title="BREADCRUMB T" />
          <Deck />
        </div>
      </div>
    );
  
}

export default Frame;