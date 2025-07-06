'use client';

import { useState, useCallback } from 'react';
import Link from 'next/link';
import { Search, Shield, Zap, Brain, FileCode, AlertTriangle, CheckCircle, XCircle } from 'lucide-react';
import CodeEditor from './components/CodeEditor';
import ResultsPanel from './components/ResultsPanel';
import UploadArea from './components/UploadArea';
import ThemeToggle from './components/ThemeToggle';

interface AnalysisResult {
  analysis: {
    detected_language: string;
    lines_of_code: {
      total: number;
      code: number;
      comments: number;
      blank: number;
    };
    complexity_metrics: {
      cyclomatic_complexity: number;
      function_count: number;
      class_count: number;
      nesting_depth?: number;
    };
    structure_analysis?: {
      control_flow?: {
        if_statements?: number;
        loops?: number;
        switches?: number;
        try_catch?: number;
      };
      function_names?: string[];
      imports?: string[];
      variable_names?: string[];
      string_literals?: string[];
    };
    patterns?: {
      algorithm_patterns?: string[];
      data_structures?: string[];
      design_patterns?: string[];
    };
    code_quality?: {
      readability_score?: number;
      maintainability_index?: number;
      code_smells?: string[];
      best_practices?: Record<string, boolean>;
    };
  };
  similarity: {
    matches: Array<{
      id: number;
      similarity_score: number;
      description: string;
      source: string;
      code_snippet: string;
    }>;
    highest_similarity: number;
    risk_level: string;
    total_checked: number;
  };
  timestamp: string;
  language: string;
}

export default function Home() {
  const [code, setCode] = useState('');
  const [language, setLanguage] = useState('python');
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [results, setResults] = useState<AnalysisResult | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [useEnhanced, setUseEnhanced] = useState(false);

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
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50 dark:from-gray-900 dark:via-gray-800 dark:to-gray-900">
      {/* Header */}
      <header className="bg-white/80 dark:bg-gray-800/80 backdrop-blur-sm border-b border-gray-200 dark:border-gray-700 sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="bg-gradient-to-r from-blue-600 to-purple-600 p-2 rounded-lg">
                <Shield className="w-6 h-6 text-white" />
              </div>
              <div>
                <h1 className="text-xl font-bold text-gray-900 dark:text-gray-100">AI-Powered Code Plagiarism Detector</h1>
                <p className="text-sm text-gray-700 dark:text-gray-300">Detect code similarity with advanced AI</p>
              </div>
            </div>
            <div className="flex items-center gap-6">
              <nav className="hidden md:flex items-center gap-4">
                <Link href="/" className="text-gray-700 dark:text-gray-300 hover:text-gray-900 dark:hover:text-gray-100 px-3 py-2 rounded-md text-sm font-medium transition-colors">
                  Analyzer
                </Link>
                <Link href="/demo" className="text-gray-700 dark:text-gray-300 hover:text-gray-900 dark:hover:text-gray-100 px-3 py-2 rounded-md text-sm font-medium transition-colors">
                  Demo
                </Link>
                <Link href="/compare" className="text-gray-700 dark:text-gray-300 hover:text-gray-900 dark:hover:text-gray-100 px-3 py-2 rounded-md text-sm font-medium transition-colors">
                  Compare
                </Link>
              </nav>
              <div className="flex items-center gap-4">
                <div className="flex items-center gap-2">
                  <Brain className="w-4 h-4 text-blue-600" />
                  <span className="text-sm text-gray-700 dark:text-gray-300">AI Enhanced</span>
                </div>
                <div className="flex items-center gap-2">
                  <Zap className="w-4 h-4 text-green-600" />
                  <span className="text-sm text-gray-700 dark:text-gray-300">Real-time Analysis</span>
                </div>
                <ThemeToggle />
              </div>
            </div>
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Input Panel */}
          <div className="space-y-6">
            <div className="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 p-6">
              <div className="flex items-center justify-between mb-4">
                <h2 className="text-lg font-semibold text-gray-900 dark:text-gray-100 flex items-center gap-2">
                  <FileCode className="w-5 h-5" />
                  Code Input
                </h2>
                <div className="flex items-center gap-4">
                  <label className="flex items-center gap-2 text-sm">
                    <input
                      type="checkbox"
                      checked={useEnhanced}
                      onChange={(e) => setUseEnhanced(e.target.checked)}
                      className="rounded border-gray-300 text-blue-600 focus:ring-blue-500"
                    />
                    <span className="text-gray-800 dark:text-gray-200">Enhanced AI Analysis</span>
                  </label>
                  <select
                    value={language}
                    onChange={(e) => setLanguage(e.target.value)}
                    className="px-3 py-1 border border-gray-300 dark:border-gray-600 rounded-md text-sm focus:ring-2 focus:ring-blue-500 focus:border-transparent bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100"
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

              <UploadArea onFileUploadAction={handleFileUpload} />
              
              <div className="mt-4">
                <CodeEditor
                  value={code}
                  onChangeAction={setCode}
                  language={language}
                  placeholder={`Enter your ${language} code here...`}
                />
              </div>

              <div className="mt-6 flex gap-3">
                <button
                  onClick={handleAnalyze}
                  disabled={isAnalyzing || !code.trim()}
                  className="flex-1 bg-gradient-to-r from-blue-600 to-purple-600 text-white px-6 py-3 rounded-lg font-medium hover:from-blue-700 hover:to-purple-700 disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-200 flex items-center justify-center gap-2"
                >
                  {isAnalyzing ? (
                    <>
                      <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin" />
                      Analyzing...
                    </>
                  ) : (
                    <>
                      <Search className="w-4 h-4" />
                      Analyze Code
                    </>
                  )}
                </button>
              </div>

              {error && (
                <div className="mt-4 p-4 bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg">
                  <div className="flex items-center gap-2">
                    <XCircle className="w-5 h-5 text-red-600 dark:text-red-400" />
                    <p className="text-red-800 dark:text-red-200 font-medium">Error</p>
                  </div>
                  <p className="text-red-700 dark:text-red-300 mt-1">{error}</p>
                </div>
              )}
            </div>

            {/* Quick Stats */}
            {results && (
              <div className="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 p-6">
                <h3 className="text-lg font-semibold text-gray-900 dark:text-gray-100 mb-4">Code Analysis Summary</h3>
                <div className="grid grid-cols-2 gap-4 mb-4">
                  <div className="bg-blue-50 dark:bg-blue-900/20 p-4 rounded-lg">
                    <div className="text-2xl font-bold text-blue-600 dark:text-blue-400">
                      {results.analysis.lines_of_code.total}
                    </div>
                    <div className="text-sm text-blue-700 dark:text-blue-300">Total Lines</div>
                  </div>
                  <div className="bg-purple-50 dark:bg-purple-900/20 p-4 rounded-lg">
                    <div className="text-2xl font-bold text-purple-600 dark:text-purple-400">
                      {results.analysis.complexity_metrics.function_count}
                    </div>
                    <div className="text-sm text-purple-700 dark:text-purple-300">Functions</div>
                  </div>
                  <div className="bg-green-50 dark:bg-green-900/20 p-4 rounded-lg">
                    <div className="text-2xl font-bold text-green-600 dark:text-green-400">
                      {results.analysis.detected_language.toUpperCase()}
                    </div>
                    <div className="text-sm text-green-700 dark:text-green-300">Language</div>
                  </div>
                  <div className="bg-gray-50 dark:bg-gray-700 p-4 rounded-lg">
                    <div className="text-2xl font-bold text-gray-600 dark:text-gray-300">
                      {results.similarity.total_checked}
                    </div>
                    <div className="text-sm text-gray-700 dark:text-gray-400">Compared</div>
                  </div>
                </div>
                
                {/* Code Structure Details */}
                <div className="border-t dark:border-gray-700 pt-4">
                  <h4 className="font-medium text-gray-900 dark:text-gray-100 mb-3">Code Structure</h4>
                  <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm">
                    <div>
                      <span className="text-gray-700 dark:text-gray-300">Code Lines:</span>
                      <span className="font-medium ml-1 text-gray-900 dark:text-gray-100">{results.analysis.lines_of_code.code}</span>
                    </div>
                    <div>
                      <span className="text-gray-700 dark:text-gray-300">Comments:</span>
                      <span className="font-medium ml-1 text-gray-900 dark:text-gray-100">{results.analysis.lines_of_code.comments}</span>
                    </div>
                    <div>
                      <span className="text-gray-700 dark:text-gray-300">Complexity:</span>
                      <span className="font-medium ml-1 text-gray-900 dark:text-gray-100">{results.analysis.complexity_metrics.cyclomatic_complexity}</span>
                    </div>
                    <div>
                      <span className="text-gray-700 dark:text-gray-300">Classes:</span>
                      <span className="font-medium ml-1 text-gray-900 dark:text-gray-100">{results.analysis.complexity_metrics.class_count}</span>
                    </div>
                  </div>
                  
                  {/* Control Flow Analysis */}
                  {results.analysis.structure_analysis && (
                    <div className="mt-3 pt-3 border-t dark:border-gray-700">
                      <h5 className="font-medium text-gray-900 dark:text-gray-100 mb-2">Control Flow</h5>
                      <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm">
                        <div>
                          <span className="text-gray-700 dark:text-gray-300">If Statements:</span>
                          <span className="font-medium ml-1 text-gray-900 dark:text-gray-100">{results.analysis.structure_analysis.control_flow?.if_statements || 0}</span>
                        </div>
                        <div>
                          <span className="text-gray-700 dark:text-gray-300">Loops:</span>
                          <span className="font-medium ml-1 text-gray-900 dark:text-gray-100">{results.analysis.structure_analysis.control_flow?.loops || 0}</span>
                        </div>
                        <div>
                          <span className="text-gray-700 dark:text-gray-300">Try/Catch:</span>
                          <span className="font-medium ml-1 text-gray-900 dark:text-gray-100">{results.analysis.structure_analysis.control_flow?.try_catch || 0}</span>
                        </div>
                        <div>
                          <span className="text-gray-700 dark:text-gray-300">Nesting:</span>
                          <span className="font-medium ml-1 text-gray-900 dark:text-gray-100">{results.analysis.complexity_metrics.nesting_depth || 0}</span>
                        </div>
                      </div>
                    </div>
                  )}
                </div>
              </div>
            )}
          </div>

          {/* Results Panel */}
          <div className="space-y-6">
            {results ? (
              <>
                {/* Risk Level Card */}
                <div className="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 p-6">
                  <div className="flex items-center justify-between mb-4">
                    <h3 className="text-lg font-semibold text-gray-900 dark:text-gray-100">Risk Assessment</h3>
                    {getRiskBadge(results.similarity.risk_level)}
                  </div>
                  
                  <div className="mb-4">
                    <div className="flex justify-between text-sm mb-2">
                      <span className="text-gray-700 dark:text-gray-300">Highest Similarity</span>
                      <span className="font-medium text-gray-900 dark:text-gray-100">{(results.similarity.highest_similarity * 100).toFixed(1)}%</span>
                    </div>
                    <div className="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-3">
                      <div
                        className={`h-3 rounded-full transition-all duration-300 ${
                          results.similarity.highest_similarity > 0.8
                            ? 'bg-red-500'
                            : results.similarity.highest_similarity > 0.6
                            ? 'bg-yellow-500'
                            : 'bg-green-500'
                        }`}
                        style={{ width: `${results.similarity.highest_similarity * 100}%` }}
                      />
                    </div>
                  </div>

                  <div className="grid grid-cols-2 gap-4 text-sm">
                    <div>
                      <span className="text-gray-700 dark:text-gray-300">Matches Found:</span>
                      <span className="font-medium ml-2 text-gray-900 dark:text-gray-100">{results.similarity.matches.length}</span>
                    </div>
                    <div>
                      <span className="text-gray-700 dark:text-gray-300">Database Size:</span>
                      <span className="font-medium ml-2 text-gray-900 dark:text-gray-100">{results.similarity.total_checked}</span>
                    </div>
                  </div>
                </div>

                <ResultsPanel results={results} />
              </>
            ) : (
              <div className="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 p-12 text-center">
                <div className="w-16 h-16 bg-gray-100 dark:bg-gray-700 rounded-full flex items-center justify-center mx-auto mb-4">
                  <Search className="w-8 h-8 text-gray-400 dark:text-gray-500" />
                </div>
                <h3 className="text-lg font-medium text-gray-900 dark:text-gray-100 mb-2">Ready to Analyze</h3>
                <p className="text-gray-700 dark:text-gray-300">
                  Enter your code above and click &ldquo;Analyze Code&rdquo; to detect potential plagiarism and get detailed insights.
                </p>
              </div>
            )}
          </div>
        </div>
      </main>
    </div>
  );
}
