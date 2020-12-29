import React, { useState, useEffect, useContext, createContext } from "react";
import http from './httpService';
import { API_URL } from '../config.json';
import jwt_decode from 'jwt-decode';

const endpoint = `${API_URL}auth-token/`;
const authContext = createContext();

// Provider component that wraps your app and makes auth object ...
// ... available to any child component that calls useAuth().
export function ProvideAuth({ children }) {
  const auth = useProvideAuth();
  return <authContext.Provider value={auth}>{children}</authContext.Provider>;
}

// Hook for child components to get the auth object ...
// ... and re-render when it changes.
export const useAuth = () => {
  return useContext(authContext);
};

// Provider hook that creates auth object and handles state
function useProvideAuth() {
  const [user, setUser] = useState(null);
  
  // Wrap any Firebase methods we want to use making sure ...
  // ... to save the user to state.
  const signin = async credentials => {
    try {
        const { data } = await http.post(endpoint, credentials);
        localStorage.setItem('token', data.token);
        const loginUser = jwt_decode(data.token)
        setUser(loginUser);
        return loginUser;
    } catch (error) {
       return null; 
    }
  };

  const signout = async () => {
      localStorage.removeItem('token');
      setUser(false);
  }

  const getUser = () => jwt_decode(localStorage.getItem('token')) || false
  // Subscribe to user on mount
  // Because this sets state in the callback it will cause any ...
  // ... component that utilizes this hook to re-render with the ...
  // ... latest auth object.
  useEffect(() => {
    const usr = getUser();
    if(usr) setUser(usr);
  }, []);
  
  // Return the user object and auth methods
  return {
    user,
    signin,
    signup,
    signout,
  };
}