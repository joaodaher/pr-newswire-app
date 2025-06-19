import React from 'react';
import ArticleCard from './ArticleCard';
import Grid from '@mui/material/Grid';

const ArticleList = ({ articles }) => {
  return (
    <Grid container spacing={2}>
      {articles.map((article, index) => (
        <Grid item xs={12} sm={6} md={4} key={`${article.id}-${index}`}>
          <ArticleCard article={article} />
        </Grid>
      ))}
    </Grid>
  );
};

export default ArticleList;
