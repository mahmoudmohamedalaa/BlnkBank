import React, { useEffect, useState } from 'react';
import api from '../api';
import { Container, ListGroup, ListGroupItem } from 'react-bootstrap';

const BankPersonnelDashboard = () => {
    const [loanFundApplications, setLoanFundApplications] = useState([]);
    const [loans, setLoans] = useState([]);



    useEffect(() => {
      getApplications();
  }, []);

  const getApplications = () => {
      api.get("/api/bank-personnel/dashboard/")
          .then((res) => res.data)
          .then((data) => {
            setLoanFundApplications(data.loan_fund_applications);
            setLoans(data.loans);
              console.log(data);
          })
          .catch((err) => {
            if(err.response.status === 403){
                alert("Acess Denied.");
                window.location.href = '/logout';
                }
          });
        };


  const getStatusClass = (status) => {
    switch (status) {
        case 'Approved':
            return 'bg-success text-white';
        case 'Pending':
            return 'bg-warning text-dark';
        case 'Rejected':
            return 'bg-danger text-white';
        default:
            return '';
    }
};

return (
    <Container className="mt-5">
        <h1 className="text-center">Bank Personnel Dashboard</h1>

        <h2 className="text-center mb-4">Loan Fund Applications</h2>
        <ListGroup>
            {loanFundApplications.map(application => (
                <ListGroupItem key={application.application_id} className="mb-3">
                    <ul className="list-group list-group-horizontal mx-auto justify-content-between">
                        <li className="list-group-item">Application ID: {application.application_id}</li>
                        <li className="list-group-item">Amount: {application.amount}</li>
                        <li className={`list-group-item ${getStatusClass(application.status)}`}>
                            Status: {application.status}
                        </li>
                    </ul>
                </ListGroupItem>
            ))}
        </ListGroup>

        <h2 className="text-center mt-5 mb-4">Loans</h2>
        <ListGroup>
            {loans.map(loan => (
                <ListGroupItem key={loan.loan_id} className="mb-3">
                    <ul className="list-group list-group-horizontal mx-auto justify-content-between">
                        <li className="list-group-item">Loan ID: {loan.loan_id}</li>
                        <li className="list-group-item">Amount: {loan.amount}</li>
                        <li className={`list-group-item ${getStatusClass(loan.status)}`}>
                            Status: {loan.status}
                        </li>
                    </ul>
                </ListGroupItem>
            ))}
        </ListGroup>
    </Container>
);
};

export default BankPersonnelDashboard;
