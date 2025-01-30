// About.js
import React from 'react';


const About = () => {
  const teamMembers = [
    { 
      name: 'Dharmilkumar Nileshkumar Patel', 
      role: 'Project Manager', 
      photo: '/images/person_1.svg', 
      description: 'Alice is an experienced project manager with 10 years in the field.' 
    },
    { 
      name: 'Virpal Kaur', 
      role: 'Frontend Developer', 
      photo: '/images/person_2.svg', 
      description: 'Virpal kaur is a skilled full-stack developer who loves designing with 7 years of experience.' 
    },
    { 
      name: 'Jitender Kaushik', 
      role: 'Quality Assurance', 
      photo: '/images/person_1.svg', 
      description: 'Charlie creates intuitive designs that enhance user experience.' 
    },
    { 
      name: 'Mohamed Ayan Mohamed Arif Khatri', 
      role: 'Data Engineer', 
      photo: '/images/person_1.svg', 
      description: 'Alice is an experienced project manager with 10 years in the field.' 
    },
    { 
      name: 'Kevinsinh Manojsinh Raj', 
      role: 'Backend Developer', 
      photo: '/images/person_1.svg', 
      description: 'Bob is a skilled full-stack developer who loves solving complex problems.' 
    },
    { 
      name: 'Dharmikkumar Nareshbhai Bhatt', 
      role: 'AI/ML Specialist', 
      photo: '/images/person_1.svg', 
      description: 'Charlie creates intuitive designs that enhance user experience.' 
    },
  ];

  return (
    <main className="about-section bg-light min-vh-100">
      <div class="container">
        <h1 className="display-4 text-center">About Us</h1>
        <p className="mt-3 text-secondary text-center">Meet our amazing team dedicated to delivering exceptional results.</p>

        <div className="row mt-5 justify-content-center">
          {teamMembers.map((member, index) => (
            <div key={index} className="col-md-4 justify-content-center mb-4">
              <div className="card team-card text-center shadow-sm" style={{ borderRadius: '10px' }}>
                <img
                  src={member.photo}
                  alt={member.name}
                  className="card-img-top rounded-circle mt-3"
                  style={{ width: '100px', height: '100px', margin: '0 auto' }}
                />
                <div className="card-body">
                  <h5 className="card-title mb-1">{member.name}</h5>
                  <p className="card-text text-muted mb-2">{member.role}</p>
                  <div className="hover-details">
                    <p className="hover-desc">{member.description}</p>
                  </div>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </main>
  );
};

export default About;
