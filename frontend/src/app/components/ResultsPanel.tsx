"use client";

import { useState } from "react";
import { Eye, Code, BarChart3 } from "lucide-react";

export interface AnalysisResult {
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

export interface ResultsPanelProps {
  results: AnalysisResult;
}

export default function ResultsPanel({ results }: ResultsPanelProps) {
  const [activeTab, setActiveTab] = useState<'matches' | 'details' | 'metrics'>('matches');

  return (
    <div className="bg-white/80 dark:bg-gray-900/80 backdrop-blur-sm rounded-3xl border border-white/60 dark:border-gray-800/60 shadow-xl">
      {/* Tab Navigation */}
      <div className="border-b border-gray-200/50 dark:border-gray-700/50">
        <nav className="flex p-2">
          <button
            onClick={() => setActiveTab('matches')}
            className={`flex-1 px-4 py-3 text-sm font-semibold rounded-2xl transition-all duration-200 ${
              activeTab === 'matches'
                ? 'bg-gradient-to-r from-blue-500 to-purple-500 text-white shadow-lg'
                : 'text-gray-600 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-800'
            }`}
          >
            <div className="flex items-center justify-center gap-2">
              <Eye className="w-4 h-4" />
              Matches ({results.similarity.matches.length})
            </div>
          </button>
          <button
            onClick={() => setActiveTab('details')}
            className={`flex-1 px-4 py-3 text-sm font-semibold rounded-2xl transition-all duration-200 ${
              activeTab === 'details'
                ? 'bg-gradient-to-r from-blue-500 to-purple-500 text-white shadow-lg'
                : 'text-gray-600 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-800'
            }`}
          >
            <div className="flex items-center justify-center gap-2">
              <Code className="w-4 h-4" />
              Details
            </div>
          </button>
          <button
            onClick={() => setActiveTab('metrics')}
            className={`flex-1 px-4 py-3 text-sm font-semibold rounded-2xl transition-all duration-200 ${
              activeTab === 'metrics'
                ? 'bg-gradient-to-r from-blue-500 to-purple-500 text-white shadow-lg'
                : 'text-gray-600 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-800'
            }`}
          >
            <div className="flex items-center justify-center gap-2">
              <BarChart3 className="w-4 h-4" />
              Metrics
            </div>
          </button>
        </nav>
      </div>

      <div className="p-8">
        {activeTab === 'matches' && (
          <div className="space-y-4">
            <h4 className="text-lg font-semibold text-gray-900 dark:text-gray-100 mb-4">
              Similarity Matches
            </h4>
            {results.similarity.matches.length > 0 ? (
              <div className="space-y-3">
                {results.similarity.matches.map((match) => (
                  <div
                    key={match.id}
                    className="bg-gray-50 dark:bg-gray-800/50 rounded-2xl p-4 border border-gray-200 dark:border-gray-700"
                  >
                    <div className="flex items-center justify-between mb-2">
                      <span className="text-sm font-medium text-gray-900 dark:text-gray-100">
                        Match #{match.id}
                      </span>
                      <span className={`px-3 py-1 rounded-full text-xs font-medium ${
                        match.similarity_score > 0.8
                          ? 'bg-red-100 text-red-800 dark:bg-red-900/30 dark:text-red-300'
                          : match.similarity_score > 0.6
                          ? 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900/30 dark:text-yellow-300'
                          : 'bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-300'
                      }`}>
                        {(match.similarity_score * 100).toFixed(1)}% similar
                      </span>
                    </div>
                    <p className="text-sm text-gray-700 dark:text-gray-300 mb-2">
                      {match.description}
                    </p>
                    <p className="text-xs text-gray-500 dark:text-gray-400">
                      Source: {match.source}
                    </p>
                  </div>
                ))}
              </div>
            ) : (
              <div className="text-center py-8">
                <div className="w-16 h-16 bg-gray-100 dark:bg-gray-700 rounded-full flex items-center justify-center mx-auto mb-4">
                  <Eye className="w-8 h-8 text-gray-400" />
                </div>
                <p className="text-gray-500 dark:text-gray-400">No similarity matches found</p>
              </div>
            )}
          </div>
        )}

        {activeTab === 'details' && (
          <div className="space-y-6">
            <h4 className="text-lg font-semibold text-gray-900 dark:text-gray-100">
              Code Analysis Details
            </h4>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="bg-blue-50 dark:bg-blue-900/20 p-4 rounded-2xl">
                <h5 className="font-medium text-blue-900 dark:text-blue-100 mb-2">Language Detection</h5>
                <p className="text-2xl font-bold text-blue-600 dark:text-blue-400">
                  {results.analysis.detected_language.toUpperCase()}
                </p>
              </div>
              <div className="bg-purple-50 dark:bg-purple-900/20 p-4 rounded-2xl">
                <h5 className="font-medium text-purple-900 dark:text-purple-100 mb-2">Code Quality</h5>
                <p className="text-sm text-purple-700 dark:text-purple-300">
                  {results.analysis.lines_of_code.code} lines of code, {results.analysis.lines_of_code.comments} comments
                </p>
              </div>
            </div>
          </div>
        )}

        {activeTab === 'metrics' && (
          <div className="space-y-6">
            <h4 className="text-lg font-semibold text-gray-900 dark:text-gray-100">
              Complexity Metrics
            </h4>
            <div className="grid grid-cols-2 gap-4">
              <div className="bg-emerald-50 dark:bg-emerald-900/20 p-4 rounded-2xl text-center">
                <div className="text-2xl font-bold text-emerald-600 dark:text-emerald-400">
                  {results.analysis.complexity_metrics.cyclomatic_complexity}
                </div>
                <div className="text-sm text-emerald-700 dark:text-emerald-300">Complexity</div>
              </div>
              <div className="bg-amber-50 dark:bg-amber-900/20 p-4 rounded-2xl text-center">
                <div className="text-2xl font-bold text-amber-600 dark:text-amber-400">
                  {results.analysis.complexity_metrics.function_count}
                </div>
                <div className="text-sm text-amber-700 dark:text-amber-300">Functions</div>
              </div>
              <div className="bg-rose-50 dark:bg-rose-900/20 p-4 rounded-2xl text-center">
                <div className="text-2xl font-bold text-rose-600 dark:text-rose-400">
                  {results.analysis.complexity_metrics.class_count}
                </div>
                <div className="text-sm text-rose-700 dark:text-rose-300">Classes</div>
              </div>
              <div className="bg-indigo-50 dark:bg-indigo-900/20 p-4 rounded-2xl text-center">
                <div className="text-2xl font-bold text-indigo-600 dark:text-indigo-400">
                  {results.analysis.complexity_metrics.nesting_depth || 0}
                </div>
                <div className="text-sm text-indigo-700 dark:text-indigo-300">Nesting</div>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
