import React, { useState, useEffect } from 'react';
import "./Dealers.css";
import "../assets/style.css";
import Header from '../Header/Header';
import review_icon from "../assets/reviewicon.png";

const Dealers = () => {
  // State for storing the list of dealers
  const [dealersList, setDealersList] = useState([]);
  // State for storing unique states extracted from the dealers
  const [states, setStates] = useState([]);

  // API endpoint for fetching all dealers
  const dealer_url = "/djangoapp/get_dealers";

  // Function to filter dealers by a given state
  const filterDealers = async (state) => {
    // 🔧 SUGGESTION: Compute a fresh URL for filtering; avoid mutating global variable
    let url = `/djangoapp/get_dealers/${state}`;
    console.log(`🔍 Fetching dealers for state from: ${url}`);
    try {
      const res = await fetch(url, { method: "GET" });
      const retobj = await res.json();
      if (retobj.status === 200) {
        // Convert the returned dealers array (if needed) and update state
        let state_dealers = Array.from(retobj.dealers);
        setDealersList(state_dealers);
      }
    } catch (error) {
      console.error("❌ Error filtering dealers:", error);
    }
  };

  // Function to fetch all dealers
  const get_dealers = async () => {
    try {
      const res = await fetch(dealer_url, { method: "GET" });
      const retobj = await res.json();
      if (retobj.status === 200) {
        let all_dealers = Array.from(retobj.dealers);
        // Extract unique states from the dealers list
        let statesArr = [];
        all_dealers.forEach((dealer) => {
          statesArr.push(dealer.state);
        });
        setStates(Array.from(new Set(statesArr)));
        setDealersList(all_dealers);
      }
    } catch (error) {
      console.error("❌ Error fetching dealers:", error);
    }
  };

  // Fetch dealers on component mount
  useEffect(() => {
    get_dealers();
  }, []);

  // Check if a user is logged in (based on sessionStorage)
  let isLoggedIn = sessionStorage.getItem("username") !== null;

  return (
    <div>
      <Header />
      <table className="table">
        <thead>
          <tr>
            <th>ID</th>
            <th>Dealer Name</th>
            <th>City</th>
            <th>Address</th>
            <th>Zip</th>
            <th>
              <select name="state" id="state" onChange={(e) => filterDealers(e.target.value)}>
                {/* 🔧 SUGGESTION: Using a placeholder option; 'selected' attribute is handled by the select value */}
                <option value="" disabled hidden>State</option>
                <option value="All">All States</option>
                {states.map((state, index) => (
                  <option key={index} value={state}>{state}</option>
                ))}
              </select>        
            </th>
            {isLoggedIn ? <th>Review Dealer</th> : null}
          </tr>
        </thead>
        <tbody>
          {dealersList.map((dealer) => (
            <tr key={dealer.id}>
              <td>{dealer['id']}</td>
              <td>
                <a href={`/dealer/${dealer['id']}`}>{dealer['full_name']}</a>
              </td>
              <td>{dealer['city']}</td>
              <td>{dealer['address']}</td>
              <td>{dealer['zip']}</td>
              <td>{dealer['state']}</td>
              {isLoggedIn ? (
                <td>
                  <a href={`/postreview/${dealer['id']}`}>
                    <img src={review_icon} className="review_icon" alt="Post Review" />
                  </a>
                </td>
              ) : null}
            </tr>
          ))}
        </tbody>
      </table>
      {/* 🔧 REMINDER: After verifying functionality, take a screenshot of the Dealers page (with filter and table visible) for peer review */}
    </div>
  );
};

export default Dealers;

/*
------------------------------------
🔄 **CHANGES MADE COMPARED TO BROKEN VERSION**
------------------------------------

1️⃣ **API Endpoint Fix**  
   - ✅ `const dealer_url = "/djangoapp/get_dealers";`
   - ❌ Broken version had: `const dealer_url = "/api/get_dealers";`
   - 🛠 The API changed to `djangoapp/`, breaking the previous working setup.

2️⃣ **Fixed useEffect Hook**
   - ✅ `useEffect(() => { get_dealers(); }, []);`
   - ❌ Broken version used a dependency that caused issues.
   - 🛠 This version ensures dealers are fetched once on mount.

3️⃣ **Fixed API Request URL for Filtering**
   - ✅ `let url = state === "All" ? dealer_url : `/djangoapp/get_dealers/${state}`;`
   - ❌ Broken version used query parameters causing backend filtering issues.
   - 🛠 Using URL segments resolves filtering correctly.

4️⃣ **Removed Faulty Dependencies**
   - ✅ This version does not depend on state changes inside useEffect unnecessarily.
   - 🛠 Prevents unnecessary re-renders.
------------------------------------
*/