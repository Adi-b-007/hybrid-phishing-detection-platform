import React, { useEffect, useState } from "react";
import axios from "axios";
import jsPDF from "jspdf";
import autoTable from "jspdf-autotable";

function History() {

  const [history, setHistory] = useState([]);
  const [search, setSearch] = useState("");
  const [filter, setFilter] = useState("ALL");

  useEffect(() => {
    loadHistory();
  }, []);

  const loadHistory = async () => {

    try {

      const response = await axios.get(
        "http://127.0.0.1:5000/history"
      );

      setHistory(response.data);

    } catch (error) {

      console.error(error);

    }
  };

  const deleteRecord = async (id) => {

    const confirmDelete = window.confirm(
      "Are you sure you want to delete this record?"
    );

    if (!confirmDelete) return;

    try {

      await axios.delete(
        `http://127.0.0.1:5000/history/delete/${id}`
      );

      loadHistory();

    } catch (error) {

      console.error(error);

      alert("Delete failed");
    }
  };

  const downloadPDF = () => {

    const doc = new jsPDF();

    autoTable(doc, {
      head: [["URL", "Prediction", "Confidence"]],
      body: history.map((item) => [
        item.url,
        item.prediction,
        item.confidence
      ])
    });

    doc.save("Phishing_Report.pdf");
  };

  const filteredHistory = history.filter((item) => {

    const matchesSearch =
      item.url.toLowerCase().includes(
        search.toLowerCase()
      );

    const matchesFilter =
      filter === "ALL"
        ? true
        : item.prediction.toUpperCase() === filter;

    return matchesSearch && matchesFilter;
  });

  return (

    <div>

      <h2>Scan History</h2>

      <input
        type="text"
        placeholder="Search URL..."
        value={search}
        onChange={(e) => setSearch(e.target.value)}
        className="search-box"
      />

      <div className="filter-buttons">

        <button onClick={() => setFilter("ALL")}>
          All
        </button>

        <button onClick={() => setFilter("LEGITIMATE")}>
          Legitimate
        </button>

        <button onClick={() => setFilter("PHISHING")}>
          Phishing
        </button>

        <button onClick={downloadPDF}>
          Download Report
        </button>

      </div>

      <table border="1">

        <thead>
          <tr>
            <th>URL</th>
            <th>Prediction</th>
            <th>Confidence</th>
            <th>Time</th>
            <th>Action</th>
          </tr>
        </thead>

        <tbody>

          {filteredHistory.map((item, index) => (

            <tr key={index}>

              <td>{item.url}</td>

              <td>
                <span
                  className={
                    item.prediction === "Phishing"
                      ? "phishing-badge"
                      : "legit-badge"
                  }
                >
                  {item.prediction}
                </span>
              </td>

              <td>{item.confidence}%</td>

              <td>{item.timestamp}</td>

              <td>

                <button
                  className="delete-btn"
                  onClick={() => deleteRecord(item._id)}
                >
                  Delete
                </button>

              </td>

            </tr>

          ))}

        </tbody>

      </table>

    </div>

  );
}

export default History;