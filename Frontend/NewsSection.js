import React, { useState, useRef } from 'react';
import { Row, Col, Modal } from 'react-bootstrap';
import TrendingTopics from './TrendingTopics';
import SearchBar from './SearchBar';
import { FacebookShareButton, FacebookIcon, WhatsappShareButton, WhatsappIcon} from 'react-share';
import { FaInstagram } from 'react-icons/fa';



const NewsSection = () => {
  // const [emojiUrl, setEmojiUrl] = useState('');
  const imageRef = useRef(null);
  const [showModal, setShowModal] = useState(false);
  const [showShareModal, setShowShareModal] = useState(false); 
  const dynamicImageUrl = imageRef.current ? imageRef.current.src : '';

  const handleSearch = (query) => {
    console.log('Search query:', query);
  };

  const handleGenerate = () => {
    setShowModal(true);
  };

  const handleCloseModal = () => {
    setShowModal(false);
  };

  const handleDownload = () => {
    if (imageRef.current) {
      const imageUrl = imageRef.current.src; // Get the image URL
      const link = document.createElement('a'); // Create an anchor element
      link.href = imageUrl; // Set the image URL as the href
      link.download = 'emoji.png'; // Set the download file name
      link.click(); // Trigger the download
    }
  };

  const handleShare = () => {
    setShowModal(false);
    setShowShareModal(true);
  };

  const closeShareModal = () => {
    setShowShareModal(false);
  };

  return (
    <div className="container news-section p-4">
      <Row>
        <SearchBar onSearch={handleSearch} />
        <Col lg={8} sm={12}>
          <div className="container mt-5">
            <ul className="nav nav-tabs" id="myTab" role="tablist">
              {/* Existing Tab Items */}
              <li className="nav-item" role="presentation">
                <button
                  className="nav-link active"
                  id="all-news-tab"
                  data-bs-toggle="tab"
                  data-bs-target="#all-news"
                  type="button"
                  role="tab"
                  aria-controls="all-news"
                  aria-selected="true"
                >
                  All News
                </button>
              </li>
              <li className="nav-item" role="presentation">
                <button
                  className="nav-link"
                  id="politics-tab"
                  data-bs-toggle="tab"
                  data-bs-target="#politics"
                  type="button"
                  role="tab"
                  aria-controls="politics"
                  aria-selected="false"
                >
                  Politics
                </button>
              </li>
              <li className="nav-item" role="presentation">
                <button
                  className="nav-link"
                  id="entertainment-tab"
                  data-bs-toggle="tab"
                  data-bs-target="#entertainment"
                  type="button"
                  role="tab"
                  aria-controls="entertainment"
                  aria-selected="false"
                >
                  Entertainment
                </button>
              </li>
              <li className="nav-item" role="presentation">
                <button
                  className="nav-link"
                  id="technology-tab"
                  data-bs-toggle="tab"
                  data-bs-target="#technology"
                  type="button"
                  role="tab"
                  aria-controls="technology"
                  aria-selected="false"
                >
                  Technology
                </button>
              </li>
              <li className="nav-item" role="presentation">
                <button
                  className="nav-link"
                  id="sports-tab"
                  data-bs-toggle="tab"
                  data-bs-target="#sports"
                  type="button"
                  role="tab"
                  aria-controls="sports"
                  aria-selected="false"
                >
                  Sports
                </button>
              </li>
              <li className="nav-item" role="presentation">
                <button
                  className="nav-link"
                  id="business-tab"
                  data-bs-toggle="tab"
                  data-bs-target="#business"
                  type="button"
                  role="tab"
                  aria-controls="business"
                  aria-selected="false"
                >
                  Business
                </button>
              </li>
            </ul>

            <div className="tab-content" id="myTabContent">
              {/* All News Tab Content */}
              <div
                className="tab-pane fade show active"
                id="all-news"
                role="tabpanel"
                aria-labelledby="all-news-tab"
              >
                <div className="mt-3 tab-data">
                  <h6>Major Tech Company Announces Revolutionary AI Product</h6>
                  <p>
                    In a groundbreaking announcement today, the tech giant revealed their latest artificial intelligence
                    innovation that promises to transform how we interact with technology...
                  </p>
                  <button 
                    className="btn btn-primary me-2"
                    onClick={handleGenerate}
                  >
                    Generate
                  </button>
                </div>
                <div className="mt-3 tab-data">
                  <h6>Global Climate Summit Reaches Historic Agreement</h6>
                  <p>
                    World leaders have come together to sign a landmark climate accord that sets ambitious targets for
                    reducing carbon emissions over the next decade...
                  </p>
                  <button 
                    className="btn btn-primary me-2"
                    onClick={handleGenerate}
                  >
                    Generate
                  </button>
                </div>
              </div>

              {/* Other Tab Panels (unchanged) */}
              <div
                className="tab-pane fade"
                id="politics"
                role="tabpanel"
                aria-labelledby="politics-tab"
              >
                <p className="mt-3 ">Politics news content goes here.</p>
              </div>
              <div
                className="tab-pane fade"
                id="entertainment"
                role="tabpanel"
                aria-labelledby="entertainment-tab"
              >
                <p className="mt-3">Entertainment news content goes here.</p>
              </div>
              <div
                className="tab-pane fade"
                id="technology"
                role="tabpanel"
                aria-labelledby="technology-tab"
              >
                <p className="mt-3">Technology news content goes here.</p>
              </div>
              <div
                className="tab-pane fade"
                id="sports"
                role="tabpanel"
                aria-labelledby="sports-tab"
              >
                <p className="mt-3">Sports news content goes here.</p>
              </div>
              <div
                className="tab-pane fade"
                id="business"
                role="tabpanel"
                aria-labelledby="business-tab"
              >
                <p className="mt-3">Business news content goes here.</p>
              </div>
            </div>
          </div>
        </Col>
        <Col lg={4} sm={12}>
          <TrendingTopics />
        </Col>
      </Row>

      {/* Generation Modal */}
      <Modal show={showModal} onHide={handleCloseModal}>
        <Modal.Header closeButton>
          <Modal.Title>Emoji</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          <div className="text-center">
            <div className="emoji-container my-4">
              <img 
                src="test.png" style={{ width: '400px', height: '200px' }}
                alt="emoji" 
                ref={imageRef} // Attach the ref to the image element
              />
               {/* <img src={emojiUrl} alt="emoji" ref={imageRef} />  */}
            </div>
          </div>
        </Modal.Body>
        <Modal.Footer>
          <button className="btn btn-download" onClick={handleDownload}>
            <i className="fa fa-download" aria-hidden="true"></i>
          </button>
          <button className="btn btn-share" onClick={handleShare}>
            <i className="fa fa-share-alt" aria-hidden="true"></i>
          </button>
        </Modal.Footer>
      </Modal>

      <Modal show={showShareModal} onHide={closeShareModal}>
        <Modal.Header closeButton>
          <Modal.Title>Share This Emoji</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          <br/>
          <div className="d-flex justify-content-center">
            {/* Social Media Share Buttons */}
            <div title="Facebook" style={{ display: 'inline-block' }}>
              <FacebookShareButton url={imageRef.current ? imageRef.current.src : ''}>
                <FacebookIcon size={32} round={true} />
              </FacebookShareButton>
            </div>
            <div style={{ marginLeft: '15px', marginRight: '15px' }} />
            <a
              href={`https://twitter.com/intent/tweet?text=Check%20out%20this%20emoji&url=${encodeURIComponent(dynamicImageUrl)}`}
              target="_blank" title="Twitter"
              rel="noopener noreferrer"
            >
              <img
                src="twitter-x.png" // Twitter X Logo URL (SVG)
                alt="Twitter X"
                style={{ width: '32px', height: '32px', borderRadius: '20px'}} // Customize the size
              />
            </a>
            <div style={{ marginLeft: '15px', marginRight: '15px' }} />
            <div title="Whatsapp" style={{ display: 'inline-block' }}>
              <WhatsappShareButton url={imageRef.current ? imageRef.current.src : ''}>
                <WhatsappIcon size={32} round={true} />
              </WhatsappShareButton>
            </div>
            <div style={{ marginLeft: '15px', marginRight: '15px' }} />
            <a
              href={`https://www.instagram.com/?url=${encodeURIComponent(imageRef.current ? imageRef.current.src : '')}`}
              target="_blank"
              rel="noopener noreferrer" title="Instagram"
            >
              <FaInstagram size={32} color="#E4405F" />
            </a>
          </div>
          <br/>
        </Modal.Body>
        <Modal.Footer>
          <button className="btn btn-secondary" onClick={closeShareModal}>Close</button>
        </Modal.Footer>
      </Modal>

    </div>
  );
};

export default NewsSection;