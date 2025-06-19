import React, { useState, useEffect, useCallback } from 'react';
import axios from 'axios';
import Header from '../components/Header';
import Filters from '../components/Filters';
import ArticleList from '../components/ArticleList';

const HomePage = () => {
  const [articles, setArticles] = useState([]);
  const [loading, setLoading] = useState(true);

  const fetchArticles = useCallback(async (currentFilters) => {
    setLoading(true);
    try {
      const params = new URLSearchParams({ limit: 50 });
      for (const key in currentFilters) {
        if (currentFilters[key]) {
          params.append(key, currentFilters[key]);
        }
      }
      const response = await axios.get(`http://0.0.0.0:8000/v1/articles?${params.toString()}`);
      setArticles(response.data.items);
    } catch (error) {
      console.error('Error fetching articles:', error);
    } finally {
      setLoading(false);
    }
  }, []);

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
