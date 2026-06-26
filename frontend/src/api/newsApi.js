import axios from "axios";

const API = "/api";

export const getNews = async () => {
  try {
    const response = await axios.get(`${API}/news`);
    return response.data;
  } catch (error) {
    console.error("Failed to fetch news:", error);
    return [];
  }
};

export const getNewsById = async (id) => {
  try {
    const response = await axios.get(`${API}/news/${id}`);
    return response.data;
  } catch (error) {
    console.error(`Failed to fetch article ${id}:`, error);
    return null;
  }
};