import React from 'react';

const About = () => {
  return (
    <div className="about-page">
      <div className="container">
      {/* About Us Section */}
      <div className="row about-section text-center mt-5">
        <div className="about-text col-md-6">
        <br/><h2><b>About Us</b></h2><br/>
        <p>Our team consists of passionate developers, data scientists, and designers working together to build the 
          Real-Time News Analysis and Social Media Engagement System. With a combination of skills in backend development, 
          AI/ML modeling, data processing, and frontend design, we aim to create a unique solution that connects real-time 
          news with social media engagement. We use advanced tools like Kafka, Elasticsearch, and Redis to ensure efficient
           data handling and trend detection. By integrating AI-driven sticker and emoji generation, our platform enhances 
           user interaction with news and trends. Together, we’re focused on delivering an innovative, engaging experience for 
           users worldwide.
        </p>
        </div>
        <div className="about-image col-md-6">
          <img src="about.jpg" alt="about" />
        </div>
      </div><br/><br/>
      <hr/>
      {/* Our Technology Section */}
      <div className="technology-section mt-5">
        <h3><b>Our Technology</b></h3>
        <p>Cutting-edge solutions powered by artificial intelligence</p>

        <div className="features">
          <div className="feature">
            <span><i className="fa">AI</i></span>
            <h3>AI-Powered Analysis</h3>
            <p>Advanced machine learning algorithms for real-time news analysis and trend detection.</p>
          </div>
          <div className="feature">
            <span><i className="fa fa-rocket" aria-hidden="true"></i></span>
            <h3>Instant Generation</h3>
            <p>Generate engaging stickers and social media content in seconds.</p>
          </div>
          <div className="feature">
            <span><i className="fa fa-code" aria-hidden="true"></i></span>
            <h3>Robust Architecture</h3>
            <p>Built with scalable, modern technologies for reliable performance.</p>
          </div>
          <div className="feature">
            <span><i className="fa fa-bolt" aria-hidden="true"></i></span>
            <h3>Real-time Updates</h3>
            <p>Stay current with instant news updates and trend analysis.</p>
          </div>
        </div>
      </div>
      <hr/>
      <div className="team-section mt-5 mb-5">
        <h3 className="text-center"><b>Meet Our Team</b></h3>
        <p className="text-center ">Passionate experts dedicated to revolutionizing news consumption</p>
        <div className="features">
          <div className="feature">
            <h3>Dharmilkumar</h3>
            <a href="/">Project Manager</a>
            <p>Responsible for overseeing the project’s overall development, managing timelines, and ensuring 
              tasks are completed efficiently. Also lead the backend architecture design, coordinate team collaboration, 
              and ensure the quality of work across all areas and includes risk management and presenting the 
              final outcomes to stakeholders.</p>
            <span>
              <a href="/"><i className="fa fa-twitter"></i></a>
              <a href="/"><i className="fa fa-linkedin"></i></a>
            </span>
          </div>
          <div className="feature">
            <h3>Virpal Kaur</h3>
            <a href="/">Frontend Developer</a>
            <p>Leading the design and implementation of the user interface using React.js, ensuring that the system is intuitive and responsive for users to search, filter, and share content.</p>
            <span>
              <a href="/"><i className="fa fa-twitter"></i></a>
              <a href="/"><i className="fa fa-linkedin"></i></a>
            </span>
          </div>
          <div className="feature">
            <h3>Kevinsinh</h3>
            <a href="/">Backend Developer</a>
            <p>Responsible for designing and implementing the Kafka-based pipeline, MongoDB integration, 
              and Elasticsearch configuration for efficient data handling and retrieval.</p>
            <span>
              <a href="/"><i className="fa fa-twitter"></i></a>
              <a href="/"><i className="fa fa-linkedin"></i></a>
            </span>
          </div>
          <div className="feature">
            <h3>Dharmikkumar</h3>
            <a href="/">AI/ML Specialist</a>
            <p>Focused on developing the trend detection models using topic modeling techniques 
              and generating stickers/emojis based on detected trends and sentiments.</p>
            <span>
              <a href="/"><i className="fa fa-twitter"></i></a>
              <a href="/"><i className="fa fa-linkedin"></i></a>
            </span>
          </div>
          <div className="feature">
            <h3>Ayan Mohamed</h3>
            <a href="/">Data Engineer</a>
            <p>Responsible for designing and implementing the Kafka-based pipeline, MongoDB integration, 
            and Elasticsearch configuration for efficient data handling and retrieval.</p>
            <span>
              <a href="/"><i className="fa fa-twitter"></i></a>
              <a href="/"><i className="fa fa-linkedin"></i></a>
            </span>
          </div>
          <div className="feature">
            <h3>Jitender Kaushik</h3>
            <a href="/">Quality Assurance</a>
            <p>Responsible for deploying the system using Docker, implementing CI/CD pipelines with Jenkins, 
              and ensuring smooth system performance during stress testing.</p>
            <span>
              <a href="/"><i className="fa fa-twitter"></i></a>
              <a href="/"><i className="fa fa-linkedin"></i></a>
            </span>
          </div>
        </div>
      </div>

      </div>
    </div>
  );
};

export default About;