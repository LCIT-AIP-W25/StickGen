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
  const [isEmojiReady, setIsEmojiReady] = useState(false);
  const [filteredNews, setFilteredNews] = useState([]);
  const [searchQuery, setSearchQuery] = useState("");
  const [currentPage, setCurrentPage] = useState(1);
  const newsPerPage = 10;
  const [activeCategory, setActiveCategory] = useState("All");
  const dynamicImageUrl = imageRef.current ? imageRef.current.src : "";
  const dynamicStickerUrl = stickerRef.current ? stickerRef.current.src : ""; // For sticker image URL
  const [selectedCategory, setSelectedCategory] = useState("All");
  const handleCategoryChange = (category) => {
    setActiveCategory(category);
    setCurrentPage(1); // Reset pagination
  };
  


  useEffect(() => {
    const fetchNews = () => {
      fetch("http://localhost:5000/api/news?query=")
        .then((res) => res.json())
        .then((data) => {
          const safeData = Array.isArray(data) ? data : []; // ✅ Defensive check
          console.log("Fetched news:", safeData);
          setNews(safeData);
          setFilteredNews(safeData);
        })
        .catch((err) => console.error("Error loading news from API", err));
    };
  
    fetchNews(); // Initial fetch
  
    const interval = setInterval(fetchNews, 60000); // Auto-refresh every 60 sec
  
    return () => clearInterval(interval); // Clear on component unmount
  }, []);
  
  
  
  const handleSearch = (query) => {
    setSearchQuery(query);
  
    fetch(`http://localhost:5000/api/news?query=${query}`)
      .then((res) => res.json())
      .then((data) => {
        setFilteredNews(data);
      })
      .catch((err) => console.error("Error during search", err));
  };
  
  
  const handleGenerateEmoji = async (summary) => {
    try {
      setIsEmojiReady(false);
      setShowModal(true);
      if (imageRef.current) {
        imageRef.current.alt = "Generated emoji...";
      }
  
      // Truncate text to 77 tokens
      const truncatedText = summary.split(' ').slice(0, 77).join(' ');
  
      const response = await fetch('http://localhost:5001/generate_emoji', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          text: truncatedText
        })
      });
  
      const data = await response.json();
  
      if (response.ok) {
        console.log(`Generated emoji URL: ${data.url}`);
  
        // ✅ Add a unique timestamp to prevent caching
        const newImageUrl = `${data.url}?timestamp=${new Date().getTime()}`;
  
        setTimeout(() => {
          if (imageRef.current) {
            imageRef.current.src = newImageUrl;
            imageRef.current.alt = "Generating Emoji ";
            setIsEmojiReady(true);
          }
        }, 1500); // 1.5 seconds delay
      } else {
        console.error('Failed to generate emoji:', data.error);
      }
    } catch (error) {
      console.error('Error:', error);
    }
  };
  
  const handleGenerateSticker = async (summary) => {
    try {
      setShowStickerModal(true);
      if (stickerRef.current) {
        stickerRef.current.alt = "Generating sticker...";
      }
  
      const truncatedText = summary.split(" ").slice(0, 77).join(" ");
  
      const response = await fetch("http://localhost:5001/generate_sticker", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ text: truncatedText }),
      });
  
      const data = await response.json();
  
      if (response.ok) {
        const newStickerUrl = `${data.url}?timestamp=${new Date().getTime()}`;
        setTimeout(() => {
          if (stickerRef.current) {
            stickerRef.current.src = newStickerUrl;
            stickerRef.current.alt = "Generated Sticker";
          }
        }, 1500);
      } else {
        console.error("Failed to generate sticker:", data.error);
      }
    } catch (error) {
      console.error("Error:", error);
    }
  };
  
  const handleCloseModal = () => {
    setShowModal(false);
  };

  const handleCloseStickerModal = () => {
    setShowStickerModal(false); // Close sticker modal
  };
  const handleDownload = () => {
    if (imageRef.current && imageRef.current.src) {
      fetch(imageRef.current.src)
        .then(response => response.blob())
        .then(blob => {
          const url = window.URL.createObjectURL(blob);
          const link = document.createElement("a");
          link.href = url;
          link.download = "emoji.png"; // Set a name for the downloaded file
          document.body.appendChild(link);
          link.click();
          document.body.removeChild(link);
          window.URL.revokeObjectURL(url); // Clean up memory
        })
        .catch(error => console.error("Error downloading image:", error));
    }
  };
  
  const handleDownloadSticker = () => {
    if (stickerRef.current && stickerRef.current.src) {
      fetch(stickerRef.current.src)
        .then(response => response.blob())
        .then(blob => {
          const url = window.URL.createObjectURL(blob);
          const link = document.createElement("a");
          link.href = url;
          link.download = "sticker.png"; // Set a name for the downloaded file
          document.body.appendChild(link);
          link.click();
          document.body.removeChild(link);
          window.URL.revokeObjectURL(url); // Clean up memory
        })
        .catch(error => console.error("Error downloading sticker:", error));
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
  // const currentNews = filteredNews.slice((currentPage - 1) * newsPerPage, currentPage * newsPerPage);


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
  
  const handleCategoryFilter = (category) => {
    setSelectedCategory(category);
    setCurrentPage(1);
  
    if (category === "All") {
      setFilteredNews(news);
    } else {
      const filtered = news.filter(item => 
        item.predicted_category &&
        item.predicted_category.toLowerCase() === category.toLowerCase()
      );
      setFilteredNews(filtered);
    }
  };
  
  let categoryFilteredNews = [];

  if (Array.isArray(filteredNews)) {
    if (selectedCategory === "All") {
      categoryFilteredNews = filteredNews;
    } else {
      categoryFilteredNews = filteredNews.filter(
        (item) =>
          item.predicted_category &&
          item.predicted_category.toLowerCase() === selectedCategory.toLowerCase()
      );
    }
  }
  
  const currentNews = Array.isArray(categoryFilteredNews)
  ? categoryFilteredNews.slice(
      (currentPage - 1) * newsPerPage,
      currentPage * newsPerPage
    )
  : [];




  return (
    <div className="container news-section p-4">
      <Row>
        <SearchBar onSearch={handleSearch} value={searchQuery} />
        <Col lg={8} sm={12}>
          <div className="container mt-5 tab-container">
            <ul className="nav nav-tabs" id="myTab" role="tablist">
              <li className="nav-item" role="presentation">
                <button  className={`nav-link ${selectedCategory === "All" ? "active" : ""}`}
                                  onClick={() => handleCategoryFilter("All")}>
                  All News
                </button>
              </li>
              <li className="nav-item" role="presentation">
                <button className={`nav-link ${selectedCategory === "Politics" ? "active" : ""}`}
                                  onClick={() => handleCategoryFilter("Politics")}>
                  Politics
                </button>
              </li>
              <li className="nav-item" role="presentation">
                <button className={`nav-link ${selectedCategory === "Sports" ? "active" : ""}`}
                             onClick={() => handleCategoryFilter("Sports")}>
                  Sports
                </button>
              </li>
              <li className="nav-item" role="presentation">
                <button className={`nav-link ${selectedCategory === "Technology" ? "active" : ""}`}
                               onClick={() => handleCategoryFilter("Technology")}>
                  Technology
                </button>
              </li>
              <li className="nav-item" role="presentation">
                <button className={`nav-link ${selectedCategory === "Education" ? "active" : ""}`}
                             onClick={() => handleCategoryFilter("Education")}>
                  Education
                </button>
              </li>
              <li className="nav-item" role="presentation">
                <button className={`nav-link ${selectedCategory === "Entertainment" ? "active" : ""}`}
                        onClick={() => handleCategoryFilter("Entertainment")}>
                  Entertainment
                </button>
              </li>
              <li className="nav-item" role="presentation">
                <button className={`nav-link ${selectedCategory === "Science" ? "active" : ""}`}
                             onClick={() => handleCategoryFilter("Science")}>
                  Science
                </button>
              </li>
              <li className="nav-item" role="presentation">
                <button className={`nav-link ${selectedCategory === "Business" ? "active" : ""}`}
                             onClick={() => handleCategoryFilter("Business")}>
                  Business
                </button>
              </li>
              <li className="nav-item" role="presentation">
                <button className={`nav-link ${selectedCategory === "Crime" ? "active" : ""}`}
                             onClick={() => handleCategoryFilter("Crime")}>
                  Crime
                </button>
              </li>
              <li className="nav-item" role="presentation">
                <button className={`nav-link ${selectedCategory === "Health" ? "active" : ""}`}
                             onClick={() => handleCategoryFilter("Health")}>
                  Health
                </button>
              </li>
            </ul>

            <div className="tab-content" id="myTabContent">
              {/* All News Tab Content */}
              <div className="tab-pane fade show active" id="all-news" role="tabpanel" aria-labelledby="all-news-tab">
                {currentNews.length > 0 ? (
                  currentNews.map((item, index) => {
                    console.log("News data:", item); // ✅ Add this to check the data

                    return (
                      <div className="mt-3 tab-data" key={index}>
                        <a href={item.link} className="text-decoration-none" target="_blank" rel="noopener noreferrer">
                          <h6>{item.headline}</h6>
                          <p>{truncateDescription(item.summary)}</p>
                        </a>
                        <button className="btn btn-primary me-2" onClick={() => handleGenerateEmoji(item.summary)}>Generate Emoji</button>
                        <button className="btn btn-secondary" onClick={() => handleGenerateSticker(item.summary)}>Generate Sticker</button>
                      </div>
                    );
                  })
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
              <div className="tab-pane fade" id="sports" role="tabpanel" aria-labelledby="sports-tab">
                <p className="mt-3">Sports news content goes here.</p>
              </div>
              <div className="tab-pane fade" id="technology" role="tabpanel" aria-labelledby="technology-tab">
                <p className="mt-3">Technology news content goes here.</p>
              </div>
              <div className="tab-pane fade" id="crime" role="tabpanel" aria-labelledby="crime-tab">
                <p className="mt-3">Education news content goes here.</p>
              </div>
              <div className="tab-pane fade" id="entertainment" role="tabpanel" aria-labelledby="entertainment-tab">
                <p className="mt-3">Entertainment news content goes here.</p>
              </div>
              <div className="tab-pane fade" id="science" role="tabpanel" aria-labelledby="science-tab">
                <p className="mt-3">Science news content goes here.</p>
              </div>
              <div className="tab-pane fade" id="business" role="tabpanel" aria-labelledby="business-tab">
                <p className="mt-3">Business news content goes here.</p>
              </div>
              <div className="tab-pane fade" id="crime" role="tabpanel" aria-labelledby="crime-tab">
                <p className="mt-3">Crime news content goes here.</p>
              </div>
              <div className="tab-pane fade" id="health" role="tabpanel" aria-labelledby="health-tab">
                <p className="mt-3">Health news content goes here.</p>
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
            src="C:/Users/patel/Desktop/final_project/project_test/backend/static/generated.png"
            // src={imageRef.current ? imageRef.current.src : ""}
            style={{ width: '300px', height: '300px' }}
            alt="Generating emoji"
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
                src="C:/Users/patel/Desktop/final_project/project_test/backend/static/generated_sticker.png" style={{ width: '300px', height: '300px' }}
                alt="Generating sticker"
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