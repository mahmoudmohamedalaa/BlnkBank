import React, { useEffect, useState } from 'react';
import api from '../api';

const CustomerDashboard = () => {
    const [loans, setLoans] = useState([]);
    const [selectedLoanId, setSelectedLoanId] = useState(null);
    const [paymentAmount, setPaymentAmount] = useState('');
   



    useEffect(() => {
      getLoans();
  }, []);

  const getLoans = () => {
      api.get("/api/customer/dashboard/")
          .then((res) => res.data)
          .then((data) => {
              setLoans(data);
              console.log(data);
          })
        .catch((err) => {
            if(err.response.status === 403){
                alert("Acess Denied.");
                window.location.href = '/logout';
                }
          });
        };


  const handlePayment = (e) => {
    e.preventDefault();
    api
        .post("/api/customer/dashboard/", { loan_id: selectedLoanId, amount: parseInt(paymentAmount), transaction_date: new Date().toISOString().split('T')[0] })
        .then((res) => {
            if (res.status === 201) {alert("Payment successful!");
              setPaymentAmount('');
              setSelectedLoanId(null);}
            else alert("Payment Failed.");
            getLoans();
        })
        .catch((err) => alert(err));
};


    // Handle the payment submission
   
    return (
      <div className="container mt-5">
          <h1 className="text-center">Customer Dashboard</h1>
          <h2 className="text-center">Your Loans</h2>
          <ul className="list-group">
              {loans.map(loan => (
                  <li key={loan.loan_id} className="list-group-item d-flex justify-content-between align-items-center">
                      <span>
                      <ul class="list-group list-group-horizontal">
                      <li class="list-group-item">Loan ID: {loan.loan_id}</li>
                      <li class="list-group-item">Amount: {loan.amount}</li>
                      <li class="list-group-item">Status: {loan.status}</li>
                      

                      </ul>
                      </span>
                      
                      <button className="btn btn-primary" onClick={() => setSelectedLoanId(loan.loan_id)}>Make Payment</button>
                  </li>
              ))}
          </ul>

          {selectedLoanId && (
              <div className="mt-4">
                  <h3>Make a Payment</h3>
                  <input
                      type="number"
                      className="form-control mb-2"
                      placeholder="Payment Amount"
                      value={paymentAmount}
                      onChange={(e) => setPaymentAmount(e.target.value)}
                  />
                  
                  <button className="btn btn-success" onClick={handlePayment}>Submit Payment</button>
              </div>
          )}
      </div>
  );
};

export default CustomerDashboard;
