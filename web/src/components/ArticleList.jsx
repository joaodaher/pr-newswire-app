import React from 'react';
import ArticleCard from './ArticleCard';
import NoArticles from './NoArticles';
import Spinner from './Spinner';
import Grid from '@mui/material/Grid';

const ArticleList = ({ articles, loading }) => {
  if (loading) {
    return <Spinner />;
  }

  if (articles.length === 0) {
    return <NoArticles />;
  }

  return (
    <Grid container spacing={2}>
      {articles.map((article) => (
        <Grid item xs={12} sm={6} md={4} key={article.id}>
          <ArticleCard article={article} />
        </Grid>
      ))}
    </Grid>
  );
};

export default ArticleList;
