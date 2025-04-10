import React from "react";
import { FaSearch } from 'react-icons/fa'

const SearchBar = ({ onSearch, value }) => {
  const handleChange = (e) => {
    onSearch(e.target.value); // Pass the search query to the parent component
  };

  return (
    <div className="search-bar-container">
      <form className="search-bar-input-group">
        <input
          type="text"
          className="search-bar-input"
          placeholder="Search news..."
          value={value}
          onChange={handleChange}
        />
        <button type="submit" className="search-bar-button">
            <FaSearch className="search-bar-icon" /> {/* Search icon */}
        </button>
      </form>
    </div>
  );
};

export default SearchBar;
