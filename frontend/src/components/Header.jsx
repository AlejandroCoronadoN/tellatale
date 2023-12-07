import React from 'react';
import PropTypes from 'prop-types';
import "./styles/styles.css"

const Header = ({ imageData }) => {
  console.log(imageData);

  return (
    <header className="navbar navbar-sticky navbar-expand-lg navbar-dark">
      <div className="container position-relative">
        <a className="navbar-brand" href="/">
          <img className="navbar-brand-regular logo-white" src="/img/logo.png"alt=" LangChain and LLM" />
          <img className="navbar-brand-sticky logo-white" src="/img/logo.png" alt="sticky brand-logo" />
        </a>
        <button className="navbar-toggler d-lg-none" type="button" data-toggle="navbarToggler" aria-label="Toggle navigation">
          <span className="navbar-toggler-icon" />
        </button>

        <div className="navbar-inner">
          {/* Mobile Menu Toggler */}
          <button className="navbar-toggler d-lg-none" type="button" data-toggle="navbarToggler" aria-label="Toggle navigation">
            <span className="navbar-toggler-icon" />
          </button>
          <nav>
            <ul className="navbar-nav menu-font" id="navbar-nav">
              <li className="nav-item">
                <a className="nav-link" href="/">
                  Home
                </a>
              </li>

              <li className="nav-item">
                <a className="nav-link" href="/app">
                  App
                </a>
              </li>
            </ul>
          </nav>
        </div>
      </div>
    </header>
  );
};

Header.propTypes = {
  imageData: PropTypes.shape({
    // Adjust the structure based on your actual imageData properties
    text: PropTypes.number.isRequired,
    imageUrl: PropTypes.string.isRequired,
    altText: PropTypes.string.isRequired,
    // Add more properties as needed
  }),
};

export default Header;
