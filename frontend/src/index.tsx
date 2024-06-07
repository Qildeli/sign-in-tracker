import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import SignIn from './pages/SignIn';
import reportWebVitals from './reportWebVitals';
import {createBrowserRouter, Navigate, Outlet, RouterProvider} from "react-router-dom";
import {ApolloProvider} from "@apollo/client";
import {client} from "./graphql/client";
import Register from "./pages/Register";
import AuthProvider, {useAuth} from "./authProvider";
import DashboardPage from "./pages/Dashboard";

const root = ReactDOM.createRoot(
  document.getElementById('root') as HTMLElement
);

const ProtectedRoute = () => {
  // @ts-ignore
  const { token } = useAuth();

  // Check if the user is authenticated
  if (!token) {
    // If not authenticated, redirect to the login page
    return <Navigate to="/signin" />;
  }

  // If authenticated, render the child routes
  return <Outlet />;
};

const Routes = () => {

  // Public routes accessible to all users
  const routesForPublic = [
    {
      path: "/signin",
      element: <SignIn/>,
    },
    {
      path: "/register",
      element: <Register/>,
    },
  ];

  // Routes accessible only to authenticated users
  const routesForAuthenticatedOnly = [
    {
      path: "/",
      element: <ProtectedRoute/>,
      children: [
        {
          path: "/dashboard",
          element: <DashboardPage/>,
        },
      ],
    },
  ];


  const router = createBrowserRouter([
    ...routesForPublic,
    ...routesForAuthenticatedOnly,
  ]);

    return <RouterProvider router={router} />;
};


root.render(
  <React.StrictMode>
      <ApolloProvider client={client}>
        <AuthProvider>
          <Routes />
        </AuthProvider>
      </ApolloProvider>
  </React.StrictMode>
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
