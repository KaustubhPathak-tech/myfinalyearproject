import React, { useState, useEffect } from "react";
import "./App.css";
import axios from "axios";
import {
  AreaChart,
  Area,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
} from "recharts";
function App() {
  const [data, setData] = useState([]);
  const [data1, setData1] = useState([]);
  const [alert, setAlert] = useState(false);
  const [emergency, setEmergency] = useState(0);
  const tempemergency = localStorage.getItem("tempemergency");
  // if (tempemergency) {
  //   setEmergency(tempemergency);
  // }

  useEffect(() => {
    setInterval(() => {
      fetchData();
    }, 5000);
  }, []);

  useEffect(() => {
    checkThresholds(data);
    predictEmergency(data);
  }, [data]);

  useEffect(() => {
    checkThresholds1(data1);
  }, [data1]);

  const checkThresholds = (data) => {
    if (data.length > 0) {
      const lastItem = data[data.length - 1];
      if (lastItem.temperature > 40) {
        triggerAlert();
      } else {
        setAlert(false);
      }
    }
  };

  const checkThresholds1 = (data1) => {
    if (data1.length > 0) {
      const lastItem = data1[data1.length - 1];
      if (lastItem.humidity > 80) {
        triggerAlert();
      } else {
        setAlert(false);
      }
    }
  };

  //function to predict emergency
  const predictEmergency = (data) => {
    if (data.length > 0) {
      const temp1 = data[data.length - 1].temperature;
      const temp2 = data[data.length - 2].temperature;
      const hum1 = data[data.length - 1].humidity;
      const hum2 = data[data.length - 2].humidity;
      if (temp1 - temp2 > 0 && hum1 - hum2 < 0) {
        setEmergency(emergency + (temp1 - temp2) + (hum2 - hum1));
      } else if (temp1 - temp2 < 0 && hum1 - hum2 > 0) {
        setEmergency(emergency - (temp2 - temp1) - (hum1 - hum2));
      } else {
        setEmergency(emergency);
      }
      // localStorage.setItem("tempemergency", emergency);
    }
  };

  const triggerAlert = () => {
    const msg = new SpeechSynthesisUtterance();
    msg.text = "Temperature or humidity exceeded threshold!";
    window.speechSynthesis.speak(msg);
    setAlert(true);
  };

  const fetchData = async () => {
    try {
      const response = await axios.get("/api/temp-data");
      const response1 = await axios.get("/api/humidity-data");
      setData(response.data);
      setData1(response1.data);
    } catch (error) {
      console.error("Error fetching data:", error);
    }
  };

  console.log(alert);
  return (
    <div className="App">
      <div>
        <h2 className="font-bold text-xl text-blue-700 pt-5">
          Live Monitoring of Temperature and Humidity
        </h2>
        <div className="p-10">
          <div className="temperature w-fit">
            <AreaChart
              width={900}
              height={400}
              data={data}
              margin={{
                top: 0,
                right: 34,
                left: 0,
                bottom: 0,
              }}
            >
              <XAxis
                dataKey="time"
                axisLine={false}
                tickSize={0}
                padding={{ left: 20, right: 20 }}
                name="Time"
              />
              <YAxis
                dataKey="temperature"
                axisLine={false}
                tickSize={0}
                padding={{ top: 20, bottom: 20 }}
                name="Temperature"
              />
              <Tooltip />
              <Legend />
              <Area
                type="monotone"
                dataKey="temperature"
                stroke="#FF8E00"
                fill="#FFF5E7"
              />
            </AreaChart>
          </div>
          <div className="humidity w-fit">
            <AreaChart
              width={900}
              height={400}
              data={data1}
              margin={{
                top: 0,
                right: 34,
                left: 0,
                bottom: 0,
              }}
            >
              <XAxis
                dataKey="time"
                axisLine={false}
                tickSize={0}
                padding={{ left: 20, right: 20 }}
                name="Time"
              />
              <YAxis
                dataKey="humidity"
                axisLine={false}
                tickSize={0}
                padding={{ top: 20, bottom: 20 }}
                name="humidity"
              />
              <Tooltip />
              <Legend />
              <Area
                type="monotone"
                dataKey="humidity"
                stroke="#FF8E00"
                fill="#FFF5E7"
                // name="Humidity"
              />
            </AreaChart>
          </div>
        </div>
      </div>
      <div className="alertbox p-4">
        <h2 className="font-bold text-xl text-blue-700 mb-4">Alert Status</h2>
        <div className="leds ">
          {alert ? (
            <>
              {" "}
              <span>High temperature or Humidity Detected</span> &nbsp; &nbsp;
              <span className="bg-red-500 pl-5 pt-1 rounded-md"></span>
            </>
          ) : (
            <>
              <span>Normal</span> &nbsp; &nbsp;{" "}
              <span className="bg-green-500 pl-5 pt-1 rounded-md"></span>
            </>
          )}
        </div>
      </div>
      <div className="emergency-prediction">
        <h2 className="font-bold text-xl text-blue-700 mb-4">
          Emergency Prediction
        </h2>
        <div className="emergency">
          <span>Chances of Accident (in %) : {emergency}</span>
        </div>
      </div>
    </div>
  );
}

export default App;
