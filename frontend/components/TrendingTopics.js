import React, { useEffect, useState } from 'react';

const TrendingTopics = () => {
  const [topics, setTopics] = useState([]);

  useEffect(() => {
    fetch('/trending.json')
      .then((res) => res.json())
      .then((data) => {
        console.log('✅ Trending Data:', data);
        setTopics(data);
      })
      .catch((err) => {
        console.error('❌ Error fetching trending topics:', err);
      });
  }, []);

  return (
    <div className="trending-topics">
      <h6><i className="fa fa-line-chart" aria-hidden="true"></i> Trending Topics</h6>
      {topics.length === 0 ? (
        <p>No trending topics found.</p>
      ) : (
        topics.map((topic, index) => (
          <div key={index} className="topic">
            <span className="hashtag">{topic.hashtag}</span>
            <span className="mentions">{(topic.mentions / 1000).toFixed(0)}K mentions</span>
          </div>
        ))
      )}
    </div>
  );
};

export default TrendingTopics;
