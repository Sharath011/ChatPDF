import { useState } from "react";
import Upload from "./components/Upload";
import Chat from "./components/Chat";

function App() {
  const [pdfUploaded, setPdfUploaded] = useState(false);

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gray-100 p-6">
      <h1 className="text-2xl font-bold mb-4">Chat with Your PDF</h1>
      <Upload onUpload={() => setPdfUploaded(true)} />
      {pdfUploaded && <Chat />}
    </div>
  );
}

export default App;
