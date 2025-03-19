import React from 'react';
import { Box, Typography, Button, Container } from '@mui/material';
import TuneIcon from '@mui/icons-material/Tune';

const HERO_IMAGE = 'https://images.unsplash.com/photo-1581351721010-8cf859cb14a4?q=80&w=2000&auto=format&fit=crop';

const Hero: React.FC = () => {
  const scrollToExperiences = () => {
    const element = document.getElementById('experiences');
    element?.scrollIntoView({ behavior: 'smooth' });
  };

  return (
    <Box
      sx={{
        position: 'relative',
        height: '70vh',
        minHeight: '500px',
        display: 'flex',
        alignItems: 'center',
        '&::before': {
          content: '""',
          position: 'absolute',
          top: 0,
          left: 0,
          right: 0,
          bottom: 0,
          background: 'linear-gradient(to bottom, rgba(0,0,0,0.7) 0%, rgba(0,0,0,0.5) 100%)',
          zIndex: 1,
        },
        backgroundImage: `url(${HERO_IMAGE})`,
        backgroundSize: 'cover',
        backgroundPosition: 'center',
        backgroundAttachment: 'fixed',
      }}
    >
      <Container
        maxWidth="lg"
        sx={{
          position: 'relative',
          zIndex: 2,
          color: 'white',
          textAlign: 'center',
        }}
      >
        <Typography
          variant="h1"
          sx={{
            fontSize: { xs: '2.5rem', md: '4rem' },
            fontWeight: 700,
            mb: 2,
            textShadow: '2px 2px 4px rgba(0,0,0,0.5)',
            letterSpacing: '-0.02em',
          }}
        >
          Welcome to Las VAIgas
        </Typography>
        <Typography
          variant="h5"
          sx={{
            mb: 4,
            textShadow: '1px 1px 2px rgba(0,0,0,0.5)',
            maxWidth: '800px',
            mx: 'auto',
            fontSize: { xs: '1.1rem', md: '1.5rem' },
            fontWeight: 400,
            lineHeight: 1.4,
          }}
        >
          AI-Powered Recommendations for Your Perfect Vegas Experience
        </Typography>
        <Button
          variant="contained"
          size="large"
          startIcon={<TuneIcon />}
          onClick={scrollToExperiences}
          sx={{
            backgroundColor: 'primary.main',
            color: 'white',
            px: 4,
            py: 1.5,
            fontSize: '1.1rem',
            fontWeight: 500,
            borderRadius: '50px',
            textTransform: 'none',
            '&:hover': {
              backgroundColor: 'primary.dark',
              transform: 'translateY(-2px)',
              transition: 'all 0.2s ease-in-out',
            },
          }}
        >
          Customize Your Experience
        </Button>
      </Container>
    </Box>
  );
};

export default Hero; 