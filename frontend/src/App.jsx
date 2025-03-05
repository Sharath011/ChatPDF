import React, { useState } from "react";
import Upload from "./components/Upload.jsx";
import Chat from "./components/Chat.jsx";

function App() {
  const [uploadedFile, setUploadedFile] = useState(null);

  return (
    <div>
      <h1>Chat with PDF</h1>
      <Upload onUpload={setUploadedFile} />
      {uploadedFile && <Chat />}
    </div>
  );
}

export default App;
