// ✅ Import necessary modules
import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import "./Dealers.css";
import "../assets/style.css";
import positive_icon from "../assets/positive.png";
import neutral_icon from "../assets/neutral.png";
import negative_icon from "../assets/negative.png";
import review_icon from "../assets/reviewbutton.png";
import Header from '../Header/Header';

const Dealer = () => {
  // State for dealer details and reviews
  const [dealer, setDealer] = useState({});
  const [reviews, setReviews] = useState([]);
  const [unreviewed, setUnreviewed] = useState(false);
  const [postReview, setPostReview] = useState(<></>);

  // Retrieve the dealer id from the URL parameters
  let params = useParams();
  let id = params.id;

  // 🔧 SUGGESTION: Instead of computing the root URL from window.location.href,
  // you can use window.location.origin directly.
  let root_url = window.location.origin + "/";
  // Construct endpoints based on the root URL and dealer id
  let dealer_url = root_url + `djangoapp/dealer/${id}`;
  let reviews_url = root_url + `djangoapp/reviews/dealer/${id}`;
  let post_review = root_url + `postreview/${id}`;

  // Function to fetch dealer details
  const get_dealer = async () => {
    try {
      const res = await fetch(dealer_url, { method: "GET" });
      const retobj = await res.json();
      if (retobj.status === 200) {
        // 🔧 SUGGESTION: If retobj.dealer is already an object, you can directly set it.
        // Here we assume it's returned as an array, so we take the first element.
        let dealerobjs = Array.from(retobj.dealer);
        setDealer(dealerobjs[0]);
      }
    } catch (error) {
      console.error("❌ Error fetching dealer details:", error);
    }
  };

  // Function to fetch reviews for the dealer
  const get_reviews = async () => {
    try {
      const res = await fetch(reviews_url, { method: "GET" });
      const retobj = await res.json();
      if (retobj.status === 200) {
        if (retobj.reviews.length > 0) {
          setReviews(retobj.reviews);
        } else {
          setUnreviewed(true);
        }
      }
    } catch (error) {
      console.error("❌ Error fetching reviews:", error);
    }
  };

  // Function to choose an icon based on sentiment
  const senti_icon = (sentiment) => {
    let icon = sentiment === "positive"
      ? positive_icon
      : sentiment === "negative"
      ? negative_icon
      : neutral_icon;
    return icon;
  };

  // Fetch dealer details and reviews on component mount
  useEffect(() => {
    get_dealer();
    get_reviews();
    // If user is logged in, set the post review link
    if (sessionStorage.getItem("username")) {
      setPostReview(
        <a href={post_review}>
          <img
            src={review_icon}
            style={{ width: '10%', marginLeft: '10px', marginTop: '10px' }}
            alt='Post Review'
          />
        </a>
      );
    }
  }, [id]); // 🔧 SUGGESTION: Depend on id so that if URL changes, the data refreshes

  return (
    <div style={{ margin: "20px" }}>
      <Header />
      <div style={{ marginTop: "10px" }}>
        <h1 style={{ color: "grey" }}>
          {dealer.full_name}{postReview}
        </h1>
        <h4 style={{ color: "grey" }}>
          {dealer.city}, {dealer.address}, Zip - {dealer.zip}, {dealer.state}
        </h4>
      </div>
      <div className="reviews_panel">
        {reviews.length === 0 && unreviewed === false ? (
          // 🔧 SUGGESTION: Use a <p> or <span> element instead of <text>
          <p>Loading Reviews....</p>
        ) : unreviewed === true ? (
          <div>No reviews yet!</div>
        ) : (
          reviews.map((review, index) => (
            <div key={index} className='review_panel'>
              <img
                src={senti_icon(review.sentiment)}
                className="emotion_icon"
                alt='Sentiment'
              />
              <div className='review'>{review.review}</div>
              <div className="reviewer">
                {review.name} {review.car_make} {review.car_model} {review.car_year}
              </div>
            </div>
          ))
        )}
      </div>
      {/* 🔧 REMINDER: Once integrated, take a screenshot of the dealer details page (with URL visible) for peer review */}
    </div>
  );
};

export default Dealer;