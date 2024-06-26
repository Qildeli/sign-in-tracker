import { createContext, useContext, useEffect, useMemo, useState } from "react";

// @ts-ignore
const AuthContext = createContext();

const AuthProvider = ({ children }: { children: React.ReactElement }) => {
  // State to hold the authentication token
  const [token, setToken_] = useState(localStorage.getItem("token"));

  // Function to set the authentication token
  const setToken = (newToken: string) => {
    setToken_(newToken);
  };

  // Function to log out the user
  const logout = () => {
    setToken_('');
    localStorage.removeItem('token');
  };

  useEffect(() => {
    if (token) {
      localStorage.setItem("token", token);
    } else {
      localStorage.removeItem("token");
    }
  }, [token]);

  // Memoized value of the authentication context
  const contextValue = useMemo(
    () => ({
      token,
      setToken,
      logout,
    }),
    [token]
  );

  // Provide the authentication context to the children components
  return (
    <AuthContext.Provider value={contextValue}>{children}</AuthContext.Provider>
  );
};

export const useAuth = () => {
  return useContext(AuthContext);
};

export default AuthProvider;
