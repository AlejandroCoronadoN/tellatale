import React from 'react';
import { createRoot } from 'react-dom';
import './index.css';
import App from './App';


// Use createRoot instead of ReactDOM.render
const root = createRoot(document.getElementById('root'));
root.render(<App />);
