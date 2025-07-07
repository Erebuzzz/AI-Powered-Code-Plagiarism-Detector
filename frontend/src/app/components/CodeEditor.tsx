"use client";

import { Editor } from "@monaco-editor/react";
import { useTheme } from "../contexts/ThemeContext";

export interface CodeEditorProps {
  value: string;
  onChangeAction: (value: string) => void;
  language: string;
  placeholder?: string;
}

export default function CodeEditor({ value, onChangeAction, language, placeholder }: CodeEditorProps) {
  const { theme } = useTheme();

  const handleEditorChange = (value: string | undefined) => {
    onChangeAction(value || "");
  };

  const getMonacoLanguage = (lang: string) => {
    const langMap: Record<string, string> = {
      python: "python",
      javascript: "javascript",
      typescript: "typescript",
      java: "java",
      cpp: "cpp",
      c: "c",
      csharp: "csharp",
      php: "php",
      ruby: "ruby",
      go: "go",
      rust: "rust",
      swift: "swift",
      kotlin: "kotlin",
    };
    return langMap[lang] || "plaintext";
  };

  return (
    <div className="border border-gray-300 dark:border-gray-600 rounded-lg overflow-hidden">
      <Editor
        height="400px"
        language={getMonacoLanguage(language)}
        value={value}
        onChange={handleEditorChange}
        theme={theme === "dark" ? "vs-dark" : "vs-light"}
        options={{
          minimap: { enabled: false },
          lineNumbers: "on",
          roundedSelection: false,
          scrollBeyondLastLine: false,
          automaticLayout: true,
          tabSize: 2,
          insertSpaces: true,
          wordWrap: "on",
          fontSize: 14,
          fontFamily: 'Monaco, "Cascadia Code", "Roboto Mono", Consolas, "Courier New", monospace',
          suggest: {
            showKeywords: true,
            showSnippets: true,
          },
          bracketPairColorization: {
            enabled: true,
          },
          hover: {
            enabled: true,
          },
          contextmenu: true,
          selectOnLineNumbers: true,
          quickSuggestions: {
            other: true,
            comments: true,
            strings: true,
          },
          folding: true,
          foldingStrategy: "indentation",
          showFoldingControls: "always",
          unfoldOnClickAfterEndOfLine: false,
          renderLineHighlight: "line",
          smoothScrolling: true,
          cursorBlinking: "blink",
          renderWhitespace: "selection",
        }}
        loading={
          <div className="flex items-center justify-center h-[400px] text-gray-500">
            <div className="flex items-center gap-2">
              <div className="w-4 h-4 border-2 border-gray-300 border-t-blue-600 rounded-full animate-spin"></div>
              Loading editor...
            </div>
          </div>
        }
      />
      {!value && placeholder && (
        <div className="absolute inset-0 flex items-start justify-start p-4 pointer-events-none">
          <span className="text-gray-400 text-sm">{placeholder}</span>
        </div>
      )}
    </div>
  );
}
