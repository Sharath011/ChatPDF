import { useState, useEffect } from "react";
import axios from "axios";

const Chat = () => {
  const [userQuery, setQuery] = useState("");
  const [response, setResponse] = useState("");
  const [models, setModels] = useState([]);
  const [selectedModel, setSelectedModel] = useState("openai");

  useEffect(() => {
    const fetchModels = async () => {
      try {
        const res = await axios.get("http://127.0.0.1:8000/models/");
        setModels(res.data.models);
      } catch (error) {
        console.error("Failed to fetch models:", error);
      }
    };
    fetchModels();
  }, []);

  const handleChat = async () => {
    if (!userQuery) return alert("Enter a question!");
  
    try {
      const res = await axios.post("http://127.0.0.1:8000/chat/", {
        query: userQuery,
        model: selectedModel, // Ensure this key exists in the request
      }); // Send JSON object
      setResponse(res.data.response);
    } catch (error) {
      console.error("Chat failed:", error);
      alert("Error fetching response");
    }
  };  

  return (
    <div className="p-4 border rounded-lg shadow-md bg-white">
      <label className="block mb-2 font-semibold">Select LLM:</label>
      <select 
        value={selectedModel} 
        onChange={(e) => setSelectedModel(e.target.value)}
        className="border px-3 py-2 rounded-md w-full mb-3"
      >
        {models.map((model) => (
          <option key={model} value={model}>{model.toUpperCase()}</option>
        ))}
      </select>

      <input 
        type="text" 
        value={userQuery} 
        onChange={(e) => setQuery(e.target.value)} 
        placeholder="Ask something about the PDF..."
        className="border px-3 py-2 w-full rounded-md"
      />
      <button 
        onClick={handleChat} 
        className="mt-2 bg-green-500 text-white px-4 py-2 rounded-lg"
      >
        Ask
      </button>
      {response && <p className="mt-4 bg-gray-100 p-3 rounded-md">{response}</p>}
    </div>
  );
};

export default Chat;
