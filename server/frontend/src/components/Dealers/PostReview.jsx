// ✅ Import necessary modules
import React, { useState, useEffect, useCallback } from "react";
import { useParams } from "react-router-dom";
import "./Dealers.css";
import "../assets/style.css";
import Header from "../Header/Header";

const PostReview = () => {
  // ✅ State management for dealer details, review text, selected car model/year/date, and list of car models
  const [dealer, setDealer] = useState({});
  const [review, setReview] = useState("");
  const [model, setModel] = useState(); // Holds the selected car make & model combined as string
  const [year, setYear] = useState("");
  const [date, setDate] = useState("");
  const [carmodels, setCarmodels] = useState([]);

  // 🔧 SUGGESTION: Compute root URL using window.location.origin for consistency
  let curr_url = window.location.href;
  // Extract root URL up to "postreview"
  let root_url = curr_url.substring(0, curr_url.indexOf("postreview"));
  let params = useParams();
  let id = params.id; // Dealer id from URL

  // Construct endpoints using the computed root URL
  let dealer_url = `${root_url}djangoapp/dealer/${id}`;
  let review_url = `${root_url}djangoapp/add_review`;
  let carmodels_url = `${root_url}djangoapp/get_cars`;

  // ✅ Function to post a review
  const postreview = async () => {
    // Construct user's full name from sessionStorage
    let name = sessionStorage.getItem("firstname") + " " + sessionStorage.getItem("lastname");
    if (name.includes("null")) {
      name = sessionStorage.getItem("username");
    }

    // 🔧 SUGGESTION: Validate that all fields are provided
    if (!model || review === "" || date === "" || year === "" || model === "") {
      alert("All details are mandatory");
      return;
    }

    // Split the model string to obtain car make and car model separately
    let model_split = model.split(" ");
    let make_chosen = model_split[0];
    let model_chosen = model_split[1];

    // Construct the JSON input for the review
    let jsoninput = JSON.stringify({
      name: name,
      dealership: id,
      review: review,
      purchase: true,
      purchase_date: date,
      car_make: make_chosen,
      car_model: model_chosen,
      car_year: year,
    });

    console.log(jsoninput);

    try {
      const res = await fetch(review_url, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: jsoninput,
      });

      const json = await res.json();
      if (json.status === 200) {
        // Redirect to dealer details page upon successful review submission
        window.location.href = window.location.origin + "/dealer/" + id;
      } else {
        alert("Failed to submit review.");
      }
    } catch (error) {
      console.error("❌ Error posting review:", error);
      alert("An error occurred while posting the review.");
    }
  };

  // ✅ useCallback for get_dealer to avoid unnecessary re-creation of function
  const get_dealer = useCallback(async () => {
    console.log(`🔍 Fetching dealer from: ${dealer_url}`);
    try {
      const res = await fetch(dealer_url, { method: "GET" });
      const retobj = await res.json();

      if (retobj.status === 200) {
        // 🔧 SUGGESTION: If retobj.dealer is returned as an array, take the first element
        let dealerobjs = Array.from(retobj.dealer);
        if (dealerobjs.length > 0) setDealer(dealerobjs[0]);
      }
    } catch (error) {
      console.error("❌ Error fetching dealer:", error);
    }
  }, [dealer_url]);

  // ✅ useCallback for get_cars to fetch available car models
  const get_cars = useCallback(async () => {
    console.log(`🔍 Fetching cars from: ${carmodels_url}`);
    try {
      const res = await fetch(carmodels_url, { method: "GET" });
      const retobj = await res.json();
      // 🔧 SUGGESTION: retobj.CarModels should contain an array of car model objects
      let carmodelsarr = Array.from(retobj.CarModels);
      setCarmodels(carmodelsarr);
    } catch (error) {
      console.error("❌ Error fetching cars:", error);
    }
  }, [carmodels_url]);

  // ✅ useEffect to fetch dealer details and available car models when component mounts
  useEffect(() => {
    get_dealer();
    get_cars();
  }, [get_dealer, get_cars]);

  return (
    <div>
      <Header />
      <div style={{ margin: "5%" }}>
        <h1 style={{ color: "darkblue" }}>{dealer.full_name}</h1>
        {/* Textarea for entering review text */}
        <textarea
          id="review"
          cols="50"
          rows="7"
          onChange={(e) => setReview(e.target.value)}
          placeholder="Write your review here..."
        ></textarea>

        <div className="input_field">
          Purchase Date{" "}
          <input type="date" onChange={(e) => setDate(e.target.value)} />
        </div>

        <div className="input_field">
          Car Make
          <select name="cars" id="cars" onChange={(e) => setModel(e.target.value)}>
            <option value="" selected disabled hidden>
              Choose Car Make and Model
            </option>
            {carmodels.map((carmodel) => (
              <option
                key={carmodel.CarModel}
                value={carmodel.CarMake + " " + carmodel.CarModel}
              >
                {carmodel.CarMake} {carmodel.CarModel}
              </option>
            ))}
          </select>
        </div>

        <div className="input_field">
          Car Year{" "}
          <input
            type="number"
            onChange={(e) => setYear(e.target.value)}
            max={2023}
            min={2015}
          />
        </div>

        <div>
          <button className="postreview" onClick={postreview}>
            Post Review
          </button>
        </div>
      </div>
    </div>
  );
};

export default PostReview;