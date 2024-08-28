import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../api";
import { ACCESS_TOKEN, REFRESH_TOKEN } from "../constants";
import "../styles/form.css"


function Register() {
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const [first_name, setFirstName] = useState("");
    const [last_name, setLastName] = useState("");
    const [email, setEmail] = useState("");
    const [phone_number, setPhoneNumber] = useState("");
    const [role, setRole] = useState("");
    const [date_of_birth, setDate_of_birth] = useState("");
    const [address, setAddress] = useState("");
    const Navigate = useNavigate();
    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            const response = await api.post("api/user/register/", {
                first_name,
                last_name,
                username,
                email,
                role,
                date_of_birth,
                address,
                phone_number,
                password,
            });
            
            Navigate("/login");
        } catch (error) {
            alert(error);

        };
    }
    return (
        <div>
            
            <form onSubmit={handleSubmit} className="form-container">
            <h1>Register</h1>
                <input
                    className="form-input"
                    type="text"
                    placeholder="First Name"
                    value={first_name}
                    onChange={(e) => setFirstName(e.target.value)}
                />
                <input

                    type="text"
                    className="form-input"
                    placeholder="Last Name"
                    value={last_name}
                    onChange={(e) => setLastName(e.target.value)}
                />
                <input
                    type="text"
                     className="form-input"
                    placeholder="Username"
                    value={username}
                    onChange={(e) => setUsername(e.target.value)}
                />
                <input
                 className="form-input"
                    type="email"
                    placeholder="Email"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                />
                <select
                 className="form-input"
                    value={role}
                    onChange={(e) => setRole(e.target.value)}
                >
                    <option value="" disabled>Select Role</option>
                    <option value="CUSTOMER">Customer</option>
                    <option value="LOANPROVIDER">Loan Provider</option>
                    <option value="BANKPERSONNEL">Bank Personnel</option>
                </select>
                <input
                 className="form-input"
                    type="date"
                    placeholder="Date of Birth"
                    value={date_of_birth}
                    onChange={(e) => setDate_of_birth(e.target.value)}
                />
                <input
                 className="form-input"
                    type="text"
                    placeholder="Address"
                    value={address}
                    onChange={(e) => setAddress(e.target.value)}
                />
                <input
                 className="form-input"
                    type="text"
                    placeholder="Phone Number"
                    value={phone_number}
                    onChange={(e) => setPhoneNumber(e.target.value)}
                />
                <input
                 className="form-input"
                    type="password"
                    placeholder="Password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                />
                <button className="form-button" type="submit">Register</button>
            </form>
        </div>
       
    );
}

export default Register;