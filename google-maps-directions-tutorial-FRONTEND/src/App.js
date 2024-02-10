import Login from "./Components/LoginForm/Login";
import Map from "./Components/Map/Map"
import React, { useState, useEffect } from "react"
import SignIn from "./Components/SignIn/SignIn";
import SignUp from "./Components/SignUp/SignUp";
import { BrowserRouter, Routes, Route } from "react-router-dom";




function App() {

  const [data, setData] = useState([{}]);

  // useEffect(() => {
  //   const postData = {
  //     key1: 'sample',
  //     key2: 'sample@'
  //   };

  //   fetch("http://localhost:5000/api/data", {
  //     method: 'POST',
  //     headers: {
  //       'Content-Type': 'application/json'
  //       // You may include additional headers if required by your API
  //     },
  //     body: JSON.stringify(postData)
  //   }).then(
  //     res => res.json()
  //   ).then(data => {
  //     setData(data)
  //     console.log(data)
  //   }
  //   )
  // }, [])



  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<SignIn />} />

        <Route path="/signup" element={<SignUp />} />
        <Route path="/map" element={<Map />} />
        


      </Routes>
    </BrowserRouter>
  );

}

export default App
