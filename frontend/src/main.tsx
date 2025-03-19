import React from 'react'
import ReactDOM from 'react-dom/client'
// Import both apps
import App from './App'
import SimpleApp from './SimpleApp'
import './index.css'
// Import debug file to check for issues
import './debug';

// Add a simple error boundary
const renderApp = () => {
  try {
    // Try to render the full app first
    ReactDOM.createRoot(document.getElementById('root')!).render(
      <React.StrictMode>
        <App />
      </React.StrictMode>,
    )
  } catch (error) {
    console.error('Error rendering full app:', error);
    
    // If the full app fails, try to render the simple app
    try {
      ReactDOM.createRoot(document.getElementById('root')!).render(
        <React.StrictMode>
          <SimpleApp />
        </React.StrictMode>,
      )
    } catch (simpleError) {
      console.error('Error rendering simple app:', simpleError);
      
      // If both fail, render a fallback UI
      const rootElement = document.getElementById('root');
      if (rootElement) {
        rootElement.innerHTML = `
          <div style="padding: 20px; color: red;">
            <h2>Something went wrong</h2>
            <p>There was an error loading the application. Please check the console for details.</p>
            <pre>${error instanceof Error ? error.message : String(error)}</pre>
          </div>
        `;
      }
    }
  }
};

renderApp();