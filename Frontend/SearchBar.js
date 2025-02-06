import React, { useState } from 'react';
import { FaSearch } from 'react-icons/fa'; 

const SearchBar = ({ onSearch }) => {
  const [query, setQuery] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    onSearch(query); // Call the onSearch function passed from the parent
  };

  return (
    <div className="search-bar-container">
      <form onSubmit={handleSubmit} className="search-bar-input-group">
        <input
          type="text"
          placeholder="Search for news, topics, or trends..."
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          className="search-bar-input"
        />
        <button type="submit" className="search-bar-button">
          <FaSearch className="search-bar-icon" /> {/* Search icon */}
        </button>
      </form>
    </div>
  );
};

export default SearchBar;