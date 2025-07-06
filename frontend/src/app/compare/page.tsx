'use client';

import { useState } from 'react';
import Link from 'next/link';
import { GitCompare, ArrowLeftRight, Code } from 'lucide-react';

export default function ComparisonTool() {
  const [code1, setCode1] = useState('');
  const [code2, setCode2] = useState('');
  const [language, setLanguage] = useState('python');

  return (
    <div className="min-h-screen bg-gradient-to-br from-green-50 via-white to-blue-50">
      <header className="bg-white/80 backdrop-blur-sm border-b border-gray-200 sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="bg-gradient-to-r from-green-600 to-blue-600 p-2 rounded-lg">
                <GitCompare className="w-6 h-6 text-white" />
              </div>
              <div>
                <h1 className="text-xl font-bold text-gray-900">Code Comparison Tool</h1>
                <p className="text-sm text-gray-600">Compare two code snippets side by side</p>
              </div>
            </div>
            <nav className="hidden md:flex items-center gap-4">
              <Link href="/" className="text-gray-600 hover:text-gray-900 px-3 py-2 rounded-md text-sm font-medium transition-colors">
                Analyzer
              </Link>
              <Link href="/demo" className="text-gray-600 hover:text-gray-900 px-3 py-2 rounded-md text-sm font-medium transition-colors">
                Demo
              </Link>
              <Link href="/compare" className="text-blue-600 bg-blue-50 px-3 py-2 rounded-md text-sm font-medium">
                Compare
              </Link>
            </nav>
          </div>
        </div>
      </header>
      
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8">
          {/* Code Input 1 */}
          <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-lg font-semibold text-gray-900">Code Sample 1</h3>
              <select
                value={language}
                onChange={(e) => setLanguage(e.target.value)}
                className="px-3 py-1 border border-gray-300 rounded-md text-sm focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              >
                <option value="python">Python</option>
                <option value="javascript">JavaScript</option>
                <option value="java">Java</option>
                <option value="cpp">C++</option>
              </select>
            </div>
            <textarea
              value={code1}
              onChange={(e) => setCode1(e.target.value)}
              placeholder="Paste your first code snippet here..."
              className="w-full h-64 p-4 border border-gray-300 rounded-lg font-mono text-sm focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-none"
            />
          </div>

          {/* Code Input 2 */}
          <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-lg font-semibold text-gray-900">Code Sample 2</h3>
              <div className="text-sm text-gray-500">Same language: {language}</div>
            </div>
            <textarea
              value={code2}
              onChange={(e) => setCode2(e.target.value)}
              placeholder="Paste your second code snippet here..."
              className="w-full h-64 p-4 border border-gray-300 rounded-lg font-mono text-sm focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-none"
            />
          </div>
        </div>

        {/* Compare Button */}
        <div className="text-center mb-8">
          <button
            disabled={!code1.trim() || !code2.trim()}
            className="bg-gradient-to-r from-green-600 to-blue-600 text-white px-8 py-3 rounded-lg font-medium hover:from-green-700 hover:to-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-200 flex items-center justify-center gap-2 mx-auto"
          >
            <ArrowLeftRight className="w-4 h-4" />
            Compare Code Snippets
          </button>
        </div>

        {/* Coming Soon Notice */}
        <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-8 text-center">
          <div className="w-16 h-16 bg-blue-100 rounded-full flex items-center justify-center mx-auto mb-4">
            <Code className="w-8 h-8 text-blue-600" />
          </div>
          <h2 className="text-xl font-semibold text-gray-900 mb-2">Advanced Comparison Coming Soon</h2>
          <p className="text-gray-600 mb-4">
            Side-by-side code comparison with detailed similarity analysis, highlighting, and diff visualization will be available here.
          </p>
          <p className="text-sm text-gray-500">
            For now, you can use the main analyzer to check individual code snippets for similarity.
          </p>
        </div>
      </main>
    </div>
  );
}
