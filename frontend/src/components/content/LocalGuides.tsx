import React, { useState, useEffect } from 'react';
import { LocalGuide, ContentFilters, GuideResponse } from '../../types/content';
import { contentService } from '../../services/contentService';
import {
  Card,
  CardContent,
  CardMedia,
  Typography,
  Box,
  Grid,
  Chip,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Pagination,
  Alert,
  IconButton
} from '@mui/material';
import {
  Visibility as VisibilityIcon,
  Favorite as FavoriteIcon,
  LocalActivity,
  Casino,
  Hiking,
  Restaurant,
  Nightlife
} from '@mui/icons-material';
import { format } from 'date-fns';

interface LocalGuidesProps {
  initialCategory?: string;
}

interface GuideCategory {
  value: string;
  label: string;
  icon: React.ReactNode;
}

const CATEGORIES: GuideCategory[] = [
  { value: 'entertainment', label: 'Entertainment', icon: <LocalActivity /> },
  { value: 'casinos', label: 'Casinos', icon: <Casino /> },
  { value: 'outdoor', label: 'Outdoor Activities', icon: <Hiking /> },
  { value: 'dining', label: 'Dining', icon: <Restaurant /> },
  { value: 'nightlife', label: 'Nightlife', icon: <Nightlife /> }
];

export const LocalGuides: React.FC<LocalGuidesProps> = ({ initialCategory }) => {
  const [guides, setGuides] = useState<LocalGuide[]>([]);
  const [totalGuides, setTotalGuides] = useState(0);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [filters, setFilters] = useState<ContentFilters>({
    category: initialCategory || '',
    sort: 'popular',
    page: 1,
    per_page: 9
  });

  useEffect(() => {
    loadGuides();
  }, [filters]);

  const loadGuides = async () => {
    try {
      setLoading(true);
      setError(null);
      const response = await contentService.getGuides(filters) as GuideResponse;
      setGuides(response.guides);
      setTotalGuides(response.total);
    } catch (error) {
      setError('Failed to load guides. Please try again later.');
      console.error('Error loading guides:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleCategoryChange = (event: any) => {
    setFilters({ ...filters, category: event.target.value, page: 1 });
  };

  const handleSortChange = (event: any) => {
    setFilters({ ...filters, sort: event.target.value, page: 1 });
  };

  const handlePageChange = (event: any, value: number) => {
    setFilters({ ...filters, page: value });
  };

  const getCategoryIcon = (category: string) => {
    const found = CATEGORIES.find(cat => cat.value === category);
    return found ? found.icon : <LocalActivity />;
  };

  return (
    <Box sx={{ width: '100%', maxWidth: 1200, margin: '0 auto' }}>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 3 }}>
        <Typography variant="h5" component="h2">
          Local Guides & Tips
        </Typography>
        <Box sx={{ display: 'flex', gap: 2 }}>
          <FormControl size="small" sx={{ minWidth: 200 }}>
            <InputLabel>Category</InputLabel>
            <Select
              value={filters.category}
              label="Category"
              onChange={handleCategoryChange}
            >
              <MenuItem value="">All Categories</MenuItem>
              {CATEGORIES.map((category) => (
                <MenuItem key={category.value} value={category.value}>
                  <Box sx={{ display: 'flex', alignItems: 'center' }}>
                    {category.icon}
                    <Typography sx={{ ml: 1 }}>{category.label}</Typography>
                  </Box>
                </MenuItem>
              ))}
            </Select>
          </FormControl>
          <FormControl size="small" sx={{ minWidth: 150 }}>
            <InputLabel>Sort By</InputLabel>
            <Select
              value={filters.sort}
              label="Sort By"
              onChange={handleSortChange}
            >
              <MenuItem value="popular">Most Popular</MenuItem>
              <MenuItem value="newest">Newest First</MenuItem>
            </Select>
          </FormControl>
        </Box>
      </Box>

      {error && (
        <Alert severity="error" sx={{ mb: 2 }}>
          {error}
        </Alert>
      )}

      <Grid container spacing={3}>
        {guides.map((guide) => (
          <Grid item xs={12} sm={6} md={4} key={guide.id}>
            <Card sx={{ height: '100%', display: 'flex', flexDirection: 'column' }}>
              <CardMedia
                component="img"
                height="200"
                image={guide.featured_image}
                alt={guide.title}
              />
              <CardContent sx={{ flexGrow: 1 }}>
                <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                  {getCategoryIcon(guide.category)}
                  <Typography variant="h6" sx={{ ml: 1 }}>
                    {guide.title}
                  </Typography>
                </Box>
                <Typography variant="body2" color="text.secondary" paragraph>
                  {guide.content.substring(0, 150)}...
                </Typography>
                <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1, mb: 2 }}>
                  {guide.tags.map((tag, index) => (
                    <Chip
                      key={index}
                      label={tag}
                      size="small"
                      variant="outlined"
                    />
                  ))}
                </Box>
                <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                  <Box sx={{ display: 'flex', alignItems: 'center' }}>
                    <IconButton size="small">
                      <VisibilityIcon fontSize="small" />
                    </IconButton>
                    <Typography variant="body2" sx={{ ml: 0.5 }}>
                      {guide.views}
                    </Typography>
                    <IconButton size="small" sx={{ ml: 1 }}>
                      <FavoriteIcon fontSize="small" />
                    </IconButton>
                    <Typography variant="body2" sx={{ ml: 0.5 }}>
                      {guide.likes}
                    </Typography>
                  </Box>
                  <Typography variant="caption" color="text.secondary">
                    {format(new Date(guide.created_at), 'MMM d, yyyy')}
                  </Typography>
                </Box>
              </CardContent>
            </Card>
          </Grid>
        ))}
      </Grid>

      {loading && (
        <Box sx={{ textAlign: 'center', my: 4 }}>
          <Typography>Loading guides...</Typography>
        </Box>
      )}

      {!loading && guides.length === 0 && (
        <Box sx={{ textAlign: 'center', my: 4 }}>
          <Typography>No guides found for the selected category.</Typography>
        </Box>
      )}

      {totalGuides > filters.per_page! && (
        <Box sx={{ display: 'flex', justifyContent: 'center', mt: 4 }}>
          <Pagination
            count={Math.ceil(totalGuides / filters.per_page!)}
            page={filters.page!}
            onChange={handlePageChange}
            color="primary"
          />
        </Box>
      )}
    </Box>
  );
}; 