import { useEffect, useState } from "react";
import { fetchNews } from "../api/news";
import { Button } from "react-bootstrap";
import { useNavigate } from "react-router-dom";



function Home() {
    const navigate = useNavigate();
    useEffect(() => {
        const isLoggedIn = localStorage.getItem("authToken"); // or "user" key
        if (isLoggedIn) {
            navigate("/dashboard");
        } else {
            navigate("/login");
        }
    }, [navigate]);

    return null;

}

export default Home;
