'use client';

import { useState } from 'react';
import { ChevronDown, ChevronRight, AlertTriangle, CheckCircle, Eye, Code, BarChart3 } from 'lucide-react';
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter';
import { oneLight, oneDark } from 'react-syntax-highlighter/dist/esm/styles/prism';
import { useTheme } from '../contexts/ThemeContext';

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

interface ResultsPanelProps {
  results: AnalysisResult;
}

export default function ResultsPanel({ results }: ResultsPanelProps) {
  const [expandedMatch, setExpandedMatch] = useState<number | null>(null);
  const [activeTab, setActiveTab] = useState<'matches' | 'details' | 'metrics'>('matches');
  const { theme } = useTheme();

  const getSimilarityColor = (score: number) => {
    if (score > 0.8) return 'text-red-600 bg-red-50 dark:text-red-400 dark:bg-red-900/20';
    if (score > 0.6) return 'text-yellow-600 bg-yellow-50 dark:text-yellow-400 dark:bg-yellow-900/20';
    return 'text-green-600 bg-green-50 dark:text-green-400 dark:bg-green-900/20';
  };

  const getSimilarityIcon = (score: number) => {
    if (score > 0.8) return <AlertTriangle className="w-4 h-4" />;
    return <CheckCircle className="w-4 h-4" />;
  };

  const formatPercentage = (score: number) => `${(score * 100).toFixed(1)}%`;

  return (
    <div className="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700">
      {/* Tab Navigation */}
      <div className="border-b border-gray-200 dark:border-gray-700">
        <nav className="flex">
          <button
            onClick={() => setActiveTab('matches')}
            className={`px-6 py-4 text-sm font-medium border-b-2 transition-colors ${
              activeTab === 'matches'
                ? 'border-blue-500 text-blue-600 dark:text-blue-400'
                : 'border-transparent text-gray-600 dark:text-gray-400 hover:text-gray-800 dark:hover:text-gray-200'
            }`}
          >
            <div className="flex items-center gap-2">
              <Eye className="w-4 h-4" />
              Similarity Matches ({results.similarity.matches.length})
            </div>
          </button>
          <button
            onClick={() => setActiveTab('details')}
            className={`px-6 py-4 text-sm font-medium border-b-2 transition-colors ${
              activeTab === 'details'
                ? 'border-blue-500 text-blue-600'
                : 'border-transparent text-gray-500 hover:text-gray-700'
            }`}
          >
            <div className="flex items-center gap-2">
              <Code className="w-4 h-4" />
              Code Details
            </div>
          </button>
          <button
            onClick={() => setActiveTab('metrics')}
            className={`px-6 py-4 text-sm font-medium border-b-2 transition-colors ${
              activeTab === 'metrics'
                ? 'border-blue-500 text-blue-600 dark:text-blue-400'
                : 'border-transparent text-gray-600 dark:text-gray-400 hover:text-gray-800 dark:hover:text-gray-200'
            }`}
          >
            <div className="flex items-center gap-2">
              <BarChart3 className="w-4 h-4" />
              Metrics
            </div>
          </button>
        </nav>
      </div>

      <div className="p-6">
        {activeTab === 'matches' && (
          <div className="space-y-4">
            {results.similarity.matches.length === 0 ? (
              <div className="text-center py-8">
                <CheckCircle className="w-12 h-12 text-green-500 mx-auto mb-3" />
                <h3 className="text-lg font-medium text-gray-900 dark:text-gray-100 mb-2">No Similar Code Found</h3>
                <p className="text-gray-700 dark:text-gray-300">
                  Your code appears to be unique with no significant similarities found in our database.
                </p>
              </div>
            ) : (
              results.similarity.matches.map((match, index) => (
                <div key={match.id} className="border border-gray-200 rounded-lg overflow-hidden">
                  <div
                    className="p-4 bg-gray-50 cursor-pointer hover:bg-gray-100 transition-colors"
                    onClick={() => setExpandedMatch(expandedMatch === index ? null : index)}
                  >
                    <div className="flex items-center justify-between">
                      <div className="flex items-center gap-3">
                        {expandedMatch === index ? (
                          <ChevronDown className="w-4 h-4 text-gray-400 dark:text-gray-500" />
                        ) : (
                          <ChevronRight className="w-4 h-4 text-gray-400 dark:text-gray-500" />
                        )}
                        <div className={`flex items-center gap-2 px-2 py-1 rounded-full text-xs font-medium ${getSimilarityColor(match.similarity_score)}`}>
                          {getSimilarityIcon(match.similarity_score)}
                          {formatPercentage(match.similarity_score)} Similar
                        </div>
                        <span className="font-medium text-gray-900 dark:text-gray-100">{match.description}</span>
                      </div>
                      <div className="flex items-center gap-2 text-sm text-gray-600 dark:text-gray-400">
                        <span className="bg-gray-200 dark:bg-gray-700 px-2 py-1 rounded text-xs text-gray-800 dark:text-gray-200">
                          {match.source}
                        </span>
                      </div>
                    </div>
                  </div>
                  
                  {expandedMatch === index && (
                    <div className="p-4 border-t border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-800">
                      <h4 className="font-medium text-gray-900 dark:text-gray-100 mb-3">Code Snippet:</h4>
                      <div className="bg-gray-50 dark:bg-gray-900 rounded-lg p-4 overflow-x-auto">
                        <SyntaxHighlighter
                          language={results.language}
                          style={theme === 'dark' ? oneDark : oneLight}
                          customStyle={{
                            background: 'transparent',
                            padding: 0,
                            margin: 0,
                            fontSize: '13px',
                          }}
                        >
                          {match.code_snippet}
                        </SyntaxHighlighter>
                      </div>
                    </div>
                  )}
                </div>
              ))
            )}
          </div>
        )}

        {activeTab === 'details' && (
          <div className="space-y-6">
            <div>
              <h3 className="text-lg font-semibold text-gray-900 dark:text-gray-100 mb-4">Code Structure Analysis</h3>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
                <div className="bg-blue-50 dark:bg-blue-900/20 p-4 rounded-lg">
                  <h4 className="font-medium text-blue-900 dark:text-blue-200 mb-2">Lines of Code</h4>
                  <div className="space-y-1 text-sm">
                    <div className="flex justify-between">
                      <span className="text-blue-700 dark:text-blue-300">Total:</span>
                      <span className="font-medium text-gray-900 dark:text-gray-100">{results.analysis.lines_of_code.total}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-blue-700 dark:text-blue-300">Code:</span>
                      <span className="font-medium text-gray-900 dark:text-gray-100">{results.analysis.lines_of_code.code}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-blue-700 dark:text-blue-300">Comments:</span>
                      <span className="font-medium text-gray-900 dark:text-gray-100">{results.analysis.lines_of_code.comments}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-blue-700 dark:text-blue-300">Blank:</span>
                      <span className="font-medium text-gray-900 dark:text-gray-100">{results.analysis.lines_of_code.blank}</span>
                    </div>
                  </div>
                </div>
                
                <div className="bg-purple-50 dark:bg-purple-900/20 p-4 rounded-lg">
                  <h4 className="font-medium text-purple-900 dark:text-purple-200 mb-2">Complexity</h4>
                  <div className="space-y-1 text-sm">
                    <div className="flex justify-between">
                      <span className="text-purple-700 dark:text-purple-300">Cyclomatic:</span>
                      <span className="font-medium text-gray-900 dark:text-gray-100">{results.analysis.complexity_metrics.cyclomatic_complexity}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-purple-700 dark:text-purple-300">Functions:</span>
                      <span className="font-medium text-gray-900 dark:text-gray-100">{results.analysis.complexity_metrics.function_count}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-purple-700 dark:text-purple-300">Classes:</span>
                      <span className="font-medium text-gray-900 dark:text-gray-100">{results.analysis.complexity_metrics.class_count}</span>
                    </div>
                    {results.analysis.complexity_metrics.nesting_depth && (
                      <div className="flex justify-between">
                        <span className="text-purple-700 dark:text-purple-300">Nesting Depth:</span>
                        <span className="font-medium text-gray-900 dark:text-gray-100">{results.analysis.complexity_metrics.nesting_depth}</span>
                      </div>
                    )}
                  </div>
                </div>
              </div>

              {/* Control Flow Analysis */}
              {results.analysis.structure_analysis?.control_flow && (
                <div className="bg-green-50 dark:bg-green-900/20 p-4 rounded-lg mb-6">
                  <h4 className="font-medium text-green-900 dark:text-green-200 mb-2">Control Flow</h4>
                  <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm">
                    <div className="flex justify-between">
                      <span className="text-green-700 dark:text-green-300">If Statements:</span>
                      <span className="font-medium text-gray-900 dark:text-gray-100">{results.analysis.structure_analysis.control_flow.if_statements || 0}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-green-700 dark:text-green-300">Loops:</span>
                      <span className="font-medium text-gray-900 dark:text-gray-100">{results.analysis.structure_analysis.control_flow.loops || 0}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-green-700 dark:text-green-300">Switches:</span>
                      <span className="font-medium text-gray-900 dark:text-gray-100">{results.analysis.structure_analysis.control_flow.switches || 0}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-green-700 dark:text-green-300">Try/Catch:</span>
                      <span className="font-medium text-gray-900 dark:text-gray-100">{results.analysis.structure_analysis.control_flow.try_catch || 0}</span>
                    </div>
                  </div>
                </div>
              )}

              {/* Function Names */}
              {results.analysis.structure_analysis?.function_names && results.analysis.structure_analysis.function_names.length > 0 && (
                <div className="bg-yellow-50 dark:bg-yellow-900/20 p-4 rounded-lg mb-4">
                  <h4 className="font-medium text-yellow-900 dark:text-yellow-200 mb-2">Function Names</h4>
                  <div className="flex flex-wrap gap-2">
                    {results.analysis.structure_analysis.function_names.map((func, index) => (
                      <span key={index} className="bg-yellow-200 dark:bg-yellow-800 text-yellow-800 dark:text-yellow-200 px-2 py-1 rounded text-sm font-mono">
                        {func}()
                      </span>
                    ))}
                  </div>
                </div>
              )}

              {/* Data Structures */}
              {results.analysis.patterns?.data_structures && results.analysis.patterns.data_structures.length > 0 && (
                <div className="bg-orange-50 dark:bg-orange-900/20 p-4 rounded-lg mb-4">
                  <h4 className="font-medium text-orange-900 dark:text-orange-200 mb-2">Data Structures</h4>
                  <div className="flex flex-wrap gap-2">
                    {results.analysis.patterns.data_structures.map((ds, index) => (
                      <span key={index} className="bg-orange-200 dark:bg-orange-800 text-orange-800 dark:text-orange-200 px-2 py-1 rounded text-sm">
                        {ds}
                      </span>
                    ))}
                  </div>
                </div>
              )}

              {/* Algorithm Patterns */}
              {results.analysis.patterns?.algorithm_patterns && results.analysis.patterns.algorithm_patterns.length > 0 && (
                <div className="bg-indigo-50 dark:bg-indigo-900/20 p-4 rounded-lg mb-4">
                  <h4 className="font-medium text-indigo-900 dark:text-indigo-200 mb-2">Algorithm Patterns</h4>
                  <div className="flex flex-wrap gap-2">
                    {results.analysis.patterns.algorithm_patterns.map((pattern, index) => (
                      <span key={index} className="bg-indigo-200 dark:bg-indigo-800 text-indigo-800 dark:text-indigo-200 px-2 py-1 rounded text-sm">
                        {pattern}
                      </span>
                    ))}
                  </div>
                </div>
              )}

              {/* Code Quality Metrics */}
              {results.analysis.code_quality && (
                <div className="bg-gray-50 dark:bg-gray-700 p-4 rounded-lg">
                  <h4 className="font-medium text-gray-900 dark:text-gray-100 mb-3">Code Quality</h4>
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-3">
                    {results.analysis.code_quality.readability_score !== undefined && (
                      <div className="text-center">
                        <div className="text-lg font-bold text-blue-600 dark:text-blue-400">
                          {results.analysis.code_quality.readability_score.toFixed(1)}%
                        </div>
                        <div className="text-sm text-gray-700 dark:text-gray-300">Readability Score</div>
                      </div>
                    )}
                    {results.analysis.code_quality.maintainability_index !== undefined && (
                      <div className="text-center">
                        <div className="text-lg font-bold text-green-600 dark:text-green-400">
                          {results.analysis.code_quality.maintainability_index.toFixed(1)}
                        </div>
                        <div className="text-sm text-gray-700 dark:text-gray-300">Maintainability Index</div>
                      </div>
                    )}
                  </div>
                  
                  {/* Code Smells */}
                  {results.analysis.code_quality.code_smells && results.analysis.code_quality.code_smells.length > 0 && (
                    <div className="mb-3">
                      <h5 className="text-sm font-medium text-red-800 dark:text-red-300 mb-2">Code Smells</h5>
                      <div className="flex flex-wrap gap-1">
                        {results.analysis.code_quality.code_smells.map((smell, index) => (
                          <span key={index} className="bg-red-100 dark:bg-red-900/20 text-red-800 dark:text-red-300 px-2 py-1 rounded text-xs">
                            {smell}
                          </span>
                        ))}
                      </div>
                    </div>
                  )}
                  
                  {/* Best Practices */}
                  {results.analysis.code_quality.best_practices && (
                    <div>
                      <h5 className="text-sm font-medium text-gray-800 dark:text-gray-200 mb-2">Best Practices</h5>
                      <div className="space-y-1 text-sm">
                        {Object.entries(results.analysis.code_quality.best_practices).map(([practice, follows]) => (
                          <div key={practice} className="flex items-center gap-2">
                            <span className={`w-2 h-2 rounded-full ${follows ? 'bg-green-500' : 'bg-red-500'}`}></span>
                            <span className="text-gray-800 dark:text-gray-200">{practice.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase())}</span>
                          </div>
                        ))}
                      </div>
                    </div>
                  )}
                </div>
              )}
            </div>
          </div>
        )}

        {activeTab === 'metrics' && (
          <div className="space-y-6">
            <div>
              <h3 className="text-lg font-semibold text-gray-900 dark:text-gray-100 mb-4">Analysis Metrics</h3>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <div className="text-center p-4 bg-gray-50 dark:bg-gray-700 rounded-lg">
                  <div className="text-2xl font-bold text-gray-900 dark:text-gray-100">
                    {results.analysis.detected_language.toUpperCase()}
                  </div>
                  <div className="text-sm text-gray-700 dark:text-gray-300 mt-1">Detected Language</div>
                </div>
                <div className="text-center p-4 bg-gray-50 dark:bg-gray-700 rounded-lg">
                  <div className="text-2xl font-bold text-gray-900 dark:text-gray-100">
                    {formatPercentage(results.similarity.highest_similarity)}
                  </div>
                  <div className="text-sm text-gray-700 dark:text-gray-300 mt-1">Highest Similarity</div>
                </div>
                <div className="text-center p-4 bg-gray-50 dark:bg-gray-700 rounded-lg">
                  <div className="text-2xl font-bold text-gray-900 dark:text-gray-100">
                    {results.similarity.total_checked}
                  </div>
                  <div className="text-sm text-gray-700 dark:text-gray-300 mt-1">Database Size</div>
                </div>
              </div>
            </div>
            
            <div className="text-xs text-gray-700 dark:text-gray-300 pt-4 border-t border-gray-200 dark:border-gray-700">
              Analysis completed at: {new Date(results.timestamp).toLocaleString()}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
