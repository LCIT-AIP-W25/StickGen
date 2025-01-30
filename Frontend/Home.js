import React from 'react';
import { useNavigate } from 'react-router-dom';

const style = {
    background: `url(${process.env.PUBLIC_URL + '/videoo.gif'})`,
  };

const Home = () => {
  const navigate = useNavigate(); // Hook for navigation

  const goToStickers = () => {
    navigate('/stickers'); // Navigate to the explanation page
  };

  return (
    <div className="main-page" style={style}>
      <div className="main-content">
        <h1>eeeeee</h1>
        <h2>wwww</h2><br/>
        <button onClick={goToStickers}>Stickers</button>
      </div>
    </div>
  );
};

export default Home;


