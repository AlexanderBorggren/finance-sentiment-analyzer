import React from "react";

interface CardProps {
  title: string;
  description: string;
}

const Card: React.FC<CardProps> = ({ title, description }) => {
  return (
    <div className="bg-white shadow-md rounded-lg p-6 max-w-sm mx-auto">
      <h3 className="text-xl font-semibold text-gray-900">{title}</h3>
      <p className="mt-4 text-gray-700">{description}</p>
    </div>
  );
};

export default Card;
