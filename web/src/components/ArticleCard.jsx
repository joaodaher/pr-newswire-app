import React from 'react';

const ArticleCard = ({ article }) => {
  return (
    <div className="bg-white p-4 rounded-lg shadow-md">
      <h2 className="text-xl font-bold mb-2">{article.title}</h2>
      <p className="text-gray-600 mb-2">
        <span className="font-semibold">News Provider:</span> {article.news_provided_by}
      </p>
      <p className="text-gray-600 mb-2">
        <span className="font-semibold">Date:</span> {new Date(article.date).toLocaleString()}
      </p>
      <p className="text-gray-700">{article.content}</p>
    </div>
  );
};

export default ArticleCard;
