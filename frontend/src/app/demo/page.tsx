'use client';

import { useState } from 'react';
import Link from 'next/link';
import { PlayCircle, Code, BarChart3, Shield } from 'lucide-react';

export default function DemoPage() {
  const [selectedDemo, setSelectedDemo] = useState<'fibonacci' | 'sort' | 'search'>('fibonacci');

  const demoResults = {
    fibonacci: {
      code: `def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

# Calculate first 10 fibonacci numbers
for i in range(10):
    print(f"F({i}) = {fibonacci(i)}")`,
      analysis: {
        similarity_score: 0.87,
        risk_level: 'high',
        matches: 3,
        language: 'Python',
        complexity: 'Medium',
      }
    },
    sort: {
      code: `def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(0, n-i-1):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
    return arr

# Example usage
numbers = [64, 34, 25, 12, 22, 11, 90]
sorted_numbers = bubble_sort(numbers)
print(sorted_numbers)`,
      analysis: {
        similarity_score: 0.92,
        risk_level: 'very_high',
        matches: 5,
        language: 'Python',
        complexity: 'Medium',
      }
    },
    search: {
      code: `def binary_search(arr, target):
    left, right = 0, len(arr) - 1
    
    while left <= right:
        mid = (left + right) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    
    return -1

# Example usage
sorted_array = [1, 3, 5, 7, 9, 11, 13, 15]
result = binary_search(sorted_array, 7)
print(f"Element found at index: {result}")`,
      analysis: {
        similarity_score: 0.73,
        risk_level: 'high',
        matches: 2,
        language: 'Python',
        complexity: 'Low',
      }
    }
  };

  const currentDemo = demoResults[selectedDemo];

  const getRiskColor = (risk: string) => {
    switch (risk) {
      case 'very_high': return 'text-red-600 bg-red-100';
      case 'high': return 'text-orange-600 bg-orange-100';
      case 'medium': return 'text-yellow-600 bg-yellow-100';
      default: return 'text-green-600 bg-green-100';
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-indigo-50 via-white to-cyan-50">
      <header className="bg-white/80 backdrop-blur-sm border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="bg-gradient-to-r from-indigo-600 to-purple-600 p-2 rounded-lg">
                <PlayCircle className="w-6 h-6 text-white" />
              </div>
              <div>
                <h1 className="text-2xl font-bold text-gray-900">Live Demo</h1>
                <p className="text-gray-600">See the AI plagiarism detector in action</p>
              </div>
            </div>
            <nav className="hidden md:flex items-center gap-4">
              <Link href="/" className="text-gray-600 hover:text-gray-900 px-3 py-2 rounded-md text-sm font-medium transition-colors">
                Analyzer
              </Link>
              <Link href="/demo" className="text-indigo-600 bg-indigo-50 px-3 py-2 rounded-md text-sm font-medium">
                Demo
              </Link>
              <Link href="/compare" className="text-gray-600 hover:text-gray-900 px-3 py-2 rounded-md text-sm font-medium transition-colors">
                Compare
              </Link>
            </nav>
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Demo Selection */}
          <div className="lg:col-span-1">
            <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
              <h2 className="text-lg font-semibold text-gray-900 mb-4">Choose Demo</h2>
              
              <div className="space-y-3">
                <button
                  onClick={() => setSelectedDemo('fibonacci')}
                  className={`w-full text-left p-4 rounded-lg border transition-all ${
                    selectedDemo === 'fibonacci' 
                      ? 'border-indigo-500 bg-indigo-50' 
                      : 'border-gray-200 hover:border-gray-300'
                  }`}
                >
                  <h3 className="font-medium text-gray-900">Fibonacci Sequence</h3>
                  <p className="text-sm text-gray-600 mt-1">Classic recursive implementation</p>
                  <div className="mt-2 flex items-center gap-2">
                    <span className="text-xs bg-orange-100 text-orange-800 px-2 py-1 rounded">87% Match</span>
                    <span className="text-xs bg-gray-100 text-gray-800 px-2 py-1 rounded">3 Similar</span>
                  </div>
                </button>

                <button
                  onClick={() => setSelectedDemo('sort')}
                  className={`w-full text-left p-4 rounded-lg border transition-all ${
                    selectedDemo === 'sort' 
                      ? 'border-indigo-500 bg-indigo-50' 
                      : 'border-gray-200 hover:border-gray-300'
                  }`}
                >
                  <h3 className="font-medium text-gray-900">Bubble Sort</h3>
                  <p className="text-sm text-gray-600 mt-1">Simple sorting algorithm</p>
                  <div className="mt-2 flex items-center gap-2">
                    <span className="text-xs bg-red-100 text-red-800 px-2 py-1 rounded">92% Match</span>
                    <span className="text-xs bg-gray-100 text-gray-800 px-2 py-1 rounded">5 Similar</span>
                  </div>
                </button>

                <button
                  onClick={() => setSelectedDemo('search')}
                  className={`w-full text-left p-4 rounded-lg border transition-all ${
                    selectedDemo === 'search' 
                      ? 'border-indigo-500 bg-indigo-50' 
                      : 'border-gray-200 hover:border-gray-300'
                  }`}
                >
                  <h3 className="font-medium text-gray-900">Binary Search</h3>
                  <p className="text-sm text-gray-600 mt-1">Efficient search algorithm</p>
                  <div className="mt-2 flex items-center gap-2">
                    <span className="text-xs bg-yellow-100 text-yellow-800 px-2 py-1 rounded">73% Match</span>
                    <span className="text-xs bg-gray-100 text-gray-800 px-2 py-1 rounded">2 Similar</span>
                  </div>
                </button>
              </div>

              <div className="mt-6 p-4 bg-gray-50 rounded-lg">
                <h3 className="font-medium text-gray-900 mb-2">About This Demo</h3>
                <p className="text-sm text-gray-600">
                  These are real results from our AI-powered plagiarism detection system. 
                  The algorithms shown are commonly implemented and thus have high similarity scores.
                </p>
              </div>
            </div>
          </div>

          {/* Code Display and Results */}
          <div className="lg:col-span-2">
            <div className="space-y-6">
              {/* Code Display */}
              <div className="bg-white rounded-xl shadow-sm border border-gray-200">
                <div className="p-4 border-b border-gray-200">
                  <div className="flex items-center gap-2">
                    <Code className="w-5 h-5 text-gray-600" />
                    <h3 className="font-semibold text-gray-900">Sample Code</h3>
                    <span className="text-sm bg-blue-100 text-blue-800 px-2 py-1 rounded">
                      {currentDemo.analysis.language}
                    </span>
                  </div>
                </div>
                <div className="p-4">
                  <pre className="bg-gray-50 p-4 rounded-lg overflow-x-auto text-sm">
                    <code>{currentDemo.code}</code>
                  </pre>
                </div>
              </div>

              {/* Analysis Results */}
              <div className="bg-white rounded-xl shadow-sm border border-gray-200">
                <div className="p-4 border-b border-gray-200">
                  <div className="flex items-center justify-between">
                    <div className="flex items-center gap-2">
                      <BarChart3 className="w-5 h-5 text-gray-600" />
                      <h3 className="font-semibold text-gray-900">Analysis Results</h3>
                    </div>
                    <span className={`px-3 py-1 rounded-full text-sm font-medium ${getRiskColor(currentDemo.analysis.risk_level)}`}>
                      {currentDemo.analysis.risk_level.replace('_', ' ').toUpperCase()} RISK
                    </span>
                  </div>
                </div>
                <div className="p-6">
                  <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
                    <div className="text-center p-4 bg-gray-50 rounded-lg">
                      <div className="text-2xl font-bold text-gray-900">
                        {(currentDemo.analysis.similarity_score * 100).toFixed(0)}%
                      </div>
                      <div className="text-sm text-gray-600">Similarity</div>
                    </div>
                    <div className="text-center p-4 bg-gray-50 rounded-lg">
                      <div className="text-2xl font-bold text-gray-900">
                        {currentDemo.analysis.matches}
                      </div>
                      <div className="text-sm text-gray-600">Matches</div>
                    </div>
                    <div className="text-center p-4 bg-gray-50 rounded-lg">
                      <div className="text-2xl font-bold text-gray-900">
                        {currentDemo.analysis.language}
                      </div>
                      <div className="text-sm text-gray-600">Language</div>
                    </div>
                    <div className="text-center p-4 bg-gray-50 rounded-lg">
                      <div className="text-2xl font-bold text-gray-900">
                        {currentDemo.analysis.complexity}
                      </div>
                      <div className="text-sm text-gray-600">Complexity</div>
                    </div>
                  </div>

                  <div className="bg-blue-50 p-4 rounded-lg">
                    <div className="flex items-start gap-3">
                      <Shield className="w-5 h-5 text-blue-600 mt-0.5" />
                      <div>
                        <h4 className="font-medium text-blue-900">AI Analysis Insight</h4>
                        <p className="text-blue-800 text-sm mt-1">
                          {selectedDemo === 'fibonacci' && "This recursive Fibonacci implementation matches classic textbook examples. High similarity is expected for this common algorithm pattern."}
                          {selectedDemo === 'sort' && "Bubble sort is one of the most basic sorting algorithms. The extremely high similarity indicates this exact implementation appears frequently in educational materials."}
                          {selectedDemo === 'search' && "Binary search implementation follows standard patterns. Moderate similarity suggests this is a common but not overly duplicated implementation."}
                        </p>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Call to Action */}
        <div className="mt-12 text-center">
          <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-8">
            <h2 className="text-2xl font-bold text-gray-900 mb-4">Ready to Analyze Your Code?</h2>
            <p className="text-gray-600 mb-6">
              Try our AI-powered plagiarism detector with your own code samples.
            </p>
            <Link
              href="/"
              className="inline-flex items-center gap-2 bg-gradient-to-r from-indigo-600 to-purple-600 text-white px-6 py-3 rounded-lg font-medium hover:from-indigo-700 hover:to-purple-700 transition-all duration-200"
            >
              <Code className="w-4 h-4" />
              Start Analyzing
            </Link>
          </div>
        </div>
      </main>
    </div>
  );
}
