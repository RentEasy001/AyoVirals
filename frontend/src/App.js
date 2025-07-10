import React, { useState, useRef, useEffect } from 'react';
import './App.css';

const App = () => {
  const [videoUrl, setVideoUrl] = useState('');
  const [selectedPersona, setSelectedPersona] = useState('nyc-drama');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState('');
  const [processingStage, setProcessingStage] = useState('');
  const [progress, setProgress] = useState(0);
  const [recentVideos, setRecentVideos] = useState([]);
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
    { name: 'YouTube', icon: '🎬', color: 'bg-red-500', limit: 100 },
    { name: 'TikTok', icon: '🎵', color: 'bg-black', limit: 150 },
    { name: 'Instagram', icon: '📷', color: 'bg-pink-500', limit: 125 },
    { name: 'Twitter/X', icon: '🐦', color: 'bg-blue-500', limit: 280 },
    { name: 'Facebook', icon: '📘', color: 'bg-blue-600', limit: 200 }
  ];

  const processingStages = [
    { stage: 'initializing', label: 'Initializing...', icon: '🔄' },
    { stage: 'downloading', label: 'Downloading Video...', icon: '📥' },
    { stage: 'transcribing', label: 'Transcribing Audio...', icon: '🎧' },
    { stage: 'analyzing', label: 'Analyzing Content...', icon: '🧠' },
    { stage: 'generating', label: 'Generating Hooks...', icon: '🎣' },
    { stage: 'complete', label: 'Complete!', icon: '✅' }
  ];

  // Load recent videos from localStorage
  useEffect(() => {
    const saved = localStorage.getItem('ayovirals-recent');
    if (saved) {
      setRecentVideos(JSON.parse(saved));
    }
  }, []);

  // Save recent videos to localStorage
  const saveRecentVideo = (url, persona, result) => {
    const video = {
      url,
      persona,
      result,
      timestamp: new Date().toISOString(),
      id: Date.now()
    };
    
    const updated = [video, ...recentVideos.filter(v => v.url !== url)].slice(0, 5);
    setRecentVideos(updated);
    localStorage.setItem('ayovirals-recent', JSON.stringify(updated));
  };

  // Calculate viral score for hooks
  const calculateViralScore = (hook) => {
    let score = 50; // Base score
    
    // Power words boost
    const powerWords = ['shocking', 'unbelievable', 'secret', 'truth', 'exposed', 'crazy', 'insane', 'viral', 'trending'];
    powerWords.forEach(word => {
      if (hook.toLowerCase().includes(word)) score += 10;
    });
    
    // Question format boost
    if (hook.includes('?')) score += 15;
    
    // Urgency words
    const urgencyWords = ['now', 'today', 'immediately', 'must', 'need', 'can\'t'];
    urgencyWords.forEach(word => {
      if (hook.toLowerCase().includes(word)) score += 8;
    });
    
    // Emotional triggers
    const emotionalWords = ['amazing', 'incredible', 'shocking', 'mind-blowing', 'life-changing'];
    emotionalWords.forEach(word => {
      if (hook.toLowerCase().includes(word)) score += 12;
    });
    
    // Personal pronouns
    if (hook.toLowerCase().includes('you') || hook.toLowerCase().includes('your')) score += 10;
    
    // Length optimization (80-100 chars ideal)
    const idealLength = hook.length >= 80 && hook.length <= 100;
    if (idealLength) score += 10;
    
    return Math.min(Math.max(score, 0), 100);
  };

  // Get fire emoji based on score
  const getFireEmoji = (score) => {
    if (score >= 90) return '🔥🔥🔥';
    if (score >= 70) return '🔥🔥';
    if (score >= 50) return '🔥';
    return '❄️';
  };

  // Get character count status
  const getCharacterStatus = (text, platform) => {
    const limit = supportedPlatforms.find(p => p.name === platform)?.limit || 200;
    const length = text.length;
    
    if (length <= limit) return { status: 'good', color: 'text-green-400' };
    if (length <= limit * 1.2) return { status: 'warning', color: 'text-yellow-400' };
    return { status: 'danger', color: 'text-red-400' };
  };

  const simulateProgress = () => {
    const stages = ['initializing', 'downloading', 'transcribing', 'analyzing', 'generating'];
    let currentStage = 0;
    let currentProgress = 0;
    
    const interval = setInterval(() => {
      if (currentStage < stages.length) {
        setProcessingStage(stages[currentStage]);
        setProgress(currentProgress);
        
        // Simulate realistic timing
        const stageIncrements = [20, 30, 25, 15, 10]; // Different speeds for each stage
        currentProgress += stageIncrements[currentStage] / 10;
        
        if (currentProgress >= (currentStage + 1) * 20) {
          currentStage++;
          currentProgress = (currentStage) * 20;
        }
      } else {
        setProcessingStage('complete');
        setProgress(100);
        clearInterval(interval);
      }
    }, 200);
    
    return interval;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!videoUrl.trim()) {
      setError('Please enter a video URL');
      return;
    }

    setLoading(true);
    setError('');
    setResult(null);
    setProgress(0);

    // Start progress simulation
    const progressInterval = simulateProgress();

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
      
      // Add viral scores to hooks
      const hooksWithScores = data.hooks.map(hook => ({
        text: hook,
        score: calculateViralScore(hook),
        fireEmoji: getFireEmoji(calculateViralScore(hook))
      }));
      
      const enhancedResult = {
        ...data,
        hooks: hooksWithScores
      };
      
      setResult(enhancedResult);
      saveRecentVideo(videoUrl, selectedPersona, enhancedResult);
      
      // Complete progress
      clearInterval(progressInterval);
      setProcessingStage('complete');
      setProgress(100);
      
    } catch (err) {
      clearInterval(progressInterval);
      setError(err.message || 'Something went wrong. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const handleFileUpload = (e) => {
    const file = e.target.files[0];
    if (file) {
      setError('Direct file upload coming soon! Please use video URLs for now.');
    }
  };

  const copyToClipboard = (text) => {
    navigator.clipboard.writeText(text);
  };

  const loadRecentVideo = (recent) => {
    setVideoUrl(recent.url);
    setSelectedPersona(recent.persona);
    setResult(recent.result);
    setError('');
  };

  const clearHistory = () => {
    setRecentVideos([]);
    localStorage.removeItem('ayovirals-recent');
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
              Hook & Keyword Generator 2.0
            </p>
            <p className="text-lg text-purple-200 mb-12 max-w-2xl mx-auto">
              Drop any video link. Get viral-ready hooks with AI-powered scoring.
            </p>
            
            {/* Platform Support */}
            <div className="flex flex-wrap justify-center gap-3 mb-12">
              {supportedPlatforms.map((platform) => (
                <div key={platform.name} className="flex items-center space-x-2 px-4 py-2 rounded-full bg-white/10 backdrop-blur-sm">
                  <span className="text-2xl">{platform.icon}</span>
                  <span className="text-white font-medium">{platform.name}</span>
                  <span className="text-xs text-purple-200">({platform.limit})</span>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>

      {/* Recent Videos */}
      {recentVideos.length > 0 && (
        <div className="container mx-auto px-4 py-8">
          <div className="max-w-4xl mx-auto">
            <div className="flex justify-between items-center mb-4">
              <h2 className="text-white text-lg font-semibold">🕒 Recent Videos</h2>
              <button
                onClick={clearHistory}
                className="text-purple-300 hover:text-purple-100 text-sm"
              >
                Clear History
              </button>
            </div>
            <div className="flex gap-2 overflow-x-auto pb-2">
              {recentVideos.map((recent) => (
                <div
                  key={recent.id}
                  onClick={() => loadRecentVideo(recent)}
                  className="flex-shrink-0 bg-white/10 backdrop-blur-sm rounded-lg p-3 cursor-pointer hover:bg-white/20 transition-colors min-w-[200px]"
                >
                  <div className="text-white text-sm font-medium truncate">{recent.url}</div>
                  <div className="text-purple-200 text-xs mt-1">{personas.find(p => p.id === recent.persona)?.name}</div>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}

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

            {/* Progress Indicator */}
            {loading && (
              <div className="mt-6 p-4 bg-black/20 rounded-xl">
                <div className="flex items-center justify-between mb-2">
                  <div className="flex items-center space-x-2">
                    <span className="text-2xl">
                      {processingStages.find(s => s.stage === processingStage)?.icon || '🔄'}
                    </span>
                    <span className="text-white font-medium">
                      {processingStages.find(s => s.stage === processingStage)?.label || 'Processing...'}
                    </span>
                  </div>
                  <span className="text-purple-200 text-sm">{progress.toFixed(0)}%</span>
                </div>
                <div className="w-full bg-purple-900/50 rounded-full h-2">
                  <div 
                    className="bg-gradient-to-r from-purple-400 to-pink-400 h-2 rounded-full transition-all duration-500"
                    style={{ width: `${progress}%` }}
                  ></div>
                </div>
              </div>
            )}

            {/* Error Message */}
            {error && (
              <div className="mt-4 p-4 bg-red-500/20 border border-red-500/50 rounded-xl text-red-200">
                {error}
              </div>
            )}
          </div>

          {/* Results Section */}
          {result && (
            <div className="bg-white/10 backdrop-blur-lg rounded-2xl p-8 border border-white/20 results-section">
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

              {/* Hook Options with Scores */}
              {result.hooks && result.hooks.length > 0 && (
                <div className="mb-8">
                  <h3 className="text-lg font-semibold text-purple-100 mb-3">🎣 Viral Hooks</h3>
                  <div className="space-y-3">
                    {result.hooks.map((hookData, index) => (
                      <div key={index} className="bg-black/20 rounded-xl p-4">
                        <div className="flex justify-between items-start mb-2">
                          <div className="flex items-center space-x-2">
                            <span className="text-2xl">{hookData.fireEmoji}</span>
                            <span className="text-purple-300 font-medium">
                              Score: {hookData.score}/100
                            </span>
                          </div>
                          <button
                            onClick={() => copyToClipboard(hookData.text)}
                            className="text-purple-300 hover:text-purple-100 transition-colors"
                          >
                            📋
                          </button>
                        </div>
                        <p className="text-white flex-1 mb-3">{hookData.text}</p>
                        
                        {/* Character counts for different platforms */}
                        <div className="flex flex-wrap gap-2 mt-2">
                          {supportedPlatforms.map((platform) => {
                            const charStatus = getCharacterStatus(hookData.text, platform.name);
                            return (
                              <span
                                key={platform.name}
                                className={`text-xs px-2 py-1 rounded-full bg-black/20 ${charStatus.color}`}
                              >
                                {platform.icon} {hookData.text.length}/{platform.limit}
                              </span>
                            );
                          })}
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {/* Enhanced Keywords & Hashtags */}
              {result.keywords && result.keywords.length > 0 && (
                <div className="mb-8">
                  <h3 className="text-lg font-semibold text-purple-100 mb-3">🔑 Smart Keywords & Hashtags</h3>
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
                      result.hooks ? `Hooks:\n${result.hooks.map(h => `${h.fireEmoji} ${h.text} (Score: ${h.score}/100)`).join('\n')}` : '',
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
        <p>🔧 AyoVirals 2.0 - AI-Powered Viral Content Generator</p>
        <p className="text-sm mt-2">Drop any video link → Get scored hooks & smart keywords instantly</p>
      </footer>
    </div>
  );
};

export default App;