import React, { useState } from 'react';
import { Box, Container, Tabs, Tab, Typography, Paper } from '@mui/material';
import { Reviews } from './content/Reviews';
import { Deals } from './content/Deals';
import { LocalGuides } from './content/LocalGuides';

interface TabPanelProps {
  children?: React.ReactNode;
  index: number;
  value: number;
}

function TabPanel(props: TabPanelProps) {
  const { children, value, index, ...other } = props;

  return (
    <div
      role="tabpanel"
      hidden={value !== index}
      id={`content-tabpanel-${index}`}
      aria-labelledby={`content-tab-${index}`}
      {...other}
    >
      {value === index && (
        <Box sx={{ p: 3 }}>
          {children}
        </Box>
      )}
    </div>
  );
}

export const ContentShowcase: React.FC = () => {
  const [tabValue, setTabValue] = useState(0);
  const [userId] = useState('test-user-id'); // In a real app, this would come from authentication

  const handleTabChange = (event: React.SyntheticEvent, newValue: number) => {
    setTabValue(newValue);
  };

  return (
    <Container maxWidth="xl">
      <Box sx={{ my: 4 }}>
        <Typography variant="h3" component="h1" gutterBottom align="center">
          Las Vegas Activities & Experiences
        </Typography>
        <Typography variant="h6" component="h2" gutterBottom align="center" color="text.secondary">
          Discover the best of Las Vegas with our curated content
        </Typography>
      </Box>

      <Paper sx={{ width: '100%', mb: 4 }}>
        <Tabs
          value={tabValue}
          onChange={handleTabChange}
          indicatorColor="primary"
          textColor="primary"
          variant="fullWidth"
        >
          <Tab label="Local Guides" />
          <Tab label="Deals & Offers" />
          <Tab label="Reviews" />
        </Tabs>

        <TabPanel value={tabValue} index={0}>
          <LocalGuides initialCategory="entertainment" />
        </TabPanel>
        
        <TabPanel value={tabValue} index={1}>
          <Deals userId={userId} />
        </TabPanel>
        
        <TabPanel value={tabValue} index={2}>
          <Reviews itemType="event" itemId={1} userId={userId} />
        </TabPanel>
      </Paper>
    </Container>
  );
}; 