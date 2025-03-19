import React, { useState } from 'react';
import { useParams } from 'react-router-dom';
import {
  Container,
  Grid,
  Typography,
  Box,
  Button,
  Chip,
  Rating,
  Divider,
  Paper,
  ImageList,
  ImageListItem,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
  Card,
  CardContent,
  useTheme,
  useMediaQuery,
  CircularProgress,
  Alert,
} from '@mui/material';
import {
  AccessTime,
  LocationOn,
  AttachMoney,
  EventSeat,
  Info,
  LocalParking,
  AccessibilityNew,
  Language,
  Security,
  CheckCircle,
} from '@mui/icons-material';
import { useEvent } from '../services/eventService';
import { formatDate } from '../utils/dateUtils';
import Map from './Map';

const EventLanding: React.FC = () => {
  const { eventId } = useParams<{ eventId: string }>();
  const { data: event, isLoading, isError, error } = useEvent(Number(eventId));
  const theme = useTheme();
  const isMobile = useMediaQuery(theme.breakpoints.down('sm'));
  const [selectedImage, setSelectedImage] = useState<string | undefined>(undefined);

  // Update selectedImage when event data is loaded
  React.useEffect(() => {
    if (event?.image_url) {
      setSelectedImage(event.image_url);
    }
  }, [event]);

  const getBookingUrl = () => {
    if (event.booking_url) {
      return event.booking_url;
    }
    if (event.url) {
      return event.url;
    }
    if (event.affiliate_links?.tickets) {
      return event.affiliate_links.tickets;
    }
    return null;
  };

  const bookingUrl = event ? getBookingUrl() : null;

  if (isLoading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="50vh">
        <CircularProgress />
      </Box>
    );
  }

  if (isError || !event) {
    return (
      <Container>
        <Alert severity="error">
          Error loading event: {error instanceof Error ? error.message : 'Unknown error'}
        </Alert>
      </Container>
    );
  }

  const renderEventDetails = () => (
    <List>
      {event.duration_minutes && (
        <ListItem>
          <ListItemIcon>
            <AccessTime color="primary" />
          </ListItemIcon>
          <ListItemText 
            primary="Duration" 
            secondary={`${Math.floor(event.duration_minutes / 60)}h ${event.duration_minutes % 60}min`} 
          />
        </ListItem>
      )}
      <ListItem>
        <ListItemIcon>
          <LocationOn color="primary" />
        </ListItemIcon>
        <ListItemText 
          primary={event.venue?.name || 'Venue'} 
          secondary={event.venue ? `${event.venue.address}, ${event.venue.city}, ${event.venue.state} ${event.venue.zip}` : event.address} 
        />
      </ListItem>
      <ListItem>
        <ListItemIcon>
          <AttachMoney color="primary" />
        </ListItemIcon>
        <ListItemText 
          primary="Price Range" 
          secondary={`$${event.price_range_min} - $${event.price_range_max}`} 
        />
      </ListItem>
      {event.capacity && (
        <ListItem>
          <ListItemIcon>
            <EventSeat color="primary" />
          </ListItemIcon>
          <ListItemText 
            primary="Capacity" 
            secondary={`${event.capacity} seats${event.availability ? ` (${event.availability} available)` : ''}`} 
          />
        </ListItem>
      )}
    </List>
  );

  const renderAdditionalInfo = () => (
    <Grid container spacing={2}>
      {event.age_restriction && (
        <Grid item xs={12} sm={6}>
          <Paper sx={{ p: 2 }}>
            <Box display="flex" alignItems="center" mb={1}>
              <Security color="primary" sx={{ mr: 1 }} />
              <Typography variant="h6">Age Restriction</Typography>
            </Box>
            <Typography>
              {typeof event.age_restriction === 'number' 
                ? `${event.age_restriction}+ years old`
                : event.age_restriction}
            </Typography>
          </Paper>
        </Grid>
      )}
      {event.parking_info && (
        <Grid item xs={12} sm={6}>
          <Paper sx={{ p: 2 }}>
            <Box display="flex" alignItems="center" mb={1}>
              <LocalParking color="primary" sx={{ mr: 1 }} />
              <Typography variant="h6">Parking Information</Typography>
            </Box>
            <Typography>{event.parking_info}</Typography>
          </Paper>
        </Grid>
      )}
      {event.accessibility_options && event.accessibility_options.length > 0 && (
        <Grid item xs={12} sm={6}>
          <Paper sx={{ p: 2 }}>
            <Box display="flex" alignItems="center" mb={1}>
              <AccessibilityNew color="primary" sx={{ mr: 1 }} />
              <Typography variant="h6">Accessibility</Typography>
            </Box>
            <Box display="flex" gap={1} flexWrap="wrap">
              {event.accessibility_options.map((option, index) => (
                <Chip key={`${event.id}-accessibility-${index}`} label={option} size="small" />
              ))}
            </Box>
          </Paper>
        </Grid>
      )}
      {event.language && (
        <Grid item xs={12} sm={6}>
          <Paper sx={{ p: 2 }}>
            <Box display="flex" alignItems="center" mb={1}>
              <Language color="primary" sx={{ mr: 1 }} />
              <Typography variant="h6">Language</Typography>
            </Box>
            <Typography>{event.language}</Typography>
          </Paper>
        </Grid>
      )}
    </Grid>
  );

  const renderReviews = () => (
    <Box>
      <Typography variant="h5" gutterBottom>
        Reviews
      </Typography>
      <Grid container spacing={2}>
        {event.reviews?.map((review, index) => (
          <Grid item xs={12} key={`${event.id}-review-${index}`}>
            <Card>
              <CardContent>
                <Box display="flex" justifyContent="space-between" alignItems="center" mb={1}>
                  <Typography variant="subtitle1" fontWeight="bold">
                    {review.user_name}
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    {formatDate(review.date)}
                  </Typography>
                </Box>
                <Rating value={review.rating} readOnly size="small" />
                <Typography variant="body1" mt={1}>
                  {review.comment}
                </Typography>
                {review.images && review.images.length > 0 && (
                  <ImageList cols={isMobile ? 2 : 4} gap={8} sx={{ mt: 2 }}>
                    {review.images.map((image, imgIndex) => (
                      <ImageListItem key={`${event.id}-review-${index}-image-${imgIndex}`}>
                        <img src={image} alt={`Review ${imgIndex + 1}`} loading="lazy" />
                      </ImageListItem>
                    ))}
                  </ImageList>
                )}
              </CardContent>
            </Card>
          </Grid>
        ))}
      </Grid>
    </Box>
  );

  return (
    <Container maxWidth="lg" sx={{ py: 4 }}>
      <Grid container spacing={4}>
        {/* Left Column - Images and Main Info */}
        <Grid item xs={12} md={8}>
          <Box sx={{ mb: 4 }}>
            <img
              src={selectedImage || event.image_url}
              alt={event.name}
              style={{
                width: '100%',
                height: '400px',
                objectFit: 'cover',
                borderRadius: theme.shape.borderRadius,
              }}
            />
            {event.gallery_images && event.gallery_images.length > 0 && (
              <ImageList cols={isMobile ? 4 : 6} gap={8} sx={{ mt: 1 }}>
                {[event.image_url, ...event.gallery_images].map((image, index) => (
                  <ImageListItem 
                    key={`${event.id}-image-${index}`}
                    sx={{ 
                      cursor: 'pointer',
                      opacity: selectedImage === image ? 1 : 0.7,
                      transition: 'opacity 0.2s',
                      '&:hover': { opacity: 1 }
                    }}
                    onClick={() => setSelectedImage(image)}
                  >
                    <img
                      src={image}
                      alt={`${event.name} ${index + 1}`}
                      loading="lazy"
                      style={{
                        height: '80px',
                        objectFit: 'cover',
                        borderRadius: theme.shape.borderRadius,
                      }}
                    />
                  </ImageListItem>
                ))}
              </ImageList>
            )}
          </Box>

          <Typography variant="h3" gutterBottom>
            {event.name}
          </Typography>

          <Box display="flex" gap={1} mb={2} flexWrap="wrap">
            <Chip label={event.category} color="primary" />
            {event.subcategory && (
              <Chip label={event.subcategory} color="secondary" />
            )}
            {event.tags?.map((tag, index) => (
              <Chip key={`${event.id}-tag-${index}`} label={tag} variant="outlined" />
            ))}
          </Box>

          <Box display="flex" alignItems="center" gap={2} mb={3}>
            <Rating value={event.rating} precision={0.5} readOnly />
            <Typography variant="body2" color="text.secondary">
              {event.rating} ({event.review_count} reviews)
            </Typography>
          </Box>

          <Typography variant="body1" paragraph>
            {event.long_description || event.description}
          </Typography>

          {event.amenities && event.amenities.length > 0 && (
            <Box mt={4}>
              <Typography variant="h6" gutterBottom>
                Amenities
              </Typography>
              <Box display="flex" gap={1} flexWrap="wrap">
                {event.amenities.map((amenity, index) => (
                  <Chip 
                    key={`${event.id}-amenity-${index}`} 
                    label={amenity} 
                    variant="outlined"
                    color="primary"
                  />
                ))}
              </Box>
            </Box>
          )}

          {event.health_safety_measures && event.health_safety_measures.length > 0 && (
            <Box mt={4}>
              <Typography variant="h6" gutterBottom>
                Health & Safety Measures
              </Typography>
              <List>
                {event.health_safety_measures.map((measure, index) => (
                  <ListItem key={`${event.id}-measure-${index}`}>
                    <ListItemIcon>
                      <CheckCircle color="success" />
                    </ListItemIcon>
                    <ListItemText primary={measure} />
                  </ListItem>
                ))}
              </List>
            </Box>
          )}
        </Grid>

        {/* Right Column - Booking and Details */}
        <Grid item xs={12} md={4}>
          <Paper sx={{ p: 3, mb: 3 }}>
            <Typography variant="h5" gutterBottom>
              Book Now
            </Typography>
            <Typography variant="h4" color="primary.main" gutterBottom>
              ${event.price_range_min}
              {event.price_range_max && event.price_range_max !== event.price_range_min && (
                <Typography component="span" variant="h6" color="text.secondary">
                  {' - '}${event.price_range_max}
                </Typography>
              )}
            </Typography>
            {bookingUrl ? (
              <Button
                variant="contained"
                color="primary"
                fullWidth
                size="large"
                href={bookingUrl}
                target="_blank"
                rel="noopener noreferrer"
                sx={{ mb: 2 }}
              >
                Get Tickets
              </Button>
            ) : (
              <Button
                variant="contained"
                color="primary"
                fullWidth
                size="large"
                disabled
                sx={{ mb: 2 }}
              >
                Currently Unavailable
              </Button>
            )}
            {event.cancellation_policy && (
              <Typography variant="body2" color="text.secondary">
                <Info sx={{ fontSize: 16, mr: 1, verticalAlign: 'middle' }} />
                {event.cancellation_policy}
              </Typography>
            )}
          </Paper>

          <Paper sx={{ p: 3, mb: 3 }}>
            <Typography variant="h6" gutterBottom>
              Event Details
            </Typography>
            {renderEventDetails()}
          </Paper>

          {event.latitude && event.longitude && (
            <Paper sx={{ p: 3, mb: 3 }}>
              <Typography variant="h6" gutterBottom>
                Location
              </Typography>
              <Box sx={{ height: 200, mb: 2 }}>
                <Map
                  latitude={event.latitude}
                  longitude={event.longitude}
                  zoom={15}
                  markers={[
                    {
                      latitude: event.latitude,
                      longitude: event.longitude,
                      title: event.venue?.name || event.name,
                    },
                  ]}
                />
              </Box>
              <Typography variant="body2">
                {event.venue?.name || event.name}
                <br />
                {event.address}
              </Typography>
            </Paper>
          )}
        </Grid>

        {/* Full Width Sections */}
        <Grid item xs={12}>
          <Divider sx={{ my: 4 }} />
          {renderAdditionalInfo()}
          <Divider sx={{ my: 4 }} />
          {renderReviews()}
        </Grid>
      </Grid>
    </Container>
  );
};

export default EventLanding; 