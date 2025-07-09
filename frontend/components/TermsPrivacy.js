import React from "react";

const TermsPrivacy = () => {
  return (
    
    <div className="termpolicy-page mt-5 mb-5">
        <div className="container bg-white p-5">
            <h2 className="text-center"><b>Terms and Privacy Policy</b></h2>
            <div className="dashboard-content">
                <section>
                    <h5>1. Introduction</h5>
                    <p>
                    Welcome to the Real-Time News Analysis and Social Media Engagement System. 
                    Your privacy is important to us. This policy explains how we collect, use, 
                    and protect your data when using our platform.
                    </p>
                </section><br/>
                <section>
                    <h5>2. Data Collection</h5>
                    <p>We collect two types of data:</p>
                    <ul>
                    <li>
                        <strong>Personal Information:</strong> If you create an account, we may collect your 
                        name, email, and login credentials.
                    </li>
                    <li>
                        <strong>Non-Personal Data:</strong> Search queries, interaction logs, IP addresses, 
                        and device details are collected for analytics and trend detection.
                    </li>
                    </ul>
                    <p>
                    We may also use cookies to enhance your experience by remembering preferences 
                    and optimizing search performance.
                    </p>
                </section><br/>
                <section>
                    <h5>3. How We Use Your Data</h5>
                    <p>Your data is used to:</p>
                    <ul>
                    <li>Improve search accuracy and detect real-time trends.</li>
                    <li>Provide personalized news suggestions.</li>
                    <li>Optimize performance through analytics and caching.</li>
                    </ul>
                    <p><strong>We do not sell or share your personal data with third parties.</strong></p>
                </section><br/>
                <section>
                    <h5>4. Data Storage & Security</h5>
                    <ul>
                    <li>News articles are securely stored in <strong>MongoDB</strong>.</li>
                    <li>Frequently searched trends are cached in <strong>Redis</strong>.</li>
                    <li>Search queries are indexed in <strong>Elasticsearch</strong> without storing personal details.</li>
                    <li>We use encryption and firewall protection for sensitive data.</li>
                    </ul>
                </section><br/>
                <section>
                    <h5>5. Third-Party Services</h5>
                    <p>
                    Our system integrates with third-party APIs like NewsAPI and OpenAI for real-time 
                    news fetching and AI-driven analysis. However, no personal data is shared with these services.
                    </p>
                </section><br/>
                <section>
                    <h5>6. User Rights & Choices</h5>
                    <p>As a user, you have the right to:</p>
                    <ul>
                    <li><strong>Request data deletion</strong> from our servers.</li>
                    <li><strong>Disable cookies</strong> in your browser settings.</li>
                    <li><strong>Opt-out of analytics tracking</strong> through account settings.</li>
                    </ul>
                </section><br/>
                <section>
                    <h5>7. Changes to This Policy</h5>
                    <p>
                    We may update this policy periodically. Any changes will be communicated via 
                    a website notification or email.
                    </p>
                </section><br/>
            </div>
        </div>
    </div>
  );
};

export default TermsPrivacy;
