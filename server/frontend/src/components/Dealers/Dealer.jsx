// ✅ Import necessary modules
import React, { useState, useEffect, useCallback } from 'react';  // ✅ Added `useCallback`
import { useParams } from 'react-router-dom';
import "./Dealers.css";
import "../assets/style.css";
import positive_icon from "../assets/positive.png";
import neutral_icon from "../assets/neutral.png";
import negative_icon from "../assets/negative.png";
import review_icon from "../assets/reviewbutton.png";
import Header from '../Header/Header';

// ✅ Dealer component
const Dealer = () => {
  const [dealer, setDealer] = useState({});
  const [reviews, setReviews] = useState([]);
  const [unreviewed, setUnreviewed] = useState(false);
  const [postReview, setPostReview] = useState(<></>);

  let params = useParams();
  let id = params.id;

  let root_url = window.location.origin + "/";
  let dealer_url = root_url + `djangoapp/dealer/${id}`;
  let reviews_url = root_url + `djangoapp/reviews/dealer/${id}`;
  let post_review = root_url + `postreview/${id}`;

  // ✅ Wrapped `get_dealer` in `useCallback`
  // const get_dealer = async () => { 
  //   try { 
  //     const res = await fetch(dealer_url, { method: "GET" }); 
  //     const retobj = await res.json(); 
  //     if (retobj.status === 200) { 
  //       let dealerobjs = Array.from(retobj.dealer); 
  //       setDealer(dealerobjs[0]); 
  //     } 
  //   } catch (error) { 
  //     console.error("❌ Error fetching dealer details:", error); 
  //   } 
  // };
  const get_dealer = useCallback(async () => {  // ✅ Converted to useCallback to avoid dependency issues
    try {
      const res = await fetch(dealer_url, { method: "GET" });
      const retobj = await res.json();
      if (retobj.status === 200) {
        let dealerobjs = Array.from(retobj.dealer);
        setDealer(dealerobjs[0]);
      }
    } catch (error) {
      console.error("❌ Error fetching dealer details:", error);
    }
  }, [dealer_url]);  // ✅ Ensures function remains stable

  // ✅ Wrapped `get_reviews` in `useCallback`
  // const get_reviews = async () => { 
  //   try { 
  //     const res = await fetch(reviews_url, { method: "GET" }); 
  //     const retobj = await res.json(); 
  //     if (retobj.status === 200) { 
  //       if (retobj.reviews.length > 0) { 
  //         setReviews(retobj.reviews); 
  //       } else { 
  //         setUnreviewed(true); 
  //       } 
  //     } 
  //   } catch (error) { 
  //     console.error("❌ Error fetching reviews:", error); 
  //   } 
  // };
  const get_reviews = useCallback(async () => {  // ✅ Converted to useCallback
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
  }, [reviews_url]);  // ✅ Avoids unnecessary re-renders

  // ✅ Wrapped `senti_icon` in `useCallback`
  // const senti_icon = (sentiment) => { 
  //   let icon = sentiment === "positive" 
  //     ? positive_icon 
  //     : sentiment === "negative" 
  //     ? negative_icon 
  //     : neutral_icon; 
  //   return icon; 
  // };
  const senti_icon = useCallback((sentiment) => {  // ✅ Ensures function remains stable
    let icon = sentiment === "positive"
      ? positive_icon
      : sentiment === "negative"
      ? negative_icon
      : neutral_icon;
    return icon;
  }, []);  // ✅ Keeps function reference stable

  // ✅ Updated `useEffect` with correct dependencies
  // useEffect(() => { 
  //   get_dealer(); 
  //   get_reviews(); 
  //   if (sessionStorage.getItem("username")) { 
  //     setPostReview( 
  //       <a href={post_review}> 
  //         <img 
  //           src={review_icon} 
  //           style={{ width: '10%', marginLeft: '10px', marginTop: '10px' }} 
  //           alt='Post Review' 
  //         /> 
  //       </a> 
  //     ); 
  //   } 
  // }, [id]); 
  useEffect(() => {  // ✅ Fixed missing dependencies warning
    get_dealer();
    get_reviews();
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
  }, [get_dealer, get_reviews, post_review]);  // ✅ Now all necessary dependencies are included

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
    </div>
  );
};

export default Dealer;