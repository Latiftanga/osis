import React, {useState, useEffect} from 'react';
import auth from './services/authService';
import AdminLayout from './layouts/AdminLayout';
import './App.css';

const App = () => {

  const [user, setUser] = useState();
  
  useEffect(() => {
    const currentUser = auth.getUser();
    setUser(currentUser);
  }, []);

  return (
      <AdminLayout user={user}></AdminLayout>
  )
};
export default App;