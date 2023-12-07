import React, {  useState } from 'react';
import deckContent from './deckContent.json';
import "./styles/styles.css"

const Deck = () => {
  const [productName, setProductName] = useState('');
  console.log(productName)
      //e.preventDefault();
    return (
      <section id="pricing" className="section price-plan-area bg-gray overflow-hidden ptb_100">
        <div className="container">
          <div className="row justify-content-center">
            <div className="col-12 col-md-10 col-lg-7">
              {/* Section Heading */}
              <div className="section-heading text-center">
                <h2>H1</h2>
                <p className="d-none d-sm-block mt-4">P1</p>
                <p className="d-block d-sm-none mt-4">P2</p>
              </div>
            </div>
          </div>
          <div className="row justify-content-center">
            <div className="col-12 col-sm-12 col-lg-12">
              <div className="row price-plan-wrapper">
                {deckContent.map((item, idx) => {
                  return(
                    <div key={`p_${idx}`} className="col-12 col-md-4 mt-3">
                      {/* Single Price Plan */}
                      <div className="single-price-plan text-center p-5">
                        {/* Plan Thumb */}
                        <div className="deck-thumb">
                          <img className="avatar-lg" src={item.deckImage} alt="" />
                        </div>
                        {/* Plan Title */}
                        <div className="deck-title my-2 my-sm-3">
                          <h3 className="text-uppercase">{item.deckTile}</h3>
                        </div>
                        {/* Plan Price */}
                        <div className="deck-price pb-2 pb-sm-3">
                          <h1 className="color-primary"><small className="fw-7">{item.deckSub}</small>{item.deckInfo}</h1>
                        </div>
                        {/* Plan Description */}
                        <div className="deck-description">
                          <ul className="deck-features">
                            <li className="border-top py-3">{item.li_1}</li>
                            <li className="border-top py-3">{item.li_2}</li>
                            <li className="border-top border-bottom py-3">{item.li_3}</li>

                            
                          </ul>
                        </div>
                        {/* Plan Button */}
                        <div className="deck-button" 
                          onClick={() => {     
                            setProductName(item.category);
                            }}>
                          <a  className="btn mt-4">{item.deckBtn}</a>
                        </div>
                      </div>
                    </div>
                  );
                })}
              </div>
            </div>
          </div>
          <div className="row justify-content-center pt-5">
            <p className="text-body pt-4 fw-5">TEXT 1 <a href="/contact">TEXT 2</a></p>
          </div>
        </div>



      </section>
    );
  
}

export default Deck;