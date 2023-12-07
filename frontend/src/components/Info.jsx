import React from 'react';
import Header from './Header';
var imageData ={  // Adjust the structure based on your actual imageData properties
    text: "HEADER TEXT",
    imageUrl: "/img/logo.png"
}

const Info = () => {

    return (
      <div className="inner inner-pages">
        <div className="main">
        <Header 
                    imageData={imageData}  />    
          <section id="home" className="section welcome-area  h-100vh overflow-hidden">
            <div className="container h-100">
              <div className="row align-items-center h-100">
                <div className="col-12 col-md-8">
                  <div className="welcome-intro">
                    <h1 className="">{"Project Name"}</h1>
                    <p className=" my-4">{"Alejandro Coronado Narvaez"}</p>
                    <a href="/app" className="btn sApp-btn text-uppercase">{"Take me to the app"}</a>
                  </div>
                </div>
              </div>
            </div>
          </section>
        </div>
      </div>
    );
  
}

export default Info;