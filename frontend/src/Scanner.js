import React, { useState } from "react";
import axios from "axios";
import { FaShieldAlt } from "react-icons/fa";
import "./Scanner.css";
<div className="header">
  <FaShieldAlt size={50} color="#00ff99" />
  <h1>PHISHING DETECTION PLATFORM</h1>
</div>
function Scanner() {

  const [url, setUrl] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const scanURL = async () => {

  const cleanedURL = url.trim();

  if (!cleanedURL) {

    alert("Please enter a URL");

    return;
  }

  try {

    setLoading(true);

    const response = await axios.post(
      "http://127.0.0.1:5000/predict",
      {
        url: cleanedURL
      }
    );

    setResult(response.data);

  } catch (error) {

    if (
      error.response &&
      error.response.data &&
      error.response.data.error
    ) {

      alert(
        error.response.data.error
      );

    } else {

      alert(
        "Unable to connect to Flask API"
      );

    }

  } finally {

    setLoading(false);

  }
};

  return (
    <div className="scanner-container">

      <div className="header">
        <FaShieldAlt size={50} />
        <h1>Phishing Detection Platform</h1>
      </div>

      <div className="search-box">

        <input
  type="text"
  placeholder="https://example.com"
  value={url}
  onChange={(e) => setUrl(e.target.value)}
/>

        <button onClick={scanURL}>
           {loading ? "Scanning..." : "Scan URL"}
        </button>

      </div>

      {result && (

        <div className="result-card">
          <div className="risk-meter">

  <h3>Risk Score</h3>

  <div className="progress">

    <div
  className="progress-fill"
  style={{
    width: `${result.risk_score}%`,
    background:
      result.risk_score > 70
        ? "#ff4444"
        : result.risk_score > 40
        ? "#ffaa00"
        : "#00ff99"
  }}
/>

  </div>

  <p>{result.confidence}%</p>

</div>

          <h2>Scan Result</h2>

          <p>
            <strong>URL:</strong> {result.url}
          </p>

          <p>
            <strong>Status:</strong>
            {" "}
            {result.prediction}
          </p>

          <p>
            <strong>Confidence:</strong>
            {" "}
            {result.confidence}%
          </p>

          <p>
            <strong>Risk Score:</strong>
            {" "}
            {result.risk_score}/100
</p>
          <div className="threat-analysis">

  <h3>Threat Analysis</h3>

  {result.reasons &&
   result.reasons.length > 0 ? (

    result.reasons.map(
      (reason, index) => (

        <p
          key={index}
          className="threat-item"
        >
          ⚠ {reason}
        </p>

      )
    )

  ) : (

    <p className="safe-msg">
      No suspicious indicators detected
    </p>

  )}

</div>
{result.domain_info && (

<div className="domain-card">

  <h3>Domain Intelligence</h3>

  <p>
    <strong>Domain:</strong>
    {" "}
    {result.domain_info.domain}
  </p>

  <p>
    <strong>TLD:</strong>
    {" "}
    {result.domain_info.tld}
  </p>

  <p>
    <strong>Length:</strong>
    {" "}
    {result.domain_info.length}
  </p>

  <p>
    <strong>Hyphens:</strong>
    {" "}
    {result.domain_info.hyphens}
  </p>

  <p>
    <strong>Contains Digits:</strong>
    {" "}
    {result.domain_info.contains_digits}
  </p>

  <p>
    <strong>Protocol:</strong>
    {" "}
    {result.domain_info.protocol}
  </p>

  <p>
    <strong>Risk Level:</strong>
    {" "}
    {result.domain_info.risk_level}
  </p>

</div>

)}
        </div>

      )}

    </div>
          
  );
}

export default Scanner;