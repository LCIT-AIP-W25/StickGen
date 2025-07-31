import axios from "axios";

const API_URL = import.meta.env.VITE_API_BASE_URL;

export const registerUser = async (email: string, password: string, role: string = "Admin") => {
    const res = await axios.post(`${API_URL}/auth/register`, { email, password, role });
    return res.data;
  };
  
  export const loginUser = async (email: string, password: string) => {
    const res = await axios.post(`${API_URL}/auth/login`, { email, password });
    return res.data; // contains token, email, role
  };
export const forgotPassword = async (email: string) => {
  const res = await axios.post(`${API_URL}/auth/forgot-password`, { email });
  return res.data;
}