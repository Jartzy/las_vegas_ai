import React, { useState, useEffect } from 'react';
import { Deal } from '../../types/content';
import { contentService } from '../../services/contentService';
import {
  Card,
  CardContent,
  CardActions,
  Typography,
  Box,
  Button,
  Grid,
  Chip,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Alert
} from '@mui/material';
import { format } from 'date-fns';
import { LocalOffer, Casino, Attractions, Event } from '@mui/icons-material';

interface DealsProps {
  venue?: string;
  userId?: string;
}

export const Deals: React.FC<DealsProps> = ({ venue, userId }) => {
  const [deals, setDeals] = useState<Deal[]>([]);
  const [dealType, setDealType] = useState<string>('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    loadDeals();
  }, [venue, dealType]);

  const loadDeals = async () => {
    try {
      setLoading(true);
      setError(null);
      const response = await contentService.getDeals(venue, dealType);
      setDeals(response);
    } catch (error) {
      setError('Failed to load deals. Please try again later.');
      console.error('Error loading deals:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleSaveItem = async (deal: Deal) => {
    if (!userId) {
      alert('Please log in to save deals');
      return;
    }

    try {
      await contentService.saveItem({
        user_id: userId,
        item_type: 'deal',
        item_id: deal.id
      });
      alert('Deal saved successfully!');
    } catch (error) {
      console.error('Error saving deal:', error);
      alert('Failed to save deal. Please try again.');
    }
  };

  const getDealIcon = (type: string) => {
    switch (type) {
      case 'discount':
        return <LocalOffer />;
      case 'package':
        return <Attractions />;
      case 'special_offer':
        return <Event />;
      default:
        return <Casino />;
    }
  };

  const getDiscountText = (deal: Deal) => {
    if (deal.discount_type === 'percentage') {
      return `${deal.discount_amount}% off`;
    }
    return `$${deal.discount_amount} off`;
  };

  return (
    <Box sx={{ width: '100%', maxWidth: 1200, margin: '0 auto' }}>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 3 }}>
        <Typography variant="h5" component="h2">
          Special Deals & Offers
        </Typography>
        <FormControl size="small" sx={{ minWidth: 200 }}>
          <InputLabel>Deal Type</InputLabel>
          <Select
            value={dealType}
            label="Deal Type"
            onChange={(e) => setDealType(e.target.value)}
          >
            <MenuItem value="">All Deals</MenuItem>
            <MenuItem value="discount">Discounts</MenuItem>
            <MenuItem value="package">Packages</MenuItem>
            <MenuItem value="special_offer">Special Offers</MenuItem>
          </Select>
        </FormControl>
      </Box>

      {error && (
        <Alert severity="error" sx={{ mb: 2 }}>
          {error}
        </Alert>
      )}

      <Grid container spacing={3}>
        {deals.map((deal) => (
          <Grid item xs={12} sm={6} md={4} key={deal.id}>
            <Card sx={{ height: '100%', display: 'flex', flexDirection: 'column' }}>
              <CardContent sx={{ flexGrow: 1 }}>
                <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                  {getDealIcon(deal.deal_type)}
                  <Typography variant="h6" sx={{ ml: 1 }}>
                    {deal.title}
                  </Typography>
                </Box>
                <Typography variant="body2" color="text.secondary" paragraph>
                  {deal.description}
                </Typography>
                <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1, mb: 2 }}>
                  <Chip
                    label={getDiscountText(deal)}
                    color="primary"
                    size="small"
                  />
                  <Chip
                    label={deal.venue}
                    variant="outlined"
                    size="small"
                  />
                  {deal.promo_code && (
                    <Chip
                      label={`Code: ${deal.promo_code}`}
                      color="secondary"
                      size="small"
                    />
                  )}
                </Box>
                {deal.end_date && (
                  <Typography variant="body2" color="error">
                    Expires: {format(new Date(deal.end_date), 'MMM d, yyyy')}
                  </Typography>
                )}
              </CardContent>
              <CardActions sx={{ justifyContent: 'space-between', p: 2 }}>
                <Button
                  size="small"
                  variant="outlined"
                  onClick={() => handleSaveItem(deal)}
                >
                  Save Deal
                </Button>
                <Button
                  size="small"
                  variant="contained"
                  href={deal.affiliate_link}
                  target="_blank"
                  rel="noopener noreferrer"
                >
                  Get Deal
                </Button>
              </CardActions>
            </Card>
          </Grid>
        ))}
      </Grid>

      {loading && (
        <Box sx={{ textAlign: 'center', my: 4 }}>
          <Typography>Loading deals...</Typography>
        </Box>
      )}

      {!loading && deals.length === 0 && (
        <Box sx={{ textAlign: 'center', my: 4 }}>
          <Typography>No active deals found.</Typography>
        </Box>
      )}
    </Box>
  );
}; 