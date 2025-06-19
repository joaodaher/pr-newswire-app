import React from 'react';
import ArticleCard from './ArticleCard';
import NoArticles from './NoArticles';
import Spinner from './Spinner';

const ArticleList = ({ articles, loading }) => {
  if (loading) {
    return <Spinner />;
  }

  if (articles.length === 0) {
    return <NoArticles />;
  }

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
      {articles.map((article) => (
        <ArticleCard key={article.id} article={article} />
      ))}
    </div>
  );
};

export default ArticleList;
