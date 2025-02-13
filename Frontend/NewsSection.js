import React, { useState, useRef } from 'react';
import { Row, Col, Modal, Pagination } from 'react-bootstrap';
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

  // Pagination Logic
  const allNews = [
    { title: 'Major Tech Company Announces Revolutionary AI Product', content: 'In a groundbreaking announcement today, the tech giant revealed their latest artificial intelligence innovation that promises to transform how we interact with technology...' },
    { title: 'Global Climate Summit Reaches Historic Agreement', content: 'World leaders have come together to sign a landmark climate accord that sets ambitious targets for reducing carbon emissions over the next decade...' },
    { title: 'New Mobile App Disrupts E-commerce Industry', content: 'A new mobile app has emerged as a game-changer in the world of online shopping, offering a seamless experience for users and redefining the e-commerce landscape...' },
    { title: 'SpaceX Launches Historic Mission to Mars', content: 'SpaceX has successfully launched its first crewed mission to Mars, marking a new era in space exploration and paving the way for future human colonization of the Red Planet...' },
    { title: 'Breakthrough in Cancer Treatment Offers New Hope', content: 'Scientists have made a significant breakthrough in cancer treatment, discovering a novel therapy that could drastically improve survival rates for patients with advanced cancer...' },
    { title: 'Global Renewable Energy Adoption Soars', content: 'As countries strive to meet their climate goals, the adoption of renewable energy technologies has reached unprecedented levels, signaling a shift towards a greener, more sustainable future...' },
    { title: '5G Technology Revolutionizes Internet Connectivity', content: 'The rollout of 5G networks has begun, promising faster internet speeds, lower latency, and a wide range of applications that will reshape industries across the globe...' },
    // Add more news items here if needed...
  ];

  const newsPerPage = 5;
  const [currentPage, setCurrentPage] = useState(1);
  const totalPages = Math.ceil(allNews.length / newsPerPage);

  const handlePageChange = (pageNumber) => {
    setCurrentPage(pageNumber);
  };

  const currentNews = allNews.slice((currentPage - 1) * newsPerPage, currentPage * newsPerPage);

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
                <div className="">
                  {currentNews.map((news, index) => (
                    <div className="mt-3 tab-data" key={index}>
                      <a href="/#" className="text-decoration-none">
                        <h6>{news.title}</h6>
                        <p>{news.content}</p>
                        <button 
                          className="btn btn-primary me-2"
                          onClick={handleGenerate}
                        >
                          Generate
                        </button>
                      </a>
                    </div>
                  ))}
                </div>

                {/* Pagination */}
                {totalPages > 1 && (
                  <div className="pagination-container">
                    <Pagination>
                      {[...Array(totalPages)].map((_, index) => (
                        <Pagination.Item
                          key={index + 1}
                          active={index + 1 === currentPage}
                          onClick={() => handlePageChange(index + 1)}
                        >
                          {index + 1}
                        </Pagination.Item>
                      ))}
                    </Pagination>
                  </div>
                )}
              </div>

              {/* Other Tab Panels */}
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
                src="test.png" style={{ width: '300px', height: '300px' }}
                alt="emoji" 
                ref={imageRef} // Attach the ref to the image element
              />
            </div>
          </div>
        </Modal.Body>
        <Modal.Footer>
          <button className="btn btn-download" onClick={handleDownload}>
            <i className="fa fa-download" aria-hidden="true"></i>
          </button>
          <button className="btn btn-share" onClick={handleShare}>
            <i className="fa fa-share" aria-hidden="true"></i>
          </button>
        </Modal.Footer>
      </Modal>

      {/* Share Modal */}
      <Modal show={showShareModal} onHide={closeShareModal}>
        <Modal.Header closeButton>
          <Modal.Title>Share this Emoji</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          <div className="d-flex justify-content-center align-items-center">
            <FacebookShareButton url={dynamicImageUrl}>
              <FacebookIcon size={36} round />
            </FacebookShareButton>
            <WhatsappShareButton url={dynamicImageUrl}>
              <WhatsappIcon size={36} round />
            </WhatsappShareButton>
            <a href="https://www.instagram.com/" target="_blank" rel="noopener noreferrer">
              <FaInstagram size={36} style={{ color: '#E4405F', marginLeft: '15px' }} />
            </a>
          </div>
        </Modal.Body>
      </Modal>
    </div>
  );
};

export default NewsSection;
