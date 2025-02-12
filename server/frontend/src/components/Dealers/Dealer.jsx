// ✅ Import necessary modules
import React, { useState, useEffect } from "react";
import "./Dealers.css";

const Dealers = () => {
  // ✅ State Management
  const [dealers, setDealers] = useState([]);
  const [selectedState, setSelectedState] = useState("All");

  // ✅ Correct API Endpoint
  let root_url = window.location.origin;
  let dealers_url = `${root_url}/djangoapp/get_dealers/`;  // ✅ This worked

  // ✅ Fetch Dealers on Mount
  useEffect(() => {
    fetchDealers();  // ✅ Correctly fetching all dealers
  }, []);

  const fetchDealers = async (state = "All") => {
    let url = state === "All" ? dealers_url : `${dealers_url}${state}/`;  // ✅ No query params
    console.log(`🔍 Fetching dealers from: ${url}`);

    try {
      const res = await fetch(url);
      const data = await res.json();

      if (data.status === 200 && data.dealers) {
        setDealers(data.dealers);
      } else {
        setDealers([]);
      }
    } catch (error) {
      console.error("❌ Error fetching dealers:", error);
    }
  };

  const handleStateChange = (event) => {
    let state = event.target.value;
    setSelectedState(state);
    fetchDealers(state);
  };

  return (
    <div>
      <h1>Dealerships</h1>
      <label>Filter by State:</label>
      <select value={selectedState} onChange={handleStateChange}>
        <option value="All">All States</option>
        <option value="Texas">Texas</option>
        <option value="California">California</option>
        <option value="Pennsylvania">Pennsylvania</option>
        <option value="Maryland">Maryland</option>
      </select>

      <table>
        <thead>
          <tr>
            <th>ID</th>
            <th>Dealer Name</th>
            <th>City</th>
            <th>Address</th>
            <th>Zip</th>
          </tr>
        </thead>
        <tbody>
          {dealers.map((dealer) => (
            <tr key={dealer.id}>
              <td>{dealer.id}</td>
              <td>
                <a href={`/dealer/${dealer.id}`}>{dealer.full_name}</a>
              </td>
              <td>{dealer.city}</td>
              <td>{dealer.address}</td>
              <td>{dealer.zip}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default Dealers;

/*
------------------------------------
🔄 **CHANGES MADE COMPARED TO BROKEN VERSION**
------------------------------------

1️⃣ **API Endpoint Fix**  
   - ✅ `let dealers_url = ${root_url}/djangoapp/get_dealers/;`
   - ❌ Broken version had: `let dealers_url = ${root_url}/api/get_dealers/;`
   - 🛠 The API changed to `api/`, breaking the previous working setup.

2️⃣ **Fixed `useEffect` Hook**
   - ✅ `useEffect(() => { fetchDealers(); }, []);`
   - ❌ Broken version used `useEffect(() => { fetchDealers(selectedState); }, [selectedState]);`
   - 🛠 This caused a **missing dependency error**.

3️⃣ **Fixed API Request URL**
   - ✅ `let url = state === "All" ? dealers_url : ${dealers_url}${state}/;`
   - ❌ Broken version used: `let url = state === "All" ? dealers_url : ${dealers_url}?state=${state};`
   - 🛠 Using query parameters caused **backend filtering issues**.

4️⃣ **Removed Faulty `useEffect` Dependencies**
   - ✅ This version does **not** depend on `selectedState` inside `useEffect`.
   - 🛠 Prevents unnecessary re-renders.

------------------------------------
*/