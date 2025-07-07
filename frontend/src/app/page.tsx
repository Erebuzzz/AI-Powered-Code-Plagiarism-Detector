'use client';

import { useState, useCallback } from 'react';
import Link from 'next/link';
import { Search, Shield, Zap, Brain, FileCode, AlertTriangle, CheckCircle, XCircle } from 'lucide-react';
import CodeEditor from './components/CodeEditor';
import ResultsPanel, { AnalysisResult } from './components/ResultsPanel';
import UploadArea from './components/UploadArea';
import ThemeToggle from './components/ThemeToggle';

export default function Home() {
  const [code, setCode] = useState<string>('');
  const [language, setLanguage] = useState<string>('python');
  const [isAnalyzing, setIsAnalyzing] = useState<boolean>(false);
  const [results, setResults] = useState<AnalysisResult | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [useEnhanced, setUseEnhanced] = useState<boolean>(false);

  const handleAnalyze = useCallback(async () => {
    if (!code.trim()) {
      setError('Please enter some code to analyze');
      return;
    }

    setIsAnalyzing(true);
    setError(null);
    setResults(null);

    try {
      const endpoint = useEnhanced ? '/api/analyze-enhanced' : '/api/analyze';
      const backendUrl = process.env.NEXT_PUBLIC_BACKEND_URL || 'http://localhost:5001';
      const response = await fetch(`${backendUrl}${endpoint}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          code,
          language,
          checkDatabase: true,
          useCohere: useEnhanced,
        }),
      });

      if (!response.ok) {
        throw new Error(`Analysis failed: ${response.statusText}`);
      }

      const data = await response.json();
      setResults(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred during analysis');
    } finally {
      setIsAnalyzing(false);
    }
  }, [code, language, useEnhanced]);

  const handleFileUpload = useCallback((content: string, filename: string) => {
    setCode(content);
    // Auto-detect language from filename
    const ext = filename.split('.').pop()?.toLowerCase();
    const langMap: Record<string, string> = {
      'py': 'python',
      'js': 'javascript',
      'ts': 'typescript',
      'tsx': 'typescript',
      'jsx': 'javascript',
      'java': 'java',
      'cpp': 'cpp',
      'c': 'c',
      'cs': 'csharp',
      'php': 'php',
      'rb': 'ruby',
      'go': 'go',
      'rs': 'rust',
      'swift': 'swift',
      'kt': 'kotlin',
    };
    if (ext && langMap[ext]) {
      setLanguage(langMap[ext]);
    }
  }, []);

  const getRiskBadge = (riskLevel: string) => {
    const configs = {
      low: { color: 'bg-green-100 text-green-800', icon: CheckCircle },
      medium: { color: 'bg-yellow-100 text-yellow-800', icon: AlertTriangle },
      high: { color: 'bg-red-100 text-red-800', icon: XCircle },
      very_high: { color: 'bg-red-200 text-red-900', icon: XCircle },
    };
    const config = configs[riskLevel as keyof typeof configs] || configs.low;
    const Icon = config.icon;
    return (
      <span className={`inline-flex items-center gap-1 px-2 py-1 rounded-full text-xs font-medium ${config.color}`}>
        <Icon size={12} />
        {riskLevel.replace('_', ' ').toUpperCase()}
      </span>
    );
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-indigo-100 dark:from-gray-950 dark:via-blue-950 dark:to-indigo-950">
      {/* Modern Header */}
      <header className="bg-white/70 dark:bg-gray-900/70 backdrop-blur-md border-b border-white/20 dark:border-gray-800/20 sticky top-0 z-50">
        <div className="max-w-[1400px] mx-auto px-6 lg:px-8 py-6">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-4">
              <div className="relative">
                <div className="absolute inset-0 bg-gradient-to-r from-blue-600 to-purple-600 rounded-2xl blur-sm opacity-75"></div>
                <div className="relative bg-gradient-to-r from-blue-600 to-purple-600 p-3 rounded-2xl">
                  <Shield className="w-7 h-7 text-white" />
                </div>
              </div>
              <div>
                <h1 className="text-2xl font-bold bg-gradient-to-r from-gray-900 to-gray-700 dark:from-white dark:to-gray-300 bg-clip-text text-transparent">
                  AI Plagiarism Detector
                </h1>
                <p className="text-sm text-gray-600 dark:text-gray-400 font-medium">Advanced code similarity analysis</p>
              </div>
            </div>
            
            <div className="flex items-center gap-6">
              <nav className="hidden md:flex items-center gap-1">
                <Link href="/" className="px-4 py-2 rounded-xl text-sm font-medium bg-blue-50 dark:bg-blue-900/30 text-blue-700 dark:text-blue-300 border border-blue-200 dark:border-blue-800">
                  Analyzer
                </Link>
                <Link href="/demo" className="px-4 py-2 rounded-xl text-sm font-medium text-gray-600 dark:text-gray-400 hover:bg-gray-50 dark:hover:bg-gray-800 transition-colors">
                  Demo
                </Link>
                <Link href="/compare" className="px-4 py-2 rounded-xl text-sm font-medium text-gray-600 dark:text-gray-400 hover:bg-gray-50 dark:hover:bg-gray-800 transition-colors">
                  Compare
                </Link>
              </nav>
              
              <div className="flex items-center gap-3">
                <div className="hidden lg:flex items-center gap-4">
                  <div className="flex items-center gap-2 px-3 py-1.5 bg-emerald-50 dark:bg-emerald-900/20 rounded-full">
                    <Brain className="w-4 h-4 text-emerald-600 dark:text-emerald-400" />
                    <span className="text-xs font-medium text-emerald-700 dark:text-emerald-300">AI Enhanced</span>
                  </div>
                  <div className="flex items-center gap-2 px-3 py-1.5 bg-amber-50 dark:bg-amber-900/20 rounded-full">
                    <Zap className="w-4 h-4 text-amber-600 dark:text-amber-400" />
                    <span className="text-xs font-medium text-amber-700 dark:text-amber-300">Real-time</span>
                  </div>
                </div>
                <ThemeToggle />
              </div>
            </div>
          </div>
        </div>
      </header>

      {/* Hero Section */}
      <div className="max-w-[1400px] mx-auto px-6 lg:px-8 pt-12 pb-8">
        <div className="text-center mb-16">
          <h2 className="text-4xl lg:text-6xl font-bold bg-gradient-to-r from-blue-600 via-purple-600 to-indigo-600 bg-clip-text text-transparent mb-6">
            Detect Code Plagiarism
          </h2>
          <p className="text-xl text-gray-600 dark:text-gray-400 max-w-3xl mx-auto leading-relaxed">
            Upload your code and get instant similarity analysis powered by advanced AI algorithms
          </p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 max-w-6xl mx-auto">
          {/* Input Panel - Enhanced */}
          <div className="space-y-8">
            {/* Main Input Card */}
            <div className="bg-white/80 dark:bg-gray-900/80 backdrop-blur-sm rounded-3xl border border-white/60 dark:border-gray-800/60 p-8 shadow-xl shadow-blue-500/5">
              {/* Card Header */}
              <div className="flex items-center justify-between mb-8">
                <div className="flex items-center gap-3">
                  <div className="p-2 bg-gradient-to-r from-blue-500 to-purple-500 rounded-xl">
                    <FileCode className="w-5 h-5 text-white" />
                  </div>
                  <h3 className="text-xl font-semibold text-gray-900 dark:text-gray-100">Code Analysis</h3>
                </div>
                
                {/* Enhanced Toggle and Language Selector */}
                <div className="flex items-center gap-4">
                  <label className="flex items-center gap-3 cursor-pointer">
                    <input
                      type="checkbox"
                      checked={useEnhanced}
                      onChange={(e) => setUseEnhanced(e.target.checked)}
                      className="w-4 h-4 rounded border-gray-300 text-blue-600 focus:ring-blue-500 focus:ring-offset-0"
                    />
                    <span className="text-sm font-medium text-gray-700 dark:text-gray-300">Enhanced AI</span>
                  </label>
                  
                  <select
                    value={language}
                    onChange={(e) => setLanguage(e.target.value)}
                    className="px-4 py-2 bg-gray-50 dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-xl text-sm font-medium text-gray-900 dark:text-gray-100 focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-colors"
                  >
                    <option value="python">Python</option>
                    <option value="javascript">JavaScript</option>
                    <option value="typescript">TypeScript</option>
                    <option value="java">Java</option>
                    <option value="cpp">C++</option>
                    <option value="c">C</option>
                    <option value="csharp">C#</option>
                    <option value="php">PHP</option>
                    <option value="ruby">Ruby</option>
                    <option value="go">Go</option>
                    <option value="rust">Rust</option>
                    <option value="swift">Swift</option>
                    <option value="kotlin">Kotlin</option>
                  </select>
                </div>
              </div>

              {/* Upload Area */}
              <div className="mb-6">
                <UploadArea onFileUploadAction={handleFileUpload} />
              </div>
              
              {/* Code Editor */}
              <div className="mb-8">
                <CodeEditor
                  value={code}
                  onChangeAction={setCode}
                  language={language}
                  placeholder={`Paste your ${language} code here or drag and drop a file above...`}
                />
              </div>

              {/* Analyze Button */}
              <button
                onClick={handleAnalyze}
                disabled={isAnalyzing || !code.trim()}
                className="w-full bg-gradient-to-r from-blue-600 via-purple-600 to-indigo-600 hover:from-blue-700 hover:via-purple-700 hover:to-indigo-700 text-white px-8 py-4 rounded-2xl font-semibold disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-300 flex items-center justify-center gap-3 shadow-lg shadow-blue-500/25 hover:shadow-xl hover:shadow-blue-500/30"
              >
                {isAnalyzing ? (
                  <>
                    <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin" />
                    <span>Analyzing Code...</span>
                  </>
                ) : (
                  <>
                    <Search className="w-5 h-5" />
                    <span>Analyze for Plagiarism</span>
                  </>
                )}
              </button>

              {/* Error Display */}
              {error && (
                <div className="mt-6 p-4 bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-2xl">
                  <div className="flex items-center gap-3">
                    <div className="p-1 bg-red-100 dark:bg-red-900/40 rounded-lg">
                      <XCircle className="w-4 h-4 text-red-600 dark:text-red-400" />
                    </div>
                    <div>
                      <p className="font-medium text-red-800 dark:text-red-200">Analysis Error</p>
                      <p className="text-sm text-red-700 dark:text-red-300 mt-1">{error}</p>
                    </div>
                  </div>
                </div>
              )}
            </div>
          </div>

          {/* Results Panel - Enhanced */}
          <div className="space-y-8">
            {results ? (
              <>
                {/* Risk Assessment Card */}
                <div className="bg-white/80 dark:bg-gray-900/80 backdrop-blur-sm rounded-3xl border border-white/60 dark:border-gray-800/60 p-8 shadow-xl shadow-purple-500/5">
                  <div className="flex items-center justify-between mb-6">
                    <h3 className="text-xl font-semibold text-gray-900 dark:text-gray-100">Risk Assessment</h3>
                    {getRiskBadge(results.similarity.risk_level)}
                  </div>
                  
                  <div className="mb-6">
                    <div className="flex justify-between text-sm mb-3">
                      <span className="font-medium text-gray-700 dark:text-gray-300">Similarity Score</span>
                      <span className="font-bold text-gray-900 dark:text-gray-100">{(results.similarity.highest_similarity * 100).toFixed(1)}%</span>
                    </div>
                    <div className="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-3 overflow-hidden">
                      <div
                        className={`h-full rounded-full transition-all duration-1000 ${
                          results.similarity.highest_similarity > 0.8
                            ? 'bg-gradient-to-r from-red-500 to-red-600'
                            : results.similarity.highest_similarity > 0.6
                            ? 'bg-gradient-to-r from-yellow-500 to-orange-500'
                            : 'bg-gradient-to-r from-green-500 to-emerald-500'
                        }`}
                        style={{ width: `${results.similarity.highest_similarity * 100}%` }}
                      />
                    </div>
                  </div>

                  <div className="grid grid-cols-2 gap-4">
                    <div className="text-center p-4 bg-blue-50 dark:bg-blue-900/20 rounded-2xl">
                      <div className="text-2xl font-bold text-blue-600 dark:text-blue-400">{results.similarity.matches.length}</div>
                      <div className="text-xs font-medium text-blue-700 dark:text-blue-300">Matches Found</div>
                    </div>
                    <div className="text-center p-4 bg-purple-50 dark:bg-purple-900/20 rounded-2xl">
                      <div className="text-2xl font-bold text-purple-600 dark:text-purple-400">{results.similarity.total_checked}</div>
                      <div className="text-xs font-medium text-purple-700 dark:text-purple-300">Sources Checked</div>
                    </div>
                  </div>
                </div>

                {/* Code Metrics Card */}
                <div className="bg-white/80 dark:bg-gray-900/80 backdrop-blur-sm rounded-3xl border border-white/60 dark:border-gray-800/60 p-8 shadow-xl shadow-indigo-500/5">
                  <h3 className="text-xl font-semibold text-gray-900 dark:text-gray-100 mb-6">Code Metrics</h3>
                  
                  <div className="grid grid-cols-2 gap-4 mb-6">
                    <div className="text-center p-4 bg-emerald-50 dark:bg-emerald-900/20 rounded-2xl">
                      <div className="text-2xl font-bold text-emerald-600 dark:text-emerald-400">{results.analysis.lines_of_code.total}</div>
                      <div className="text-xs font-medium text-emerald-700 dark:text-emerald-300">Total Lines</div>
                    </div>
                    <div className="text-center p-4 bg-amber-50 dark:bg-amber-900/20 rounded-2xl">
                      <div className="text-2xl font-bold text-amber-600 dark:text-amber-400">{results.analysis.complexity_metrics.function_count}</div>
                      <div className="text-xs font-medium text-amber-700 dark:text-amber-300">Functions</div>
                    </div>
                  </div>

                  <div className="space-y-3">
                    <div className="flex justify-between items-center py-2 px-3 bg-gray-50 dark:bg-gray-800/50 rounded-xl">
                      <span className="text-sm font-medium text-gray-700 dark:text-gray-300">Language</span>
                      <span className="text-sm font-bold text-gray-900 dark:text-gray-100 uppercase">{results.analysis.detected_language}</span>
                    </div>
                    <div className="flex justify-between items-center py-2 px-3 bg-gray-50 dark:bg-gray-800/50 rounded-xl">
                      <span className="text-sm font-medium text-gray-700 dark:text-gray-300">Complexity</span>
                      <span className="text-sm font-bold text-gray-900 dark:text-gray-100">{results.analysis.complexity_metrics.cyclomatic_complexity}</span>
                    </div>
                    <div className="flex justify-between items-center py-2 px-3 bg-gray-50 dark:bg-gray-800/50 rounded-xl">
                      <span className="text-sm font-medium text-gray-700 dark:text-gray-300">Comments</span>
                      <span className="text-sm font-bold text-gray-900 dark:text-gray-100">{results.analysis.lines_of_code.comments}</span>
                    </div>
                  </div>
                </div>

                {/* Full Results Panel */}
                <ResultsPanel results={results} />
              </>
            ) : (
              <div className="bg-white/80 dark:bg-gray-900/80 backdrop-blur-sm rounded-3xl border border-white/60 dark:border-gray-800/60 p-12 text-center shadow-xl">
                <div className="w-20 h-20 bg-gradient-to-r from-blue-500 to-purple-500 rounded-full flex items-center justify-center mx-auto mb-6">
                  <Search className="w-10 h-10 text-white" />
                </div>
                <h3 className="text-xl font-semibold text-gray-900 dark:text-gray-100 mb-3">Ready to Analyze</h3>
                <p className="text-gray-600 dark:text-gray-400 leading-relaxed">
                  Upload your code file or paste it in the editor above, then click &ldquo;Analyze for Plagiarism&rdquo; to get detailed similarity insights and risk assessment.
                </p>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
