import React, { useState } from "react";

const Chat = () => {
  const [query, setQuery] = useState("");
  const [response, setResponse] = useState("");

  const handleQuery = async () => {
    const formData = new FormData();
    formData.append("query", query);

    try {
      const res = await fetch("http://127.0.0.1:8000/chat/", {
        method: "POST",
        body: formData,
      });
      const data = await res.json();
      setResponse(data.response);
    } catch (error) {
      console.error("Error fetching response:", error);
    }
  };

  return (
    <div>
      <input 
        type="text" 
        value={query} 
        onChange={(e) => setQuery(e.target.value)} 
        placeholder="Ask about the document..." 
      />
      <button onClick={handleQuery}>Submit</button>
      <p><strong>Response:</strong> {response}</p>
    </div>
  );
};

export default Chat;
