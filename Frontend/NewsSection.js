import React, { useState, useRef, useEffect } from "react";
import { Row, Col, Modal, Pagination } from "react-bootstrap";
import TrendingTopics from "./TrendingTopics";
import SearchBar from "./SearchBar";
import Papa from "papaparse";
import { FacebookShareButton, FacebookIcon } from "react-share";
import { FaInstagram } from "react-icons/fa";
import { WhatsappShareButton, WhatsappIcon } from "react-share";

const NewsSection = () => {
  const imageRef = useRef(null);
  const stickerRef = useRef(null);
  const [showModal, setShowModal] = useState(false);
  const [showStickerModal, setShowStickerModal] = useState(false); // New state for Sticker Modal
  const [showShareModal, setShowShareModal] = useState(false);
  const [news, setNews] = useState([]);
  const [filteredNews, setFilteredNews] = useState([]);
  const [searchQuery, setSearchQuery] = useState("");
  const [currentPage, setCurrentPage] = useState(1);
  const newsPerPage = 10;
  const dynamicImageUrl = imageRef.current ? imageRef.current.src : "";
  const dynamicStickerUrl = stickerRef.current ? stickerRef.current.src : ""; // For sticker image URL

  useEffect(() => {
    fetch("/news_data.csv")
      .then((response) => response.text())
      .then((csvText) => {
        Papa.parse(csvText, {
          header: true,
          skipEmptyLines: true,
          complete: (result) => {
            const filteredData = result.data.map(({ headline, link, short_description, date }) => ({
              headline,
              link,
              short_description,
              date,
            }));
            setNews(filteredData);
            setFilteredNews(filteredData);
          },
        });
      })
      .catch((error) => console.error("Error loading CSV:", error));
  }, []);

  const handleSearch = (query) => {
    setSearchQuery(query);
    const filtered = news.filter((item) =>
      item.headline.toLowerCase().includes(query.toLowerCase())
    );
    setFilteredNews(filtered);
  };

  const handleGenerateEmoji = () => {
    setShowModal(true);
  };

  const handleGenerateSticker = () => {
    setShowStickerModal(true); // Show sticker modal
  };

  const handleCloseModal = () => {
    setShowModal(false);
  };

  const handleCloseStickerModal = () => {
    setShowStickerModal(false); // Close sticker modal
  };

  const handleDownload = () => {
    if (imageRef.current) {
      const imageUrl = imageRef.current.src;
      const link = document.createElement("a");
      link.href = imageUrl;
      link.download = "emoji.png";
      link.click();
    }
  };

  const handleDownloadSticker = () => {
    if (stickerRef.current) {
      const stickerUrl = stickerRef.current.src;
      const link = document.createElement("a");
      link.href = stickerUrl;
      link.download = "sticker.png";
      link.click();
    }
  };

  const handleShare = () => {
    setShowModal(false);
    setShowStickerModal(false);
    setShowShareModal(true);
  };

  const closeShareModal = () => {
    setShowShareModal(false);
  };
  

  // Pagination Logic
  const totalPages = Math.ceil(filteredNews.length / newsPerPage);
  const pagesToShow = 5;
  const startPage = Math.max(1, currentPage - Math.floor(pagesToShow / 2));
  const endPage = Math.min(totalPages, startPage + pagesToShow - 1);
  const currentNews = filteredNews.slice((currentPage - 1) * newsPerPage, currentPage * newsPerPage);


  const handlePageChange = (pageNumber) => {
    setCurrentPage(pageNumber);
  };

  const handlePrevious = () => {
    setCurrentPage(Math.max(1, currentPage - pagesToShow));
  };

  const handleNext = () => {
    setCurrentPage(Math.min(totalPages, currentPage + pagesToShow));
  };

  const truncateDescription = (description) => {
    const words = description.split(" ");
    if (words.length > 50) {
      return words.slice(0, 50).join(" ") + " ...";
    }
    return description;
  };

  return (
    <div className="container news-section p-4">
      <Row>
        <SearchBar onSearch={handleSearch} value={searchQuery} />
        <Col lg={8} sm={12}>
          <div className="container mt-5">
            <ul className="nav nav-tabs" id="myTab" role="tablist">
              <li className="nav-item" role="presentation">
                <button className="nav-link active" id="all-news-tab" data-bs-toggle="tab" data-bs-target="#all-news" type="button" role="tab" aria-controls="all-news" aria-selected="true">
                  All News
                </button>
              </li>
              <li className="nav-item" role="presentation">
                <button className="nav-link" id="politics-tab" data-bs-toggle="tab" data-bs-target="#politics" type="button" role="tab" aria-controls="politics" aria-selected="false">
                  Politics
                </button>
              </li>
              <li className="nav-item" role="presentation">
                <button className="nav-link" id="entertainment-tab" data-bs-toggle="tab" data-bs-target="#entertainment" type="button" role="tab" aria-controls="entertainment" aria-selected="false">
                  Entertainment
                </button>
              </li>
              <li className="nav-item" role="presentation">
                <button className="nav-link" id="technology-tab" data-bs-toggle="tab" data-bs-target="#technology" type="button" role="tab" aria-controls="technology" aria-selected="false">
                  Technology
                </button>
              </li>
              <li className="nav-item" role="presentation">
                <button className="nav-link" id="sports-tab" data-bs-toggle="tab" data-bs-target="#sports" type="button" role="tab" aria-controls="sports" aria-selected="false">
                  Sports
                </button>
              </li>
              <li className="nav-item" role="presentation">
                <button className="nav-link" id="business-tab" data-bs-toggle="tab" data-bs-target="#business" type="button" role="tab" aria-controls="business" aria-selected="false">
                  Business
                </button>
              </li>
            </ul>

            <div className="tab-content" id="myTabContent">
              {/* All News Tab Content */}
              <div className="tab-pane fade show active" id="all-news" role="tabpanel" aria-labelledby="all-news-tab">
                {currentNews.length > 0 ? (
                  currentNews.map((item, index) => (
                    <div className="mt-3 tab-data" key={index}>
                      <a href={item.link} className="text-decoration-none" target="_blank" rel="noopener noreferrer">
                        <h6>{item.headline}</h6>
                        <p>{truncateDescription(item.short_description)}</p>
                      </a>
                      <button className="btn btn-primary me-2" onClick={handleGenerateEmoji}>Generate Emoji</button>
                      <button className="btn btn-secondary" onClick={handleGenerateSticker}>Generate Sticker</button>
                    </div>
                  ))
                ) : (
                  <p>No results found.</p>
                )}

                {/* Pagination */}
                {totalPages > 1 && (
                  <div className="pagination-container">
                    <Pagination>
                      <Pagination.Prev onClick={handlePrevious} disabled={currentPage === 1} />
                      {[...Array(endPage - startPage + 1)].map((_, index) => {
                        const pageNumber = startPage + index;
                        return (
                          <Pagination.Item
                            key={pageNumber}
                            active={pageNumber === currentPage}
                            onClick={() => handlePageChange(pageNumber)}
                          >
                            {pageNumber}
                          </Pagination.Item>
                        );
                      })}
                      <Pagination.Next onClick={handleNext} disabled={currentPage === totalPages} />
                    </Pagination>
                  </div>
                )}
              </div>

              {/* Other Tab Panels */}
              <div className="tab-pane fade" id="politics" role="tabpanel" aria-labelledby="politics-tab">
                <p className="mt-3">Politics news content goes here.</p>
              </div>
              <div className="tab-pane fade" id="entertainment" role="tabpanel" aria-labelledby="entertainment-tab">
                <p className="mt-3">Entertainment news content goes here.</p>
              </div>
              <div className="tab-pane fade" id="technology" role="tabpanel" aria-labelledby="technology-tab">
                <p className="mt-3">Technology news content goes here.</p>
              </div>
              <div className="tab-pane fade" id="sports" role="tabpanel" aria-labelledby="sports-tab">
                <p className="mt-3">Sports news content goes here.</p>
              </div>
              <div className="tab-pane fade" id="business" role="tabpanel" aria-labelledby="business-tab">
                <p className="mt-3">Business news content goes here.</p>
              </div>
            </div>
          </div>
        </Col>
        <Col lg={4} sm={12}>
          <TrendingTopics />
        </Col>
      </Row>

      {/* Emoji Generation Modal */}
      <Modal show={showModal} onHide={handleCloseModal}>
        <Modal.Header closeButton>
          <Modal.Title>Emoji</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          <div className="text-center">
            <div className="emoji-container my-4">
              <img
                src="emoji.jpg" style={{ width: '300px', height: '300px' }}
                alt="emoji"
                ref={imageRef}
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

      {/* Sticker Generation Modal */}
      <Modal show={showStickerModal} onHide={handleCloseStickerModal}>
        <Modal.Header closeButton>
          <Modal.Title>Sticker</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          <div className="text-center">
            <div className="sticker-container my-4">
              <img
                src="sticker.png" style={{ width: '300px', height: '300px' }}
                alt="sticker"
                ref={stickerRef}
              />
            </div>
          </div>
        </Modal.Body>
        <Modal.Footer>
          <button className="btn btn-download" onClick={handleDownloadSticker}>
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
          <Modal.Title>Share this Emoji/Sticker</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          <div className="d-flex justify-content-center align-items-center" style={{ padding: '2rem 0rem' }}>
            <FacebookShareButton url={dynamicImageUrl || dynamicStickerUrl}>
              <FacebookIcon size={36} round />
            </FacebookShareButton>
            <div style={{ marginRight: '15px' }} />
            <WhatsappShareButton url={dynamicImageUrl || dynamicStickerUrl}>
              <WhatsappIcon size={36} round />
            </WhatsappShareButton>
            <a
              href={`https://twitter.com/intent/tweet?text=Check%20out%20this%20emoji&url=${encodeURIComponent(dynamicImageUrl || dynamicStickerUrl)}`}
              target="_blank" title="Twitter"
              rel="noopener noreferrer"
            >
              <img
                src="twitter-x.png" // Twitter X Logo URL (SVG)
                alt="Twitter X"
                style={{ width: '32px', height: '32px', marginLeft: '15px', borderRadius: '20px'}}
              />
            </a>
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