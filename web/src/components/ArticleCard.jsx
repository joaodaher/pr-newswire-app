import React from 'react';
import Card from '@mui/material/Card';
import CardContent from '@mui/material/CardContent';
import Typography from '@mui/material/Typography';
import CardActionArea from '@mui/material/CardActionArea';
import Box from '@mui/material/Box';

const ArticleCard = ({ article, onClick }) => {
  return (
    <Card
      elevation={2}
      sx={{
        height: '100%',
        display: 'flex',
        flexDirection: 'column',
        transition: 'box-shadow 0.3s ease-in-out',
        '&:hover': {
          boxShadow: 8,
        },
      }}
    >
      <CardActionArea
        onClick={() => onClick(article)}
        sx={{ height: '100%', display: 'flex' }}
      >
        <CardContent sx={{ display: 'flex', flexDirection: 'column', flexGrow: 1 }}>
          <Typography
            variant="h6"
            component="h2"
            sx={{
              fontWeight: '600',
              overflow: 'hidden',
              textOverflow: 'ellipsis',
              display: '-webkit-box',
              WebkitLineClamp: '3',
              WebkitBoxOrient: 'vertical',
              lineHeight: 1.4,
              mb: 1,
            }}
          >
            {article.title}
          </Typography>

          <Box sx={{ marginTop: 'auto' }}>
            <Typography variant="body2" color="primary" sx={{ fontWeight: 'bold', mt: 1 }}>
              {article.news_provided_by}
            </Typography>
            <Typography variant="caption" color="text.secondary">
              {new Date(article.date).toLocaleString()}
            </Typography>
          </Box>
        </CardContent>
      </CardActionArea>
    </Card>
  );
};

export default ArticleCard;
