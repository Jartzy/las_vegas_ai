import React, { useState, useEffect } from 'react';
import { Review, ReviewResponse, ContentFilters } from '../../types/content';
import { contentService } from '../../services/contentService';
import { Rating, Card, CardContent, Typography, Box, Button, TextField, Dialog, 
         DialogTitle, DialogContent, DialogActions, Select, MenuItem, FormControl, 
         InputLabel } from '@mui/material';
import { format } from 'date-fns';

interface ReviewsProps {
  itemType: 'event' | 'casino' | 'outdoor_activity';
  itemId: number;
  userId?: string;
}

export const Reviews: React.FC<ReviewsProps> = ({ itemType, itemId, userId }) => {
  const [reviews, setReviews] = useState<Review[]>([]);
  const [totalReviews, setTotalReviews] = useState(0);
  const [currentPage, setCurrentPage] = useState(1);
  const [filters, setFilters] = useState<ContentFilters>({
    sort: 'newest',
    page: 1,
    per_page: 5
  });
  const [isDialogOpen, setIsDialogOpen] = useState(false);
  const [newReview, setNewReview] = useState({
    rating: 5,
    title: '',
    content: '',
    photos: [] as string[]
  });

  useEffect(() => {
    loadReviews();
  }, [itemType, itemId, filters]);

  const loadReviews = async () => {
    try {
      const response = await contentService.getReviews(itemType, itemId, filters) as ReviewResponse;
      setReviews(response.reviews);
      setTotalReviews(response.total);
      setCurrentPage(response.current_page);
    } catch (error) {
      console.error('Error loading reviews:', error);
    }
  };

  const handleCreateReview = async () => {
    try {
      if (!userId) {
        alert('Please log in to submit a review');
        return;
      }

      await contentService.createReview({
        ...newReview,
        user_id: userId,
        [itemType === 'event' ? 'event_id' : 
         itemType === 'casino' ? 'casino_id' : 'outdoor_activity_id']: itemId
      });

      setIsDialogOpen(false);
      setNewReview({ rating: 5, title: '', content: '', photos: [] });
      loadReviews();
    } catch (error) {
      console.error('Error creating review:', error);
    }
  };

  const handleSortChange = (event: any) => {
    setFilters({ ...filters, sort: event.target.value, page: 1 });
  };

  const handlePageChange = (newPage: number) => {
    setFilters({ ...filters, page: newPage });
  };

  return (
    <Box sx={{ width: '100%', maxWidth: 800, margin: '0 auto' }}>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 2 }}>
        <Typography variant="h5" component="h2">
          Reviews ({totalReviews})
        </Typography>
        <Box sx={{ display: 'flex', gap: 2 }}>
          <FormControl size="small">
            <InputLabel>Sort By</InputLabel>
            <Select
              value={filters.sort}
              label="Sort By"
              onChange={handleSortChange}
              sx={{ minWidth: 150 }}
            >
              <MenuItem value="newest">Newest First</MenuItem>
              <MenuItem value="highest_rated">Highest Rated</MenuItem>
              <MenuItem value="most_helpful">Most Helpful</MenuItem>
            </Select>
          </FormControl>
          <Button
            variant="contained"
            color="primary"
            onClick={() => setIsDialogOpen(true)}
          >
            Write Review
          </Button>
        </Box>
      </Box>

      {reviews.map((review) => (
        <Card key={review.id} sx={{ mb: 2 }}>
          <CardContent>
            <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 1 }}>
              <Rating value={review.rating} readOnly />
              <Typography variant="body2" color="text.secondary">
                {format(new Date(review.created_at), 'MMM d, yyyy')}
              </Typography>
            </Box>
            <Typography variant="h6" gutterBottom>
              {review.title}
            </Typography>
            <Typography variant="body1" paragraph>
              {review.content}
            </Typography>
            {review.photos.length > 0 && (
              <Box sx={{ display: 'flex', gap: 1, mt: 2 }}>
                {review.photos.map((photo, index) => (
                  <img
                    key={index}
                    src={photo}
                    alt={`Review photo ${index + 1}`}
                    style={{ width: 100, height: 100, objectFit: 'cover' }}
                  />
                ))}
              </Box>
            )}
            <Box sx={{ display: 'flex', alignItems: 'center', mt: 2 }}>
              <Typography variant="body2" color="text.secondary">
                {review.helpful_votes} people found this helpful
              </Typography>
              {review.verified_purchase && (
                <Typography
                  variant="body2"
                  color="success.main"
                  sx={{ ml: 2 }}
                >
                  Verified Purchase
                </Typography>
              )}
            </Box>
          </CardContent>
        </Card>
      ))}

      {totalReviews > filters.per_page! && (
        <Box sx={{ display: 'flex', justifyContent: 'center', mt: 2 }}>
          <Button
            disabled={currentPage === 1}
            onClick={() => handlePageChange(currentPage - 1)}
          >
            Previous
          </Button>
          <Typography sx={{ mx: 2 }}>
            Page {currentPage} of {Math.ceil(totalReviews / filters.per_page!)}
          </Typography>
          <Button
            disabled={currentPage === Math.ceil(totalReviews / filters.per_page!)}
            onClick={() => handlePageChange(currentPage + 1)}
          >
            Next
          </Button>
        </Box>
      )}

      <Dialog open={isDialogOpen} onClose={() => setIsDialogOpen(false)} maxWidth="md" fullWidth>
        <DialogTitle>Write a Review</DialogTitle>
        <DialogContent>
          <Box sx={{ mt: 2 }}>
            <Box sx={{ mb: 2 }}>
              <Typography component="legend">Rating</Typography>
              <Rating
                value={newReview.rating}
                onChange={(_, value) => setNewReview({ ...newReview, rating: value || 5 })}
              />
            </Box>
            <TextField
              fullWidth
              label="Title"
              value={newReview.title}
              onChange={(e) => setNewReview({ ...newReview, title: e.target.value })}
              sx={{ mb: 2 }}
            />
            <TextField
              fullWidth
              multiline
              rows={4}
              label="Review"
              value={newReview.content}
              onChange={(e) => setNewReview({ ...newReview, content: e.target.value })}
            />
          </Box>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setIsDialogOpen(false)}>Cancel</Button>
          <Button
            onClick={handleCreateReview}
            variant="contained"
            disabled={!newReview.title || !newReview.content}
          >
            Submit Review
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
}; 