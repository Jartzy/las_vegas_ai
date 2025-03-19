// src/components/EventsDisplay.tsx
import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import {
  Container,
  Grid,
  Card,
  CardContent,
  Typography,
  CardMedia,
  Box,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  SelectChangeEvent,
  CircularProgress,
  Alert,
  Chip,
  Paper,
  Rating,
  Divider,
} from '@mui/material';
import { Event, EventFilters } from '../types/event';
import { useEvents } from '../services/eventService';
import { formatDate } from '../utils/dateUtils';
import AttractionsIcon from '@mui/icons-material/Attractions';
import LocalActivityIcon from '@mui/icons-material/LocalActivity';

interface EventsDisplayProps {
  userLocation?: { latitude: number; longitude: number };
}

const DEFAULT_IMAGE = 'https://images.unsplash.com/photo-1581351721010-8cf859cb14a4?q=80&w=1200&auto=format&fit=crop';

const EventsDisplay: React.FC<EventsDisplayProps> = ({ userLocation }) => {
  const [filters, setFilters] = useState<EventFilters>({
    category: 'all',
    priceRange: 'all',
    timeframe: 'all',
    sortBy: 'date',
    location: userLocation,
    rating: 0,
  });

  const { data: events, isLoading, isError, error } = useEvents(filters);

  const handleFilterChange = (event: SelectChangeEvent<string>) => {
    const { name, value } = event.target;
    setFilters((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  const renderPriceTag = (min: number, max: number) => {
    const priceLevel = min < 50 ? '$' : min < 100 ? '$$' : min < 200 ? '$$$' : '$$$$';
    return (
      <Chip
        label={priceLevel}
        size="small"
        sx={{
          backgroundColor: 'primary.main',
          color: 'white',
          fontWeight: 'bold',
        }}
      />
    );
  };

  const renderEventCard = (event: Event) => (
    <Link 
      to={`/events/${event.id}`} 
      style={{ textDecoration: 'none', display: 'block', height: '100%' }}
    >
      <Card
        sx={{
          height: '100%',
          display: 'flex',
          flexDirection: 'column',
          transition: 'transform 0.2s',
          '&:hover': {
            transform: 'translateY(-4px)',
            boxShadow: 6,
          },
        }}
      >
        <CardMedia
          component="img"
          height="200"
          image={event.image_url || DEFAULT_IMAGE}
          alt={event.name}
          sx={{ 
            objectFit: 'cover',
            backgroundColor: 'grey.100' 
          }}
          onError={(e) => {
            const target = e.target as HTMLImageElement;
            target.src = DEFAULT_IMAGE;
          }}
        />
        <CardContent sx={{ flexGrow: 1, p: 2 }}>
          <Box sx={{ mb: 2 }}>
            <Typography gutterBottom variant="h6" component="h2" sx={{ fontWeight: 'bold' }}>
              {event.name}
            </Typography>
            <Box sx={{ display: 'flex', gap: 1, mb: 1, flexWrap: 'wrap' }}>
              {renderPriceTag(event.price_range_min, event.price_range_max)}
              <Chip
                label={event.category}
                size="small"
                sx={{ backgroundColor: 'secondary.light' }}
              />
              {event.tags?.map((tag) => (
                <Chip 
                  key={`${event.id}-${tag}`} 
                  label={tag} 
                  size="small" 
                  variant="outlined" 
                />
              ))}
            </Box>
          </Box>
          <Typography 
            variant="body2" 
            color="text.secondary" 
            sx={{ 
              mb: 2,
              display: '-webkit-box',
              WebkitLineClamp: 3,
              WebkitBoxOrient: 'vertical',
              overflow: 'hidden',
              textOverflow: 'ellipsis'
            }}
          >
            {event.description}
          </Typography>
          <Box sx={{ mt: 'auto' }}>
            <Typography variant="body2" color="text.primary" sx={{ mb: 1 }}>
              {formatDate(event.start_date)}
            </Typography>
            <Typography variant="body2" color="text.secondary" sx={{ mb: 1 }}>
              {event.address}
            </Typography>
            <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
              <Rating value={event.rating} precision={0.5} size="small" readOnly />
              <Typography variant="body2" color="text.secondary">
                ({event.review_count})
              </Typography>
            </Box>
          </Box>
        </CardContent>
      </Card>
    </Link>
  );

  if (isLoading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="50vh">
        <CircularProgress />
      </Box>
    );
  }

  if (isError) {
    return (
      <Container>
        <Alert severity="error">
          Error loading events: {error instanceof Error ? error.message : 'Unknown error'}
        </Alert>
      </Container>
    );
  }

  const aiCuratedExperiences = events?.filter((event) => event.rating >= 4.5);
  const popularAttractions = events?.filter((event) => event.review_count > 1000);

  return (
    <Container maxWidth="lg" sx={{ py: 4 }}>
      <Paper sx={{ p: 3, mb: 4 }} elevation={0}>
        <Grid container spacing={2}>
          <Grid item xs={12} sm={3}>
            <FormControl fullWidth>
              <InputLabel>Duration</InputLabel>
              <Select
                name="timeframe"
                value={filters.timeframe}
                label="Duration"
                onChange={handleFilterChange}
              >
                <MenuItem value="all">Any Duration</MenuItem>
                <MenuItem value="today">Just for a Day</MenuItem>
                <MenuItem value="this-week">Visiting for a Week</MenuItem>
                <MenuItem value="this-month">I'm a Local</MenuItem>
              </Select>
            </FormControl>
          </Grid>
          <Grid item xs={12} sm={3}>
            <FormControl fullWidth>
              <InputLabel>Category</InputLabel>
              <Select
                name="category"
                value={filters.category}
                label="Category"
                onChange={handleFilterChange}
              >
                <MenuItem value="all">All Categories</MenuItem>
                <MenuItem value="shows">Shows</MenuItem>
                <MenuItem value="concerts">Concerts</MenuItem>
                <MenuItem value="sports">Sports</MenuItem>
                <MenuItem value="comedy">Comedy</MenuItem>
                <MenuItem value="cirque">Cirque du Soleil</MenuItem>
              </Select>
            </FormControl>
          </Grid>
          <Grid item xs={12} sm={3}>
            <FormControl fullWidth>
              <InputLabel>Price Range</InputLabel>
              <Select
                name="priceRange"
                value={filters.priceRange}
                label="Price Range"
                onChange={handleFilterChange}
              >
                <MenuItem value="all">All Prices</MenuItem>
                <MenuItem value="under-50">Under $50</MenuItem>
                <MenuItem value="50-100">$50 - $100</MenuItem>
                <MenuItem value="100-200">$100 - $200</MenuItem>
                <MenuItem value="over-200">Over $200</MenuItem>
              </Select>
            </FormControl>
          </Grid>
          <Grid item xs={12} sm={3}>
            <FormControl fullWidth>
              <InputLabel>Sort By</InputLabel>
              <Select
                name="sortBy"
                value={filters.sortBy}
                label="Sort By"
                onChange={handleFilterChange}
              >
                <MenuItem value="date">Date</MenuItem>
                <MenuItem value="price-low">Price: Low to High</MenuItem>
                <MenuItem value="price-high">Price: High to Low</MenuItem>
                <MenuItem value="rating">Rating</MenuItem>
              </Select>
            </FormControl>
          </Grid>
        </Grid>
      </Paper>

      <Box sx={{ mb: 6 }} id="experiences">
        <Box sx={{ display: 'flex', alignItems: 'center', mb: 3 }}>
          <AttractionsIcon sx={{ mr: 1, color: 'primary.main' }} />
          <Typography variant="h5" component="h2" sx={{ fontWeight: 'bold' }}>
            AI-Curated Experiences
          </Typography>
        </Box>
        <Grid container spacing={3}>
          {aiCuratedExperiences?.slice(0, 6).map((event) => (
            <Grid item key={event.id} xs={12} sm={6} md={4}>
              {renderEventCard(event)}
            </Grid>
          ))}
        </Grid>
      </Box>

      <Divider sx={{ my: 6 }} />

      <Box sx={{ mb: 6 }}>
        <Box sx={{ display: 'flex', alignItems: 'center', mb: 3 }}>
          <LocalActivityIcon sx={{ mr: 1, color: 'primary.main' }} />
          <Typography variant="h5" component="h2" sx={{ fontWeight: 'bold' }}>
            Popular Attractions
          </Typography>
        </Box>
        <Grid container spacing={3}>
          {popularAttractions?.slice(0, 9).map((event) => (
            <Grid item key={event.id} xs={12} sm={6} md={4}>
              {renderEventCard(event)}
            </Grid>
          ))}
        </Grid>
      </Box>

      <Divider sx={{ my: 6 }} />

      <Box sx={{ mb: 6 }}>
        <Box sx={{ display: 'flex', alignItems: 'center', mb: 3 }}>
          <LocalActivityIcon sx={{ mr: 1, color: 'primary.main' }} />
          <Typography variant="h5" component="h2" sx={{ fontWeight: 'bold' }}>
            All Events
          </Typography>
        </Box>
        <Grid container spacing={3}>
          {events?.map((event) => (
            <Grid item key={event.id} xs={12} sm={6} md={4}>
              {renderEventCard(event)}
            </Grid>
          ))}
        </Grid>
      </Box>
    </Container>
  );
};

export default EventsDisplay;