import React from "react";

const ListCard = ({ list }) => {
  return (
    <div className="bg-white p-4 rounded-lg shadow-md">
      <h3 className="text-xl font-semibold mb-2">{list.name}</h3>
      <p className="text-gray-600 mb-4">{list.description}</p>
      <p className="text-sm text-gray-500">Updated: {list.updated_at}</p>
    </div>
  );
};

export default ListCard;
