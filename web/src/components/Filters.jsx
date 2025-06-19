import React, { useState, useCallback } from 'react';

const debounce = (func, delay) => {
  let timeout;
  return (...args) => {
    clearTimeout(timeout);
    timeout = setTimeout(() => func(...args), delay);
  };
};

const Filters = ({ onSearch }) => {
  const [filters, setFilters] = useState({
    title: '',
    content: '',
    news_provider: '',
    start_date: '',
    end_date: '',
  });

  const debouncedOnSearch = useCallback(debounce(onSearch, 500), [onSearch]);

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFilters((prevFilters) => {
      const newFilters = {
        ...prevFilters,
        [name]: value,
      };
      debouncedOnSearch(newFilters);
      return newFilters;
    });
  };

  return (
    <div className="p-4 bg-gray-100 rounded-lg shadow-md mb-4">
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <input
          type="text"
          name="title"
          placeholder="Filter by title"
          value={filters.title}
          onChange={handleInputChange}
          className="p-2 border rounded-md"
        />
        <input
          type="text"
          name="content"
          placeholder="Filter by content"
          value={filters.content}
          onChange={handleInputChange}
          className="p-2 border rounded-md"
        />
        <input
          type="text"
          name="news_provider"
          placeholder="Filter by news provider"
          value={filters.news_provider}
          onChange={handleInputChange}
          className="p-2 border rounded-md"
        />
        <div className="flex gap-2">
          <input
            type="datetime-local"
            name="start_date"
            value={filters.start_date}
            onChange={handleInputChange}
            className="p-2 border rounded-md w-full"
          />
          <input
            type="datetime-local"
            name="end_date"
            value={filters.end_date}
            onChange={handleInputChange}
            className="p-2 border rounded-md w-full"
          />
        </div>
      </div>
    </div>
  );
};

export default Filters;
