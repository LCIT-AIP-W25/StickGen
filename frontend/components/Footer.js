import React from 'react';
import { Link } from 'react-router-dom';  // Import Link from react-router-dom
import { useLocation } from 'react-router-dom';
const Footer = () => {
  const location = useLocation();
  return (
    <footer className=" footer-section">
      <div className="container">
        <div className="row">
          {/* Brand and Tagline */}
          <div className="col-md-5 mb-4">
            <div className="footer-brand">
              <img 
                alt="logo" 
                src="logo.png" 
                className="img-fluid mb-3" 
                style={{ maxWidth: '150px' }} 
              />
              <p className="text-muted">
                Transforming news consumption with AI-powered analysis and engaging social media content generation.</p>
                <span><i className="fa fa-facebook"></i></span>
                <span><i className="fa fa-twitter"></i></span>
                <span><i className="fa fa-instagram"></i></span>
                <span><i className="fa fa-whatsapp"></i></span>
            </div>
          </div>

          {/* Quick Links */}
          <div className="col-md-1"></div>
          <div className="col-md-3 mb-4">
            <h3 className="h5 mb-3">QUICK LINKS</h3>
            <ul className="list-unstyled">
              <li className="mb-2">
                <Link to="/dashboard" className={`text-decoration-none ${location.pathname === '/dashboard' ? 'active' : ''}`}>Dashboard</Link>
              </li>
              <li className="mb-2">
                <Link to="/about" className={`text-decoration-none ${location.pathname === '/dashboard' ? 'active' : ''}`}>About Us</Link>
              </li>
              <li className="mb-2">
                <Link to="/stickers" className={`text-decoration-none ${location.pathname === '/dashboard' ? 'active' : ''}`}>Stickers</Link>
              </li>
              <li className="mb-2">
                <Link to="/api" className={`text-decoration-none ${location.pathname === '/dashboard' ? 'active' : ''}`}>API</Link>
              </li>
            </ul>
          </div>

          {/* Support */}
          <div className="col-md-3 mb-4">
            <h3 className="h5 mb-3">SUPPORT</h3>
            <ul className="list-unstyled">
              <li className="mb-2">
                <Link to="/contact" className={`text-decoration-none ${location.pathname === '/dashboard' ? 'active' : ''}`}>Contact</Link>
              </li>
              <li className="mb-2">
                <Link to="/terms-privacy" className={`text-decoration-none ${location.pathname === '/dashboard' ? 'active' : ''}`}>Privacy Policy</Link>
              </li>
            </ul>
          </div>
        </div>
        <hr/>
      </div>
      {/* Copyright Notice */}
      <div className="bg-white footer-bottom">
        <div className="container text-center">
          <p className="text-muted">
            © 2025 Iconque. All rights reserved.
          </p>
        </div>
      </div>
    </footer>
  );
};

export default Footer;