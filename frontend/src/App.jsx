import React, { useState, useEffect } from "react";
import axios from "axios";
import { toast, ToastContainer } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";
import ListCard from "./components/ListCard";
import CreateListModal from "./components/CreateListModal";

const App = () => {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [accessToken, setAccessToken] = useState("");
  const [lists, setLists] = useState([]);
  const [loading, setLoading] = useState(true);
  const [isModalOpen, setIsModalOpen] = useState(false);

  useEffect(() => {
    const token = localStorage.getItem("trakt_access_token");
    if (token) {
      setIsAuthenticated(true);
      setAccessToken(token);
      fetchLists(token);
    }
  }, []);

  const authenticateTrakt = async () => {
    try {
      const response = await axios.get("/auth/trakt");
      window.location.href = response.data.auth_url;
    } catch (error) {
      toast.error("Failed to authenticate with Trakt");
    }
  };

  const fetchLists = async (token) => {
    try {
      const response = await axios.get("/lists", {
        headers: { Authorization: `Bearer ${token}` },
      });
      setLists(response.data);
    } catch (error) {
      toast.error("Failed to fetch lists");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="p-8 bg-gray-100 min-h-screen">
      <h1 className="text-3xl font-bold mb-8">CouchMoney Clone</h1>

      {/* Authentication */}
      {!isAuthenticated && (
        <button
          onClick={authenticateTrakt}
          className="bg-blue-500 text-white px-6 py-2 rounded-md hover:bg-blue-600"
        >
          Connect to Trakt
        </button>
      )}

      {/* Description */}
      {isAuthenticated && (
        <div className="mb-8">
          <p className="text-lg">
            Welcome to CouchMoney Clone! This app helps you create and manage Trakt lists with personalized recommendations.
            Your lists are automatically updated daily with the latest recommendations based on your preferences.
          </p>
        </div>
      )}

      {/* Create List Button */}
      {isAuthenticated && (
        <button
          onClick={() => setIsModalOpen(true)}
          className="bg-green-500 text-white px-6 py-2 rounded-md hover:bg-green-600"
        >
          Create List
        </button>
      )}

      {/* List of Trakt Lists */}
      {isAuthenticated && (loading ? (
        <p>Loading...</p>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {lists.map((list) => (
            <ListCard key={list.ids.trakt} list={list} />
          ))}
        </div>
      ))}

      {/* Create List Modal */}
      {isModalOpen && (
        <CreateListModal
          accessToken={accessToken}
          onClose={() => setIsModalOpen(false)}
        />
      )}

      <ToastContainer />
    </div>
  );
};

export default App;
