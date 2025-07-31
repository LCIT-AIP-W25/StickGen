import axios from 'axios';
import React, { useState } from 'react'
import { Button, Card, Container, Form, FormControl } from 'react-bootstrap'
import { useNavigate, useSearchParams } from 'react-router-dom';

function ResetPassword() {
    const [searchParams] = useSearchParams();

    const [password, setPassword] = useState("");
    const [confirmPassword, setConfirmPassword] = useState("");
    const navigate = useNavigate();
    const userId = searchParams.get("userId");
    const token = searchParams.get("token");
    const API_URL = "https://localhost:5269/api";

    const handleReset = async (e: React.FormEvent) => {
        e.preventDefault();

        if (password !== confirmPassword) {
            alert("Passwords do not match");
            return;
        }

        try {
            await axios.post(`${API_URL}/auth/reset-password`, {
                userId,
                token,
                newPassword: password
            });

            alert("Password reset successfully!");
            navigate("/login");
        } catch (err) {
            console.error(err);
            alert("Failed to reset password. The link may have expired.");
        }
    };


    return (
        <Container className='d-flex justify-content-center mt-5'>
            <Card style={{ width: "25rem" }} className='p-4 shadow'>
                <Card.Title className='mb-4 text-center'>Reset Password</Card.Title>
                <Form onSubmit={handleReset}>
                    <Form.Group className='mb-3'>
                        <Form.Label>New Password</Form.Label>
                        <FormControl type='password' required value={password} onChange={(e) => setPassword(e.target.value)} placeholder='Enter new Password' />
                    </Form.Group>
                    <Form.Group className='mb-4'>
                        <Form.Label>Confirm Password</Form.Label>
                        <FormControl type='password' required value={confirmPassword} onChange={(e) => setConfirmPassword(e.target.value)} placeholder='Enter new Password' />
                    </Form.Group>
                    <Button variant="secondary" type="submit" className="w-100">Reset Password</Button>

                </Form>
            </Card>
        </Container>
    )
}

export default ResetPassword