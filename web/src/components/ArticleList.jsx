import React from 'react';
import ArticleCard from './ArticleCard';
import Grid from '@mui/material/Grid';

const ArticleList = ({ articles, onArticleClick }) => {
  return (
    <Grid container spacing={2}>
      {articles.map((article, index) => (
        <Grid item xs={12} sm={6} md={4} key={`${article.id}-${index}`} sx={{ display: 'flex' }}>
          <ArticleCard article={article} onClick={onArticleClick} />
        </Grid>
      ))}
    </Grid>
  );
};

export default ArticleList;
