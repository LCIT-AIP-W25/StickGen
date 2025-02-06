import React from 'react';

const TrendingTopics = () => {
  return (
    <div className="trending-topics">
      <h6><i class="fa fa-line-chart" aria-hidden="true"></i> Trending Topics</h6>
      <div className="topic">
        <span className="hashtag">#Technnovation</span>
        <span className="mentions">50K mentions</span>
      </div>
      <div className="topic">
        <span className="hashtag">#ClimateAction</span>
        <span className="mentions">45K mentions</span>
      </div>
      <div className="topic">
        <span className="hashtag">#GlobalSummit</span>
        <span className="mentions">38K mentions</span>
      </div>
      <div className="topic">
        <span className="hashtag">#FutureOfAI</span>
        <span className="mentions">32K mentions</span>
      </div>
    </div>
  );
};

export default TrendingTopics;