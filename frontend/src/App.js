import React, { useState, useRef } from 'react';
import './App.css';

const App = () => {
  const [videoUrl, setVideoUrl] = useState('');
  const [selectedPersona, setSelectedPersona] = useState('nyc-drama');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState('');
  const fileInputRef = useRef(null);

  const personas = [
    { id: 'nyc-drama', name: '🏙️ NYC Drama', description: 'Urban lifestyle & apartment hunts' },
    { id: 'luxury-rentals', name: '🏨 Luxury Rentals', description: 'High-end property showcases' },
    { id: 'fitness-guru', name: '💪 Fitness Guru', description: 'Motivational workout content' },
    { id: 'conspiracy-mode', name: '🔍 Conspiracy Mode', description: 'Deep dive investigations' },
    { id: 'lifestyle-flex', name: '✨ Lifestyle Flex', description: 'Aspirational daily routines' },
    { id: 'storytime', name: '📖 Storytime', description: 'Narrative-driven content' },
    { id: 'business-tips', name: '💼 Business Tips', description: 'Entrepreneurial insights' },
    { id: 'viral-trends', name: '🔥 Viral Trends', description: 'Trending topic analysis' }
  ];

  const supportedPlatforms = [
    { name: 'YouTube', icon: '🎬', color: 'bg-red-500' },
    { name: 'TikTok', icon: '🎵', color: 'bg-black' },
    { name: 'Instagram', icon: '📷', color: 'bg-pink-500' },
    { name: 'Twitter/X', icon: '🐦', color: 'bg-blue-500' },
    { name: 'Facebook', icon: '📘', color: 'bg-blue-600' }
  ];

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!videoUrl.trim()) {
      setError('Please enter a video URL');
      return;
    }

    setLoading(true);
    setError('');
    setResult(null);

    try {
      const response = await fetch(`${process.env.REACT_APP_BACKEND_URL}/api/process-video`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          video_url: videoUrl,
          persona: selectedPersona
        }),
      });

      if (!response.ok) {
        throw new Error('Failed to process video');
      }

      const data = await response.json();
      setResult(data);
    } catch (err) {
      setError(err.message || 'Something went wrong. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const handleFileUpload = (e) => {
    const file = e.target.files[0];
    if (file) {
      // For now, we'll show an error since file upload isn't implemented yet
      setError('Direct file upload coming soon! Please use video URLs for now.');
    }
  };

  const copyToClipboard = (text) => {
    navigator.clipboard.writeText(text);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-900 via-purple-800 to-indigo-900">
      {/* Hero Section */}
      <div className="relative overflow-hidden">
        <div className="absolute inset-0 bg-black/50"></div>
        <div 
          className="absolute inset-0 bg-cover bg-center"
          style={{ backgroundImage: 'url(https://images.pexels.com/photos/5475810/pexels-photo-5475810.jpeg)' }}
        ></div>
        
        <div className="relative z-10 container mx-auto px-4 py-16 sm:py-24">
          <div className="text-center">
            <h1 className="text-4xl sm:text-6xl font-bold text-white mb-6 tracking-tight">
              🔧 <span className="bg-gradient-to-r from-purple-400 to-pink-400 bg-clip-text text-transparent">AyoVirals</span>
            </h1>
            <p className="text-xl sm:text-2xl text-purple-100 mb-8 max-w-3xl mx-auto">
              Hook & Keyword Generator
            </p>
            <p className="text-lg text-purple-200 mb-12 max-w-2xl mx-auto">
              Drop any video link. Get viral-ready hooks and sharp hashtags instantly.
            </p>
            
            {/* Platform Support */}
            <div className="flex flex-wrap justify-center gap-3 mb-12">
              {supportedPlatforms.map((platform) => (
                <div key={platform.name} className="flex items-center space-x-2 px-4 py-2 rounded-full bg-white/10 backdrop-blur-sm">
                  <span className="text-2xl">{platform.icon}</span>
                  <span className="text-white font-medium">{platform.name}</span>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>

      {/* Main Content */}
      <div className="container mx-auto px-4 py-12">
        <div className="max-w-4xl mx-auto">
          {/* Input Section */}
          <div className="bg-white/10 backdrop-blur-lg rounded-2xl p-8 mb-8 border border-white/20">
            <form onSubmit={handleSubmit} className="space-y-6">
              <div>
                <label className="block text-purple-100 text-sm font-medium mb-3">
                  📹 Video URL
                </label>
                <div className="relative">
                  <input
                    type="url"
                    value={videoUrl}
                    onChange={(e) => setVideoUrl(e.target.value)}
                    placeholder="Paste your video URL here..."
                    className="w-full px-4 py-3 bg-white/10 border border-white/20 rounded-xl text-white placeholder-purple-300 focus:outline-none focus:ring-2 focus:ring-purple-400 focus:border-transparent"
                  />
                  <button
                    type="button"
                    onClick={() => fileInputRef.current.click()}
                    className="absolute right-3 top-3 text-purple-300 hover:text-purple-100 transition-colors"
                  >
                    📁
                  </button>
                </div>
                <input
                  type="file"
                  ref={fileInputRef}
                  onChange={handleFileUpload}
                  accept="video/*"
                  className="hidden"
                />
              </div>

              {/* Persona Selection */}
              <div>
                <label className="block text-purple-100 text-sm font-medium mb-3">
                  🎭 Choose Your Persona
                </label>
                <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3">
                  {personas.map((persona) => (
                    <label key={persona.id} className="cursor-pointer">
                      <input
                        type="radio"
                        name="persona"
                        value={persona.id}
                        checked={selectedPersona === persona.id}
                        onChange={(e) => setSelectedPersona(e.target.value)}
                        className="sr-only"
                      />
                      <div className={`p-4 rounded-xl border-2 transition-all ${
                        selectedPersona === persona.id
                          ? 'border-purple-400 bg-purple-400/20'
                          : 'border-white/20 bg-white/5 hover:border-purple-400/50'
                      }`}>
                        <div className="font-medium text-white mb-1">{persona.name}</div>
                        <div className="text-sm text-purple-200">{persona.description}</div>
                      </div>
                    </label>
                  ))}
                </div>
              </div>

              {/* Submit Button */}
              <button
                type="submit"
                disabled={loading}
                className="w-full bg-gradient-to-r from-purple-500 to-pink-500 text-white font-bold py-4 px-8 rounded-xl hover:from-purple-600 hover:to-pink-600 transition-all duration-200 transform hover:scale-105 disabled:opacity-50 disabled:cursor-not-allowed disabled:transform-none"
              >
                {loading ? (
                  <span className="flex items-center justify-center">
                    <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                      <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                      <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                    </svg>
                    Processing...
                  </span>
                ) : (
                  '✨ Generate Viral Content'
                )}
              </button>
            </form>

            {/* Error Message */}
            {error && (
              <div className="mt-4 p-4 bg-red-500/20 border border-red-500/50 rounded-xl text-red-200">
                {error}
              </div>
            )}
          </div>

          {/* Results Section */}
          {result && (
            <div className="bg-white/10 backdrop-blur-lg rounded-2xl p-8 border border-white/20">
              <h2 className="text-2xl font-bold text-white mb-6">🔥 Your Viral Content</h2>
              
              {/* Video Summary */}
              {result.summary && (
                <div className="mb-8">
                  <h3 className="text-lg font-semibold text-purple-100 mb-3">📝 Video Summary</h3>
                  <div className="bg-black/20 rounded-xl p-4">
                    <p className="text-purple-100">{result.summary}</p>
                  </div>
                </div>
              )}

              {/* Hook Options */}
              {result.hooks && result.hooks.length > 0 && (
                <div className="mb-8">
                  <h3 className="text-lg font-semibold text-purple-100 mb-3">🎣 Viral Hooks</h3>
                  <div className="space-y-3">
                    {result.hooks.map((hook, index) => (
                      <div key={index} className="bg-black/20 rounded-xl p-4 flex justify-between items-start">
                        <p className="text-white flex-1 mr-4">{hook}</p>
                        <button
                          onClick={() => copyToClipboard(hook)}
                          className="text-purple-300 hover:text-purple-100 transition-colors"
                        >
                          📋
                        </button>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {/* Keywords & Hashtags */}
              {result.keywords && result.keywords.length > 0 && (
                <div className="mb-8">
                  <h3 className="text-lg font-semibold text-purple-100 mb-3">🔑 Keywords & Hashtags</h3>
                  <div className="bg-black/20 rounded-xl p-4">
                    <div className="flex flex-wrap gap-2">
                      {result.keywords.map((keyword, index) => (
                        <span
                          key={index}
                          className="px-3 py-1 bg-purple-500/30 text-purple-100 rounded-full text-sm cursor-pointer hover:bg-purple-500/50 transition-colors"
                          onClick={() => copyToClipboard(keyword)}
                        >
                          {keyword}
                        </span>
                      ))}
                    </div>
                  </div>
                </div>
              )}

              {/* Copy All Button */}
              <div className="text-center">
                <button
                  onClick={() => {
                    const allContent = [
                      result.summary ? `Summary: ${result.summary}` : '',
                      result.hooks ? `Hooks:\n${result.hooks.join('\n')}` : '',
                      result.keywords ? `Keywords: ${result.keywords.join(' ')}` : ''
                    ].filter(Boolean).join('\n\n');
                    copyToClipboard(allContent);
                  }}
                  className="bg-gradient-to-r from-green-500 to-emerald-500 text-white font-bold py-3 px-6 rounded-xl hover:from-green-600 hover:to-emerald-600 transition-all duration-200"
                >
                  📋 Copy All Content
                </button>
              </div>
            </div>
          )}
        </div>
      </div>

      {/* Footer */}
      <footer className="text-center py-8 text-purple-200">
        <p>🔧 AyoVirals - Your Viral Content Generator</p>
        <p className="text-sm mt-2">Drop any video link → Get viral hooks & keywords instantly</p>
      </footer>
    </div>
  );
};

export default App;