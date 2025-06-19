import React, { useState, useCallback } from 'react';
import TextField from '@mui/material/TextField';
import Grid from '@mui/material/Grid';
import Box from '@mui/material/Box';
import { AdapterDayjs } from '@mui/x-date-pickers/AdapterDayjs';
import { LocalizationProvider } from '@mui/x-date-pickers/LocalizationProvider';
import { DatePicker } from '@mui/x-date-pickers/DatePicker';
import dayjs from 'dayjs';

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
    start_date: null,
    end_date: null,
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

  const handleDateChange = (name, value) => {
    setFilters((prevFilters) => {
      let newDate = value;
      if (newDate) {
        if (name === 'start_date') {
          newDate = newDate.startOf('day');
        } else if (name === 'end_date') {
          newDate = newDate.endOf('day');
        }
      }

      const newFilters = {
        ...prevFilters,
        [name]: newDate ? newDate.toISOString() : null,
      };
      debouncedOnSearch(newFilters);
      return newFilters;
    });
  };

  return (
    <LocalizationProvider dateAdapter={AdapterDayjs}>
      <Box sx={{ p: 2, backgroundColor: 'grey.100', borderRadius: 1, mb: 4 }}>
        <Grid container spacing={2} alignItems="center">
          <Grid item xs={12} md={3}>
            <TextField
              fullWidth
              name="title"
              label="Filter by title"
              value={filters.title}
              onChange={handleInputChange}
              size="small"
            />
          </Grid>
          <Grid item xs={12} md={3}>
            <TextField
              fullWidth
              name="content"
              label="Filter by content"
              value={filters.content}
              onChange={handleInputChange}
              size="small"
            />
          </Grid>
          <Grid item xs={12} md={3}>
            <TextField
              fullWidth
              name="news_provider"
              label="Filter by news provider"
              value={filters.news_provider}
              onChange={handleInputChange}
              size="small"
            />
          </Grid>
          <Grid item xs={12} md={3}>
            <Grid container spacing={2}>
              <Grid item xs={6}>
                <DatePicker
                  label="Start date"
                  value={filters.start_date ? dayjs(filters.start_date) : null}
                  onChange={(newValue) => handleDateChange('start_date', newValue)}
                  slotProps={{ textField: { fullWidth: true, size: 'small' } }}
                />
              </Grid>
              <Grid item xs={6}>
                <DatePicker
                  label="End date"
                  value={filters.end_date ? dayjs(filters.end_date) : null}
                  onChange={(newValue) => handleDateChange('end_date', newValue)}
                  slotProps={{ textField: { fullWidth: true, size: 'small' } }}
                />
              </Grid>
            </Grid>
          </Grid>
        </Grid>
      </Box>
    </LocalizationProvider>
  );
};

export default Filters;
