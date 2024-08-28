import React, { useState,useEffect } from 'react';
import api from '../api';
import { Container, ListGroup, ListGroupItem } from 'react-bootstrap';


const LoanProviderDashboard = () => {
    const [applications, setApplications] = useState([]);

    useEffect(() => {
        getApplications();
    }, []);

    const getApplications = () => {
        api.get("/api/loan-provider/dashboard/")
            .then((res) => res.data)
            .then((data) => {
                setApplications(data);
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
        switch (status.toLowerCase()) {
            case 'approved':
                return 'bg-success text-white';  // Green background for accepted
            case 'pending':
                return 'bg-warning text-dark';   // Yellow background for pending
            case 'rejected':
                return 'bg-danger text-white';   // Red background for rejected
            default:
                return 'bg-secondary text-white';  // Default background
        }
    };

    return (
        <Container className="mt-5">
            <h1 className="text-center">Loan Provider Dashboard</h1>
            <h2 className="text-center mb-4">Your Loan Fund Applications</h2>
            <ListGroup>
                {applications.map(application => (
                    <ListGroupItem key={application.application_id} className="mb-3">
                        <ul className="list-group list-group-horizontal mx-auto justify-content-between">
                            <li className="list-group-item">Amount: {application.amount}</li>
                            <li className={`list-group-item ${getStatusClass(application.status)}`}>
                                Status: {application.status}
                            </li>
                        </ul>
                    </ListGroupItem>
                ))}
            </ListGroup>
        </Container>
    );
};

export default LoanProviderDashboard;