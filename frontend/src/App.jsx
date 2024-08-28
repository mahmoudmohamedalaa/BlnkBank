import React from 'react'
import { BrowserRouter, Routes, Route,Navigate} from 'react-router-dom'
import Login from './pages/Login'
import Register from './pages/Register' 
import CustomerDashboard from './pages/CustomerDashboard'
import LoanProviderDashboard from './pages/LoanProviderDashboard'
import BankerDashboard from './pages/BankerDashboard'
import ProtectedRoute from './components/ProtectedRoute'
import NotFound from './pages/NotFound' 
import 'bootstrap/dist/css/bootstrap.min.css';


function LogOut() {
  localStorage.clear()
  return <Navigate to= "/login" />
}

function RegisterandLogout() {
  localStorage.clear()
  return <Navigate to= "/register" />
}

function App() {
  return (
    
      <Routes>
        <Route path="" element={<Login />} />
        <Route path="/login" element={<Login />} />
        <Route path="/api/user/register" element={<Register />} />
        <Route path="/logout" element={<LogOut />} />
        <Route path="/registerandlogout" element={<RegisterandLogout />} />
        <Route path="/api/customer/dashboard/" element={
          <ProtectedRoute>
            <CustomerDashboard/>
          </ProtectedRoute>
          
          } 
          />
           
          
        <Route path="/api/loan-provider/dashboard/"element={
          <ProtectedRoute>
          
            <LoanProviderDashboard/>
          </ProtectedRoute>
         
          }  />
        <Route path="/api/bank-personnel/dashboard/" element={
          
            <BankerDashboard/>
         
          }  /> 
        <Route path="*" element={<NotFound />} />
      </Routes>
   
  )
}

export default App
