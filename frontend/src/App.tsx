import './App.css'
import React from 'react';
import Card from './components/ui/Card';

const App: React.FC = () => {
    return (
        <div className="min-h-screen bg-gray-100 py-10">
            <h1 className="text-center text-4xl font-bold mb-8">Sentiment Analysis Results</h1>
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6 px-4">
                <Card 
                    title="Bullish Sentiment" 
                    description="Strong positive sentiment detected in the latest news."
                />
                <Card 
                    title="Neutral Sentiment" 
                    description="Market sentiment is balanced with no significant bias."
                />
                <Card 
                    title="Bearish Sentiment" 
                    description="Negative sentiment prevails based on recent news."
                />
            </div>
        </div>
    );
};

export default App;