import React, {useState} from 'react';
import Button from '@mui/material/Button';
import Auth from "../layouts/auth";
import {Box, Grid, TextField} from '@mui/material';
import Link from '@mui/material/Link';
import {LOGIN_MUTATION} from "../graphql/mutations";
import {useMutation} from "@apollo/client";
import {useAuth} from "../provider/authProvider";
import {useNavigate} from "react-router-dom";

function SignIn() {
    //@ts-ignore
    const { setToken } = useAuth();
    const navigate = useNavigate();

  const [formState, setFormState]: any = useState({})

  const [login] = useMutation(LOGIN_MUTATION, {
      variables: {
          input: {
            email: formState.email,
            password: formState.password
          }
      },
      onCompleted: ({ login }) => {
        setToken(login.accessToken);
        navigate('/dashboard');
      }
    });

  const handleSubmit = (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    const data = new FormData(event.currentTarget);
    const email = data.get('email');
    const password = data.get('password');

    setFormState({
        email, password
    })

      login()
  };

  return (
        <Auth title="Sign In">
            <Box component="form" onSubmit={handleSubmit} noValidate sx={{ mt: 1 }}>
                <TextField
                  margin="normal"
                  required
                  fullWidth
                  id="email"
                  label="Email Address"
                  name="email"
                  autoComplete="email"
                  autoFocus
                  onChange={e => {
                      setFormState((prevState: any) => ({
                          ...prevState,
                          email: e.target.value
                      }))
                  }}
                />
                <TextField
                  margin="normal"
                  required
                  fullWidth
                  id="password"
                  label="Password"
                  type="password"
                  name="password"
                  onChange={p => {
                      setFormState((prevState: any) => ({
                          ...prevState,
                          password: p.target.value
                      }))
                  }}
                />
                <Button
                  type="submit"
                  fullWidth
                  variant="contained"
                  sx={{ mt: 3, mb: 2 }}
                >
                  Sign In
                </Button>
                <Grid container justifyContent="flex-end">
                  <Grid item>
                    <Link href="/register" variant="body2">
                      Don't have an account? Register
                    </Link>
                  </Grid>
                </Grid>
            </Box>
        </Auth>
  );
}

export default SignIn;
