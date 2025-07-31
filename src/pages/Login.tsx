import { useState } from "react";
import { loginUser } from "../api/auth";
import { useNavigate } from "react-router-dom";
import { Form, Button, Card, Container } from "react-bootstrap";

function Login() {
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const navigate = useNavigate();

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        try {
            const res = await loginUser(email, password);
            localStorage.setItem("token", res.token);
            localStorage.setItem("email", res.email);
            localStorage.setItem("role", res.role);
            navigate("/dashboard");
        } catch {
            alert("Login failed");
        }
    };

    return (
        <Container className="d-flex justify-content-center mt-5">
            <Card style={{ width: "25rem" }} className="p-4 shadow">
                <Card.Title className="mb-4 text-center">Login</Card.Title>
                <Form onSubmit={handleSubmit}>
                    <Form.Group className="mb-3">
                        <Form.Label>Email address</Form.Label>
                        <Form.Control type="email" required value={email}
                            onChange={(e) => setEmail(e.target.value)} placeholder="Enter email" />
                    </Form.Group>

                    <Form.Group className="mb-4">
                        <Form.Label>Password</Form.Label>
                        <Form.Control type="password" required value={password}
                            onChange={(e) => setPassword(e.target.value)} placeholder="Password" />
                    </Form.Group>

                    <Button variant="primary" type="submit" className="w-100">Login</Button>
                    <Form.Text className="text-muted d-block text-center mt-3">
                        <a href="/forgot-password">Forgot Password?</a>
                    </Form.Text>

                </Form>
            </Card>
        </Container>
    );
}

export default Login;
