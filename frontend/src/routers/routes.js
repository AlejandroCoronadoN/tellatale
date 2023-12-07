import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";

import Frame from "../components/Frame";
import Info from "../components/Info";

class MyRoutes extends React.Component {
  render() {
    return (
      <Router>
        <Routes>
          <Route path="/app" element={<Info />} />
          <Route path="/" element={<Frame />} />

          {/* Add more routes as needed */}
        </Routes>
      </Router>
    );
  }
}

export default MyRoutes;
