import React, { useState, useEffect } from 'react';
import axios from 'axios';
import Header from '../components/Header';
import Filters from '../components/Filters';
import ArticleList from '../components/ArticleList';

const HomePage = () => {
  const [articles, setArticles] = useState([]);
  const [loading, setLoading] = useState(true);
  const [filters, setFilters] = useState({
    title: '',
    content: '',
    news_provider: '',
    start_date: '',
    end_date: '',
  });

  const fetchArticles = async () => {
    setLoading(true);
    try {
      const params = new URLSearchParams();
      for (const key in filters) {
        if (filters[key]) {
          params.append(key, filters[key]);
        }
      }
      const response = await axios.get(`http://0.0.0.0:8000/v1/articles?${params.toString()}`);
      setArticles(response.data.items);
    } catch (error) {
      console.error('Error fetching articles:', error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchArticles({});
  }, [fetchArticles]);

  const handleSearch = (newFilters) => {
    fetchArticles(newFilters);
  };

  return (
    <div className="bg-gray-50 min-h-screen">
      <Header />
      <main className="container mx-auto p-4">
        <Filters onSearch={handleSearch} />
        <ArticleList articles={articles} loading={loading} />
      </main>
    </div>
  );
};

export default HomePage;
