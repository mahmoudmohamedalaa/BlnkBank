import React, {useState} from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../api';
import { ACCESS_TOKEN ,REFRESH_TOKEN} from '../constants';
import "../styles/form.css"

function Login() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);
  
  
  const Navigate = useNavigate();
  const handleSubmit= async (e) => {
    e.preventDefault();
    setLoading(true);

    try{
      const response = await api.post('/api/token/', {username, password});
      localStorage.setItem(ACCESS_TOKEN, response.data.access);
      localStorage.setItem(REFRESH_TOKEN, response.data.refresh);
      const userResponse = await api.post('/login/', {username, password});
      
      Navigate(userResponse.data.redirect_url);
    
  }catch (error) {
    //alert('An error occurred. Please try again');
    alert(error);
  }
  finally {
    setLoading(false);
  }
};
  return (
    <div>
     
      <form onSubmit={handleSubmit} className="form-container">
      <h1>Login</h1>
        <input  className="form-input" type="text" placeholder="Username" value={username} onChange={(e)=> setUsername(e.target.value)} />
        <input  className="form-input" type="password" placeholder="Password" value={password} onChange={(e)=> setPassword(e.target.value)} />
        <button className="form-button" type="submit">Login</button>
      </form>
    </div>
  );
}

export default Login;