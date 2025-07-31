import { useEffect, useState } from "react";
import { Card, Container, Row, Col, Form, Button } from "react-bootstrap";
import { fetchNewsByKeyword } from "../api/news";
import { stripHtml, getSentimentColor } from "../utils/helper";

interface NewsItem {
    title: string;
    description: string;
    link: string;
    publishedAt: string;
    source: string;
    imageUrl: string;
    sentiment: string;
}

const Dashboard = () => {
    const [news, setNews] = useState<NewsItem[]>([]);
    const [filteredNews, setFilteredNews] = useState<NewsItem[]>([]);
    const [keyword, setKeyword] = useState<string>("");
    const [selectedSentiments, setSelectedSentiments] = useState<string[]>([]);


    const loadNews = async () => {
        try {
            const result = await fetchNewsByKeyword(keyword);
            setNews(result);
            setFilteredNews(result);

        } catch (err) {
            console.error("News fetch failed:", err);
        }
    };

    useEffect(() => {
        loadNews();
    }, []);

    const applyFilters = (allNews: NewsItem[], sentiments: string[]) => {
        if (sentiments.length === 0) {
            setFilteredNews(allNews);
        } else {
            setFilteredNews(
                allNews.filter(n =>
                    sentiments.includes(n.sentiment?.toLowerCase())
                )
            );
        }
    };
    const handleSentimentChange = (sentiment: string) => {
        console.log(sentiment);
        let updated = [...selectedSentiments];
        console.log(updated);
        if (updated.includes(sentiment)) {
            updated = updated.filter(s => s !== sentiment);
        } else {
            updated.push(sentiment);
        }
        setSelectedSentiments(updated);
        applyFilters(news, updated);
    };



    return (
        <Container className="mt-4">
            <h2 className="mb-4">Latest News</h2>
            <Form className="d-flex mb-4" onSubmit={(e) => { e.preventDefault(); loadNews(); }}>
                <Form.Control
                    type="text"
                    value={keyword}
                    onChange={(e) => setKeyword(e.target.value)}
                    placeholder="Enter keyword, e.g. AI, Politics, India"
                    className="me-2"
                />
                <Button variant="primary" type="submit">Search</Button>
            </Form>

            <Row>
                <Col md={2}>
                    <h5>Sentiment</h5>
                    <Form.Check
                        type="checkbox"
                        label="Positive"
                        checked={selectedSentiments.includes("positive")}
                        onChange={() => handleSentimentChange("positive")}
                    />
                    <Form.Check
                        type="checkbox"
                        label="Negative"
                        checked={selectedSentiments.includes("negative")}
                        onChange={() => handleSentimentChange("negative")}
                    />
                    <Form.Check
                        type="checkbox"
                        label="Neutral"
                        checked={selectedSentiments.includes("neutral")}
                        onChange={() => handleSentimentChange("neutral")}
                    />
                </Col>
                <Col md={10}>
                    <Row>
                        {filteredNews.map((item, idx) => (
                            <Col md={4} key={idx} className="mb-4">
                                <Card style={{ height: "100%" }}>
                                    {/* TOP SECTION: Image or Text Box */}
                                    {item.imageUrl && item.imageUrl.startsWith("http") ? (
                                        <div style={{ height: "180px", overflow: "hidden" }}>
                                            <Card.Img
                                                variant="top"
                                                src={item.imageUrl}
                                                alt="News"
                                                style={{ objectFit: "cover", height: "180px", width: "100%" }}
                                            />
                                        </div>
                                    ) : (
                                        <div
                                            style={{
                                                backgroundColor: "#f1f1f1",
                                                padding: "15px",
                                                height: "180px",
                                                overflow: "hidden",
                                                display: "flex",
                                                flexDirection: "column",
                                                justifyContent: "flex-start",
                                            }}
                                        >
                                            <strong style={{ fontSize: "1rem", marginBottom: "8px" }}>
                                                {item.title}
                                            </strong>
                                        </div>
                                    )}

                                    {/* MAIN BODY */}
                                    <Card.Body className="d-flex flex-column">
                                        {/* Badge for Sentiment */}
                                        <div className="mb-2">
                                            <span className={`badge text-white px-2 py-1 ${getSentimentColor(item.sentiment)}`}>
                                                {item.sentiment?.toUpperCase() || "NEUTRAL"}
                                            </span>
                                        </div>

                                        {item.imageUrl && (
                                            <Card.Title style={{ fontSize: "1rem" }}>{item.title}</Card.Title>
                                        )}
                                        <Card.Text style={{ flexGrow: 1 }}>
                                            {stripHtml(item.description).slice(0, 120) + "..."}
                                        </Card.Text>

                                        <a href={item.link} target="_blank" rel="noopener noreferrer">
                                            Read More
                                        </a>
                                    </Card.Body>

                                    <Card.Footer className="text-muted">
                                        {item.source} — {new Date(item.publishedAt).toLocaleString()}
                                    </Card.Footer>
                                </Card>
                            </Col>
                        ))}
                    </Row>
                </Col>
            </Row>
        </Container>
    );
};

export default Dashboard;
