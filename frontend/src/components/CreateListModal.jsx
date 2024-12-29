import React, { useState } from "react";
import axios from "axios";
import { toast } from "react-toastify";

const CreateListModal = ({ accessToken, onClose }) => {
  const [step, setStep] = useState(1);
  const [listName, setListName] = useState("");
  const [listDescription, setListDescription] = useState("");
  const [selectedGenres, setSelectedGenres] = useState([]);
  const [selectedPopularity, setSelectedPopularity] = useState(null);
  const [selectedLanguage, setSelectedLanguage] = useState(null);
  const [startYear, setStartYear] = useState("");
  const [endYear, setEndYear] = useState("");

  const nextStep = () => setStep(step + 1);
  const prevStep = () => setStep(step - 1);

  const handleCreateList = async () => {
    try {
      const response = await axios.post("/create-list", {
        name: listName,
        description: listDescription,
        items: [], // Add selected items here
      }, {
        headers: { Authorization: `Bearer ${accessToken}` },
      });
      toast.success(`List created with ID: ${response.data.list_id}`);
      onClose();
    } catch (error) {
      toast.error("Failed to create list");
    }
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center">
      <div className="bg-white p-8 rounded-lg w-1/3">
        {step === 1 && (
          <div>
            <h2 className="text-2xl font-bold mb-6">Step 1: Select List Type</h2>
            <button onClick={nextStep} className="bg-blue-500 text-white px-4 py-2 rounded-md">Next</button>
          </div>
        )}
        {step === 2 && (
          <div>
            <h2 className="text-2xl font-bold mb-6">Step 2: Select Genres</h2>
            <button onClick={prevStep} className="bg-gray-500 text-white px-4 py-2 rounded-md">Back</button>
            <button onClick={nextStep} className="bg-blue-500 text-white px-4 py-2 rounded-md">Next</button>
          </div>
        )}
        {step === 3 && (
          <div>
            <h2 className="text-2xl font-bold mb-6">Step 3: Select Popularity</h2>
            <button onClick={prevStep} className="bg-gray-500 text-white px-4 py-2 rounded-md">Back</button>
            <button onClick={nextStep} className="bg-blue-500 text-white px-4 py-2 rounded-md">Next</button>
          </div>
        )}
        {step === 4 && (
          <div>
            <h2 className="text-2xl font-bold mb-6">Step 4: Select Language</h2>
            <button onClick={prevStep} className="bg-gray-500 text-white px-4 py-2 rounded-md">Back</button>
            <button onClick={nextStep} className="bg-blue-500 text-white px-4 py-2 rounded-md">Next</button>
          </div>
        )}
        {step === 5 && (
          <div>
            <h2 className="text-2xl font-bold mb-6">Step 5: Select Date Range</h2>
            <button onClick={prevStep} className="bg-gray-500 text-white px-4 py-2 rounded-md">Back</button>
            <button onClick={handleCreateList} className="bg-green-500 text-white px-4 py-2 rounded-md">Create List</button>
          </div>
        )}
      </div>
    </div>
  );
};

export default CreateListModal;
