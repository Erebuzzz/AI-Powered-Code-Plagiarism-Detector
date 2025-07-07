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
        {/* ...existing code for tabs and rendering... */}
      </div>
    </div>
  );
}
