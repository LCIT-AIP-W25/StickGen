import axios from "axios";

const API_URL = import.meta.env.VITE_API_BASE_URL;

export const fetchNews = async () => {
  const response = await axios.get(`${API_URL}/rss/fetch?keyword=AI`);
  return response.data;
};
export const fetchNewsByKeyword = async (keyword: string) => {
  const response = await axios.get(`${API_URL}/rss/fetch?keyword=${encodeURIComponent(keyword)}`);
  return response.data;
};
