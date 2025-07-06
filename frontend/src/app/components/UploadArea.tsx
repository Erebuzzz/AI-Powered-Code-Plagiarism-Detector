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
        const content = e.target?.result as string;
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
      className={`border-2 border-dashed rounded-lg p-6 text-center cursor-pointer transition-colors duration-200 ${
        isDragActive
          ? 'border-blue-400 bg-blue-50 dark:bg-blue-900/20 dark:border-blue-500'
          : 'border-gray-300 dark:border-gray-600 hover:border-gray-400 dark:hover:border-gray-500 hover:bg-gray-50 dark:hover:bg-gray-800'
      }`}
    >
      <input {...getInputProps()} />
      <div className="flex flex-col items-center gap-2">
        {isDragActive ? (
          <>
            <Upload className="w-8 h-8 text-blue-500 dark:text-blue-400" />
            <p className="text-blue-600 dark:text-blue-400 font-medium">Drop your code file here</p>
          </>
        ) : (
          <>
            <File className="w-8 h-8 text-gray-400 dark:text-gray-500" />
            <p className="text-gray-700 dark:text-gray-300">
              Drag &amp; drop a code file here, or{' '}
              <span className="text-blue-600 dark:text-blue-400 font-medium">click to browse</span>
            </p>
            <p className="text-xs text-gray-600 dark:text-gray-400">
              Supports: .py, .js, .ts, .java, .cpp, .c, .cs, .php, .rb, .go, .rs, .swift, .kt
            </p>
          </>
        )}
      </div>
    </div>
  );
}
