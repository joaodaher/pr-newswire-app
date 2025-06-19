import React from 'react';
import Typography from '@mui/material/Typography';
import Box from '@mui/material/Box';

const NoArticles = () => {
  return (
    <Box sx={{ textAlign: 'center', p: 4 }}>
      <Typography variant="h6">No articles found</Typography>
      <Typography variant="body1">Try adjusting your search filters.</Typography>
    </Box>
  );
};

export default NoArticles;
