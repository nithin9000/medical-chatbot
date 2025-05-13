import React, { useState } from 'react';

const DocumentsUploaded = () => {
  const [document, setDocument] = useState(null);  // To store selected file
  const [uploadedDocument, setUploadedDocument] = useState(null);  // To store uploaded file after submit

  const handleFileChange = (e) => {
    const file = e.target.files[0];
    setDocument(file);  // Store the selected file
  };

  const handleUpload = () => {
    if (document) {
      setUploadedDocument(document);  // Store the uploaded file
      setDocument(null);  // Clear the selected file input after upload
    } else {
      alert('Please select a file first');
    }
  };

  return (
    <div>
      <h2>Upload Documents</h2>

      {/* File Input */}
      <input
        type="file"
        onChange={handleFileChange}
        accept="application/pdf, image/*, .doc, .docx, .txt"
      />

      {/* Display the selected document name */}
      {document && <p>File selected: {document.name}</p>}

      {/* Submit button to upload the document */}
      <button onClick={handleUpload}>Submit</button>

      {/* Display the uploaded document */}
      {uploadedDocument && (
        <div>
          <h3>Uploaded Document</h3>
          <p>{uploadedDocument.name}</p>  {/* Show the document name */}
          {/* Optionally, show a link to download the file */}
          <a href={URL.createObjectURL(uploadedDocument)} download={uploadedDocument.name}>
            Download {uploadedDocument.name}
          </a>
        </div>
      )}
    </div>
  );
};

export default DocumentsUploaded;
