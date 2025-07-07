'use client';

import { useCallback } from 'react';
import { useDropzone } from 'react-dropzone';
import { Upload, File } from 'lucide-react';

interface UploadAreaProps {
  onFileUploadAction: (content: string, filename: string) => void;
}

export default function UploadArea({ onFileUploadAction }: UploadAreaProps) {
  const onDrop = useCallback((acceptedFiles: File[]) => {
    const file = acceptedFiles[0];
    if (file) {
      const reader = new FileReader();
      reader.onload = (e) => {
        const content = (e.target?.result as string) || '';
        onFileUploadAction(content, file.name);
      };
      reader.readAsText(file);
    }
  }, [onFileUploadAction]);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'text/plain': ['.py', '.js', '.ts', '.tsx', '.jsx', '.java', '.cpp', '.c', '.cs', '.php', '.rb', '.go', '.rs', '.swift', '.kt'],
      'application/javascript': ['.js'],
      'text/javascript': ['.js'],
      'text/typescript': ['.ts', '.tsx'],
      'text/x-python': ['.py'],
      'text/x-java-source': ['.java'],
      'text/x-c': ['.c'],
      'text/x-c++src': ['.cpp'],
      'text/x-csharp': ['.cs'],
      'text/x-php': ['.php'],
      'text/x-ruby': ['.rb'],
      'text/x-go': ['.go'],
      'text/x-rust': ['.rs'],
      'text/x-swift': ['.swift'],
      'text/x-kotlin': ['.kt'],
    },
    multiple: false,
    maxSize: 1024 * 1024, // 1MB
  });

  return (
    <div
      {...getRootProps()}
      className={`relative border-2 border-dashed rounded-2xl p-8 text-center cursor-pointer transition-all duration-300 ${
        isDragActive
          ? 'border-blue-400 bg-gradient-to-br from-blue-50 to-purple-50 dark:from-blue-900/20 dark:to-purple-900/20 dark:border-blue-500 scale-[1.02]'
          : 'border-gray-300 dark:border-gray-600 hover:border-blue-300 dark:hover:border-blue-400 hover:bg-gray-50/50 dark:hover:bg-gray-800/50'
      }`}
    >
      <input {...getInputProps()} />
      <div className="flex flex-col items-center gap-4">
        {isDragActive ? (
          <>
            <div className="relative">
              <div className="absolute inset-0 bg-gradient-to-r from-blue-500 to-purple-500 rounded-2xl blur-sm opacity-75 animate-pulse"></div>
              <div className="relative bg-gradient-to-r from-blue-500 to-purple-500 p-4 rounded-2xl">
                <Upload className="w-8 h-8 text-white" />
              </div>
            </div>
            <div>
              <p className="text-lg font-semibold text-blue-600 dark:text-blue-400 mb-1">Drop your file here</p>
              <p className="text-sm text-blue-500 dark:text-blue-300">Release to upload</p>
            </div>
          </>
        ) : (
          <>
            <div className="p-4 bg-gray-100 dark:bg-gray-800 rounded-2xl">
              <File className="w-8 h-8 text-gray-600 dark:text-gray-400" />
            </div>
            <div>
              <p className="text-lg font-semibold text-gray-700 dark:text-gray-300 mb-1">
                Upload Code File
              </p>
              <p className="text-sm text-gray-600 dark:text-gray-400 mb-2">
                Drag &amp; drop your file here, or{' '}
                <span className="text-blue-600 dark:text-blue-400 font-medium hover:underline">click to browse</span>
              </p>
              <div className="flex flex-wrap justify-center gap-1 text-xs text-gray-500 dark:text-gray-500">
                <span className="px-2 py-1 bg-gray-100 dark:bg-gray-700 rounded-md">.py</span>
                <span className="px-2 py-1 bg-gray-100 dark:bg-gray-700 rounded-md">.js</span>
                <span className="px-2 py-1 bg-gray-100 dark:bg-gray-700 rounded-md">.ts</span>
                <span className="px-2 py-1 bg-gray-100 dark:bg-gray-700 rounded-md">.java</span>
                <span className="px-2 py-1 bg-gray-100 dark:bg-gray-700 rounded-md">.cpp</span>
                <span className="px-2 py-1 bg-gray-100 dark:bg-gray-700 rounded-md">+more</span>
              </div>
            </div>
          </>
        )}
      </div>
    </div>
  );
}
