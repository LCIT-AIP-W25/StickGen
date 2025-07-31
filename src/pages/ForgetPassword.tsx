import React, { useState } from 'react'
import { Button, Card, Container, Form } from 'react-bootstrap'
import { forgotPassword } from '../api/auth';

function ForgetPassword() {

    const handleSumbit = async (e: React.FormEvent) => {
        e.preventDefault();
        try {
            await forgotPassword(email);
            alert("Check your email for the reset link.");
        } catch (err) {
            alert("Failed to send reset link.");
          }
        console.log("Sending forgot password to", email);
        setSubmitted(true);
    };


    const [email, setEmail] = useState("");
    const [submitted, setSubmitted] = useState(false);

    return (
        <Container className="d-flex justify-content-center mt-5">
            <Card style={{ width: "25rem" }} className="p-4 shadow">
                <Card.Title className='mb-4 text-center'> Forgot Password </Card.Title>
                {submitted ? (<p className='text-success text center'>If this email exists, a resent link has been sent.</p>) :
                    (<Form onSubmit={handleSumbit}>
                        <Form.Group className='mb-3'>
                            <Form.Label>Email Address</Form.Label>
                            <Form.Control type='email' required value={email} onChange={(e) => setEmail(e.target.value)} placeholder='Enter your registered email'>
                            </Form.Control>
                        </Form.Group>

                        <Button variant='primary' type='submit' className='w-100'>
                            Send Reset Link
                        </Button>
                    </Form>
                    )}
            </Card>
        </Container>
    )
}

export default ForgetPassword