import React from 'react';
import { Navbar, Nav } from 'react-bootstrap';
import { Link, useLocation } from 'react-router-dom';

const Header = () => {
  const location = useLocation();

  return (
    <div className="header-section">
      <div className="container">
        <Navbar expand="lg">
          <Navbar.Brand as={Link} to="/">
            <img alt="logo" src="logo.png" />
          </Navbar.Brand>
          <Navbar.Toggle aria-controls="basic-navbar-nav" />
          <Navbar.Collapse id="basic-navbar-nav">
            <Nav className="ml-auto">
              <Nav.Link 
                as={Link} 
                to="/" 
                active={location.pathname === '/'}
              >
                Home
              </Nav.Link>
              <Nav.Link 
                as={Link} 
                to="/dashboard" 
                active={location.pathname === '/dashboard'}
              >
                Dashboard
              </Nav.Link>
              <Nav.Link 
                as={Link} 
                to="/about" 
                active={location.pathname === '/about'}
              >
                About
              </Nav.Link>
            </Nav>
          </Navbar.Collapse>
        </Navbar>
      </div>
    </div>
  );
};

export default Header;