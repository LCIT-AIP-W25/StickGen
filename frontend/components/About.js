import React from 'react';

const About = () => {
  return (
    <div className="about-page">
      <div className="container">
      {/* About Us Section */}
      <div className="row about-section text-center mt-5">
        <div className="about-text col-lg-6 col-md-12">
        <br/><h2><b>About Us</b></h2><br/>
        <p>We are a team of passionate developers, data scientists, and designers building a cutting-edge Real-Time News Analysis and Social Media Engagement System. Combining AI, backend expertise, and frontend innovation, we leverage tools like Kafka, Elasticsearch, and Redis to detect trends and enhance news interaction. Our AI-driven sticker and emoji generation makes news more engaging, bridging the gap between real-time updates and social media.
        </p>
        </div>
        <div className="about-image col-lg-6 col-md-12">
          <img src="about.jpg" alt="about" />
        </div>
      </div><br/><br/>
      <hr/>
      {/* Our Technology Section */}
      <div className="technology-section mt-5">
        <h3><b>Features</b></h3>
        <p>Our system redefines news and social media engagement by providing real-time trend detection and AI-powered content generation. It enables users to discover viral topics early, create engaging stickers and emojis, and share content effortlessly across platforms.</p>

        <div className="features">
          <div className="feature">
            <span><i className="fa fa-newspaper-o" aria-hidden="true"></i></span>
            <h3>Real-Time News <br/>Scraping</h3>
            <p>System will automatically collect the latest news articles from trusted sources, allowing content creators to spot emerging trends before they go viral.</p>
          </div>
          <div className="feature">
            <span><i className="fa fa-line-chart" aria-hidden="true"></i></span>
            <h3>Smart Search & Trend Detection</h3>
            <p>AI will analyze and categorize news data in real-time, highlighting trending topics and allowing creators to capitalize on them quickly.</p>
          </div>
          <div className="feature">
            <span><i className="fa fa-smile-o" aria-hidden="true"></i></span>
            <h3>AI-Generated Stickers & Emojis</h3>
            <p>AI will generate stickers and emojis related to trending news, giving creators fresh and engaging content to share on social media.</p>
          </div>
          <div className="feature">
            <span><i className="fa fa-share-alt" aria-hidden="true"></i></span>
            <h3>One-Click Social Media Integration</h3>
            <p>With just one click, creators can share AI-generated content directly to their social media accounts, improving consistency and reach.</p>
          </div>
        </div>
      </div>
      <hr/>
      <div className="team-section mt-5 mb-5">
          <h3 className="text-center"><b>Meet Our Team</b></h3>
          <p className="text-center">Passionate experts dedicated to revolutionizing news consumption</p><br/>
          <div className="team-member row">
            <div className="col-md-6">
              <div className="team-card d-flex">
                <div className="team-img" style={{ flex: "0 0 40%" }}>
                  <img src="dharmil.jpg" alt="Dharmilkumar" className="img-fluid" />
                </div>
                <div className="team-detail" style={{ flex: "0 0 60%" }}>
                  <h3>Dharmilkumar</h3>
                  <a href="/">Project Manager</a>
                  <p>Responsible for overseeing the project’s overall development, managing timelines, and ensuring tasks are completed efficiently.</p>
                  <span>
                    <a href="/"><i className="fa fa-twitter"></i></a>
                    <a href="/"><i className="fa fa-linkedin"></i></a>
                  </span>
                </div>
              </div>
            </div>
            <div className="col-md-6">
              <div className="team-card d-flex">
                <div className="team-img" style={{ flex: "0 0 40%" }}>
                  <img src="virpal.jpg" alt="Virpal Kaur" className="img-fluid" />
                </div>
                <div className="team-detail" style={{ flex: "0 0 60%" }}>
                  <h3>Virpal Kaur</h3>
                  <a href="/">Frontend Developer</a>
                  <p>Leading the design and implementation of the user interface using React.js, ensuring that the system is intuitive and responsive.</p>
                  <span>
                    <a href="/"><i className="fa fa-twitter"></i></a>
                    <a href="/"><i className="fa fa-linkedin"></i></a>
                  </span>
                </div>
              </div>
            </div>
            <div className="col-md-6">
              <div className="team-card d-flex">
                <div className="team-img" style={{ flex: "0 0 40%" }}>
                  <img src="kevin.jpg" alt="Kevinsinh" className="img-fluid" />
                </div>
                <div className="team-detail" style={{ flex: "0 0 60%" }}>
                  <h3>Kevinsinh</h3>
                  <a href="/">Backend Developer</a>
                  <p>Responsible for designing and implementing the Kafka-based pipeline, MongoDB integration, and Elasticsearch configuration.</p>
                  <span>
                    <a href="/"><i className="fa fa-twitter"></i></a>
                    <a href="/"><i className="fa fa-linkedin"></i></a>
                  </span>
                </div>
              </div>
            </div>
            <div className="col-md-6">
              <div className="team-card d-flex">
                <div className="team-img" style={{ flex: "0 0 40%" }}>
                  <img src="dharmik.jpg" alt="Dharmikkumar" className="img-fluid" style={{ objectPosition: "top"}}/>
                </div>
                <div className="team-detail" style={{ flex: "0 0 60%" }}>
                  <h3>Dharmik Bhatt</h3>
                  <a href="/">AI/ML Specialist</a>
                  <p>Focused on developing the trend detection models using topic modeling techniques and generating stickers/emojis.</p>
                  <span>
                    <a href="/"><i className="fa fa-twitter"></i></a>
                    <a href="/"><i className="fa fa-linkedin"></i></a>
                  </span>
                </div>
              </div>
            </div>
            <div className="col-md-6">
              <div className="team-card d-flex">
                <div className="team-img" style={{ flex: "0 0 40%" }}>
                  <img src="ayan.jpg" alt="Ayan Mohamed" className="img-fluid" />
                </div>
                <div className="team-detail" style={{ flex: "0 0 60%" }}>
                  <h3>Ayan Khatri</h3>
                  <a href="/">Data Engineer</a>
                  <p>Responsible for designing and implementing the Kafka-based pipeline, MongoDB integration, and Elasticsearch configuration.</p>
                  <span>
                    <a href="/"><i className="fa fa-twitter"></i></a>
                    <a href="/"><i className="fa fa-linkedin"></i></a>
                  </span>
                </div>
              </div>
            </div>
            <div className="col-md-6">
              <div className="team-card d-flex">
                <div className="team-img" style={{ flex: "0 0 40%" }}>
                  <img src="jetinder.jpg" alt="Jitender Kaushik" className="img-fluid" style={{ objectPosition: "top"}}/>
                </div>
                <div className="team-detail" style={{ flex: "0 0 60%" }}>
                  <h3>Jitender Kaushik</h3>
                  <a href="/">Quality Assurance</a>
                  <p>Responsible for deploying the system using Docker, ensuring smooth system performance.</p>
                  <span>
                    <a href="/"><i className="fa fa-twitter"></i></a>
                    <a href="/"><i className="fa fa-linkedin"></i></a>
                  </span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default About;