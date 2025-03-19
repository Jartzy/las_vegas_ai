import React from 'react';
import { AppBar, Toolbar, Typography, Button, Box, Container } from '@mui/material';
import { Casino, LocalActivity, Restaurant, Hiking, Nightlife } from '@mui/icons-material';

export const Navbar: React.FC = () => {
  return (
    <AppBar position="static">
      <Container maxWidth="xl">
        <Toolbar>
          <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
            Las Vegas AI
          </Typography>
          <Box sx={{ display: 'flex', gap: 2 }}>
            <Button color="inherit" startIcon={<Casino />}>
              Casinos
            </Button>
            <Button color="inherit" startIcon={<LocalActivity />}>
              Shows
            </Button>
            <Button color="inherit" startIcon={<Restaurant />}>
              Dining
            </Button>
            <Button color="inherit" startIcon={<Hiking />}>
              Outdoor
            </Button>
            <Button color="inherit" startIcon={<Nightlife />}>
              Nightlife
            </Button>
          </Box>
        </Toolbar>
      </Container>
    </AppBar>
  );
}; 