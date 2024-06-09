import React, { useEffect, useState } from 'react';
import { useQuery } from '@apollo/client';
import { Box, Typography, Alert } from '@mui/material';
import { useAuth } from '../authProvider';
import { DASHBOARD_QUERY } from '../graphql/queries';
import Button from '@mui/material/Button';
import { useNavigate } from 'react-router-dom';
import Dashboard from '../layouts/dashboard';
import { environment } from "../environment";

function DashboardPage() {
  // @ts-ignore
  const { token, logout } = useAuth();
  const navigate = useNavigate();

  const [personalSignInCount, setPersonalSignInCount] = useState(0);
  const [globalSignInCount, setGlobalSignInCount] = useState(0);
  const [alertMessage, setAlertMessage] = useState('');

  const { data } = useQuery(DASHBOARD_QUERY, {
    context: {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    },
  });

  useEffect(() => {
    if (data) {
      setPersonalSignInCount(data.personalSignInCount);
      setGlobalSignInCount(data.globalSignInCount);
    }
  }, [data]);

  useEffect(() => {
    if (!token) return;

    const ws = new WebSocket(environment.wsApiUrl);

    ws.onopen = () => {
      console.log('WebSocket connection opened');
      ws.send(JSON.stringify({ type: 'authenticate', token }));
    };

    ws.onmessage = (event) => {
      console.log('WebSocket message received:', event.data);
      const message = JSON.parse(event.data);
      if (message.type === 'update' && message.globalSignInCount !== undefined) {
        setGlobalSignInCount(message.globalSignInCount);
      } else if (message.type === 'personalUpdate' && message.personalSignInCount !== undefined) {
        setPersonalSignInCount(message.personalSignInCount);
      } else if (message.type === 'initial') {
        setGlobalSignInCount(message.globalSignInCount);
        setPersonalSignInCount(message.personalSignInCount);
      } else if (message.message) {
        setAlertMessage(message.message);
      }
    };

    ws.onerror = (error) => {
      console.error('WebSocket error:', error);
    };

    ws.onclose = (event) => {
      console.log('WebSocket connection closed:', event);
    };

    return () => {
      ws.close();
    };
  }, [token]);

  const handleLogout = () => {
    logout();
    navigate('/signin');
  };

  return (
    <Dashboard title="Welcome to Dashboard!">
      <Button
        variant="outlined"
        onClick={handleLogout}
        sx={{ position: 'absolute', top: 16, right: 16 }}
      >
        Log out
      </Button>
      <Typography variant="h6" gutterBottom align="center">
        You've signed in {personalSignInCount} times!
      </Typography>
      <Typography variant="h6" gutterBottom align="center">
        Everyone has signed in {globalSignInCount} times!
      </Typography>
      {alertMessage && (
        <Box sx={{ mt: 2 }}>
          <Alert severity="success">{alertMessage}</Alert>
        </Box>
      )}
      <Box sx={{ mt: 2, display: 'flex', justifyContent: 'space-between' }}>
      </Box>
    </Dashboard>
  );
}

export default DashboardPage;
