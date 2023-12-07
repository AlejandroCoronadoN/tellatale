import React, { useState } from 'react';
import Form from 'react-bootstrap/Form';
import Button from 'react-bootstrap/Button';
import Container from 'react-bootstrap/Container';
import Col from 'react-bootstrap/Col';
import Row from 'react-bootstrap/Row';
import './App.css';
import { getProduct, getUser } from './utils';

/**
 * Functional component for the single-page app.
 *
 * @returns {JSX.Element} - React JSX element representing the application.
 */
function App() {
  // State to manage the input values
  const [userValue, setUserValue] = useState('');
  const [productValue, setProductValue] = useState('');
  const [userResponse, setUserRespose] = useState("");
  const [productResponse, setProductRespose] = useState("");

  /**
   * Handles user input change.
   *
   * @param {Object} event - The input change event.
   */
  const handleUserChange = (event) => {
    setUserValue(event.target.value);
  };


  /**
   * Handles user input change.
   *
   * @param {Object} event - The input change event.
   */
  const handleProductChange = (event) => {
    setProductValue(event.target.value);
  };

  const clickProduct = async () => {
    try {
      const product = await getProduct(productValue);
      setProductRespose(JSON.stringify( product ))
    } catch (error) {
      console.error(error);
    }
  };
  /**
   * Handles "SCAN USER" button click.
   */
  const clickUser = async () => {
    try {
      const user = await getUser(userValue);
      setUserRespose(JSON.stringify( user ))
      console.log(user);
    } catch (error) {
      console.error(error);
    }
  };


  return (
    <Container>
      {/* Blue header line with project name */}
      <Row>
        <Col md={12} className="header-line">
          {/* Full-width column for the header */}
          Reece SCO
        </Col>
      </Row>

      {/* User input row */}
      <Row>
        <Col md={{ span: 4, offset: 4 }}>
          {/* Bootstrap Form for user input with offset 4 */}
          <Form.Group controlId="userInput">
            <Form.Control
              type="text"
              placeholder="Enter user"
              value={userValue}
              onChange={handleUserChange}
            />
          </Form.Group>
          <Button variant="primary" onClick={clickUser}>
            SCAN USER
          </Button>
        </Col>
      </Row>

      {/* Product input row */}
      <Row>
        <Col md={{ span: 4, offset: 4 }}>
          {/* Bootstrap Form for product input with offset 4 */}
          <Form.Group controlId="productInput">
            <Form.Control
              type="text"
              placeholder="Enter product"
              value={productValue}
              onChange={handleProductChange}
            />
          </Form.Group>
          <Button variant="primary" onClick={clickProduct}>
            SCAN PRODUCT
          </Button>
        </Col>
      </Row>

      {/* Display userValue and productValue */}
      <Row>
        <Col md={12}>
          <div>
            <strong>User Value:</strong> 
            {JSON.stringify( userResponse)}
          </div>
          <div>
            <strong>Product Value:</strong> 
            {JSON.stringify( productResponse)}
          </div>
        </Col>
      </Row>
    </Container>
  );
}

export default App;
