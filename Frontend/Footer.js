import React from 'react';

const Footer = () => {
  return (
    <footer className="bg-white footer-section">
      <div className="container">
        <div className="row">
          {/* Brand and Tagline */}
          <div className="col-md-6 mb-4">
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
                <span><i className="fa fa-linkedin"></i></span>
            </div>
          </div>

          {/* Quick Links */}
          <div className="col-md-3 mb-4">
            <h3 className="h5 mb-3">QUICK LINKS</h3>
            <ul className="list-unstyled">
              <li className="mb-2">
                <a href="/dashboard" className="text-decoration-none">Dashboard</a>
              </li>
              <li className="mb-2">
                <a href="/about" className="text-decoration-none">About Us</a>
              </li>
              <li className="mb-2">
                <a href="/stickers" className="text-decoration-none">Stickers</a>
              </li>
              <li className="mb-2">
                <a href="/api" className="text-decoration-none">API</a>
              </li>
            </ul>
          </div>

          {/* Support */}
          <div className="col-md-3 mb-4">
            <h3 className="h5 mb-3">SUPPORT</h3>
            <ul className="list-unstyled">
              <li className="mb-2">
                <a href="/documentation" className="text-decoration-none">Documentation</a>
              </li>
              <li className="mb-2">
                <a href="/api-status" className="text-decoration-none">API Status</a>
              </li>
              <li className="mb-2">
                <a href="/contact" className="text-decoration-none">Contact</a>
              </li>
              <li className="mb-2">
                <a href="/privacy-policy" className="text-decoration-none">Privacy Policy</a>
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