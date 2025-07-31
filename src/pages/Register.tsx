import { useState } from "react";
import { registerUser } from "../api/auth";
import { useNavigate } from "react-router-dom";
import { Form, Button, Card, Container } from "react-bootstrap";

function Register() {
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [confirmPassword, setConfirmPassword] = useState("");
    const [fullName, setFullName] = useState("");
    const [showPassword, setShowPassword] = useState(false);
    const [agreed, setAgreed] = useState(false);
    const navigate = useNavigate();

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();

        if (!agreed) return alert("You must agree to the terms.");
        if (password !== confirmPassword) return alert("Passwords do not match.");

        try {
            await registerUser(email, password); // assuming fullName not yet stored
            alert("Registered successfully. Please log in.");
            navigate("/login");
        } catch {
            alert("Registration failed.");
        }
    };

    return (
        <Container className="d-flex justify-content-center mt-5">
            <Card style={{ width: "28rem" }} className="p-4 shadow-sm">
                <Card.Title className="mb-4 text-center">Create Account</Card.Title>
                <Form onSubmit={handleSubmit}>
                    <Form.Group className="mb-3">
                        <Form.Label>Full Name</Form.Label>
                        <Form.Control type="text" required value={fullName}
                            onChange={(e) => setFullName(e.target.value)} placeholder="Your name" />
                    </Form.Group>

                    <Form.Group className="mb-3">
                        <Form.Label>Email address</Form.Label>
                        <Form.Control type="email" required value={email}
                            onChange={(e) => setEmail(e.target.value)} placeholder="Enter email" />
                    </Form.Group>

                    <Form.Group className="mb-3">
                        <Form.Label>Password</Form.Label>
                        <Form.Control type={showPassword ? "text" : "password"} required value={password}
                            onChange={(e) => setPassword(e.target.value)} placeholder="Password" />
                    </Form.Group>

                    <Form.Group className="mb-3">
                        <Form.Label>Confirm Password</Form.Label>
                        <Form.Control type={showPassword ? "text" : "password"} required value={confirmPassword}
                            onChange={(e) => setConfirmPassword(e.target.value)} placeholder="Confirm Password" />
                    </Form.Group>

                    <Form.Group className="mb-3">
                        <Form.Check
                            type="checkbox"
                            label="Show Password"
                            checked={showPassword}
                            onChange={() => setShowPassword(!showPassword)}
                        />
                    </Form.Group>

                    <Form.Group className="mb-4">
                        <Form.Check
                            type="checkbox"
                            label="I agree to the Terms and Conditions"
                            checked={agreed}
                            onChange={() => setAgreed(!agreed)}
                            required
                        />
                    </Form.Group>

                    <Button type="submit" variant="success" className="w-100">
                        Sign Up
                    </Button>
                </Form>
            </Card>
        </Container>
    );
}

export default Register;
