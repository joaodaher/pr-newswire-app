import React from 'react';
import Card from '@mui/material/Card';
import CardContent from '@mui/material/CardContent';
import Typography from '@mui/material/Typography';
import Accordion from '@mui/material/Accordion';
import AccordionSummary from '@mui/material/AccordionSummary';
import AccordionDetails from '@mui/material/AccordionDetails';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';

const ArticleCard = ({ article }) => {
  return (
    <Card sx={{ height: '100%' }}>
      <CardContent>
        <Typography variant="h5" component="div">
          {article.title}
        </Typography>
        <Typography sx={{ mb: 1.5 }} color="text.secondary">
          {article.news_provided_by}
        </Typography>
        <Typography variant="body2" color="text.secondary">
          {new Date(article.date).toLocaleString()}
        </Typography>
      </CardContent>
      <Accordion>
        <AccordionSummary
          expandIcon={<ExpandMoreIcon />}
          aria-controls="panel1a-content"
          id="panel1a-header"
        >
          <Typography>Show Content</Typography>
        </AccordionSummary>
        <AccordionDetails>
          <Typography>{article.content}</Typography>
        </AccordionDetails>
      </Accordion>
    </Card>
  );
};

export default ArticleCard;
