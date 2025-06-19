import React, { useState, useEffect, useCallback } from 'react';
import axios from 'axios';
import Header from '../components/Header';
import Filters from '../components/Filters';
import ArticleList from '../components/ArticleList';
import Container from '@mui/material/Container';
import CssBaseline from '@mui/material/CssBaseline';
import Box from '@mui/material/Box';

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
    <Box sx={{ display: 'flex', flexDirection: 'column', minHeight: '100vh' }}>
      <CssBaseline />
      <Header />
      <Container component="main" sx={{ mt: 4, mb: 4, flexGrow: 1 }}>
        <Filters onSearch={handleSearch} />
        <ArticleList articles={articles} loading={loading} />
      </Container>
    </Box>
  );
};

export default HomePage;
