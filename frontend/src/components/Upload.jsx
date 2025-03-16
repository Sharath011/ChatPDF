import { useState } from "react";
import axios from "axios";

const Upload = ({ onUpload }) => {
  const [file, setFile] = useState(null);
  const [uploading, setUploading] = useState(false);

  const handleFileChange = (event) => {
    setFile(event.target.files[0]);
  };

  const handleUpload = async () => {
    if (!file) return alert("Please select a PDF file.");
    
    setUploading(true);
    const formData = new FormData();
    formData.append("file", file);

    try {
      await axios.post("http://127.0.0.1:8000/upload/", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });
      alert("PDF uploaded successfully!");
      onUpload(); // Notify parent
    } catch (error) {
      console.error("Upload failed:", error);
      alert("Upload failed. Try again.");
    }
    setUploading(false);
  };

  return (
    <div className="p-4 border rounded-lg shadow-md bg-white">
      <input type="file" accept="application/pdf" onChange={handleFileChange} className="mb-2" />
      <button 
        onClick={handleUpload} 
        className="bg-blue-500 text-white px-4 py-2 rounded-lg"
        disabled={uploading}
      >
        {uploading ? "Uploading..." : "Upload PDF"}
      </button>
    </div>
  );
};

export default Upload;