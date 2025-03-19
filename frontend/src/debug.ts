// Simple debug file to check if imports are working
import React from 'react';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import { Box } from '@mui/material';

// Log to confirm imports are working
console.log('Debug file loaded');
console.log('React version:', React.version);
console.log('MUI imports working:', !!ThemeProvider && !!createTheme && !!CssBaseline && !!Box);

// Export something to make TypeScript happy
export const debug = { loaded: true }; 