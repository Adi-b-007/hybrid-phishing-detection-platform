import React, { useEffect, useState } from "react";
import axios from "axios";
import "./Stats.css";

import {
  PieChart,
  Pie,
  Tooltip,
  Cell,
  Legend
} from "recharts";

function Stats() {

  const [stats, setStats] = useState(null);

  useEffect(() => {

    axios
      .get("http://127.0.0.1:5000/stats")
      .then((response) => {

        setStats(response.data);

      })
      .catch((error) => {

        console.error(error);

      });

  }, []);

  if (!stats) return null;

  const chartData = [

    {
      name: "Legitimate",
      value: stats.legitimate_urls
    },

    {
      name: "Phishing",
      value: stats.phishing_urls
    }

  ];

  const COLORS = [
    "#00ff99",
    "#ff4d4d"
  ];

  return (

    <div>

      <h2 className="section-title">
  Security Dashboard
       </h2>

      <div className="stats-container">

        <div className="card">
          <h2>{stats.total_scans}</h2>
          <p>Total Scans</p>
        </div>

        <div className="card">
          <h2>{stats.legitimate_urls}</h2>
          <p>Legitimate</p>
        </div>

        <div className="card">
          <h2>{stats.phishing_urls}</h2>
          <p>Phishing</p>
        </div>

      </div>

      <div className="chart-container">

        <h3>Detection Analytics</h3>

        <PieChart
          width={400}
          height={300}
        >

          <Pie
            data={chartData}
            cx="50%"
            cy="50%"
            outerRadius={100}
            dataKey="value"
            label
          >

            {chartData.map((entry, index) => (

              <Cell
                key={index}
                fill={COLORS[index]}
              />

            ))}

          </Pie>

          <Tooltip />

          <Legend />

        </PieChart>

      </div>

    </div>

  );

}

export default Stats;