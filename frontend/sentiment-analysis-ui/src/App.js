import React, { useState } from "react";
import axios from "axios";

function App() {
  // States for user input, selected model, result, and loading state
  const [text, setText] = useState("");
  const [model, setModel] = useState("custom");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  // Handle input change
  const handleTextChange = (e) => setText(e.target.value);

  // Handle model selection change
  const handleModelChange = (e) => setModel(e.target.value);

  // Handle the button click to analyze sentiment
  const handleAnalyzeClick = async () => {
    setLoading(true);
    try {
      const response = await axios.post("http://127.0.0.1:8000/analyze/", {
        text: text,
        model: model,
      });
      setResult(response.data);
    } catch (error) {
      console.error("Error analyzing sentiment:", error);
      setResult({ sentiment: "Error", confidence: null });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="App">
      <h1>Sentiment Analysis</h1>
      
      {/* Input Field */}
      <div>
        <textarea
          value={text}
          onChange={handleTextChange}
          placeholder="Enter your text here..."
          rows="4"
          cols="50"
        />
      </div>

      {/* Dropdown for Model Selection */}
      <div>
        <label htmlFor="model">Select Model: </label>
        <select
          id="model"
          value={model}
          onChange={handleModelChange}
        >
          <option value="custom">Custom Model</option>
          <option value="llama">Llama 3</option>
        </select>
      </div>

      {/* Analyze Button */}
      <div>
        <button 
          onClick={handleAnalyzeClick} 
          disabled={loading || model === "llama"}
        >
          {loading 
            ? "Analyzing..." 
            : model === "llama" 
            ? "Groq Api needs credit card, sorry boss" 
            : "Analyze Sentiment"
          }
        </button>
      </div>


      {/* Result Section */}
      {result && (
        <div>
          <h3>Result:</h3>
          <p>Sentiment: <strong>{result.sentiment}</strong></p>
          {result.confidence !== null && (
            <p>Confidence: <strong>{result.confidence ? (result.confidence * 100).toFixed(2) + "%" : "N/A"}</strong></p>
          )}
        </div>
      )}
    </div>
  );
}

export default App;
