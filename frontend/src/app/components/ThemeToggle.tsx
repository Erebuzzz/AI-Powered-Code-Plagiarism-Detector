'use client';

import { Moon, Sun } from 'lucide-react';
import { useTheme } from '../contexts/ThemeContext';

export default function ThemeToggle() {
  const { theme, toggleTheme } = useTheme();

  return (
    <button
      onClick={toggleTheme}
      className="relative p-3 rounded-2xl bg-white/80 hover:bg-white dark:bg-gray-800/80 dark:hover:bg-gray-800 transition-all duration-300 border border-gray-200/50 dark:border-gray-700/50 shadow-lg hover:shadow-xl backdrop-blur-sm group"
      aria-label={`Switch to ${theme === 'light' ? 'dark' : 'light'} mode`}
    >
      <div className="relative">
        {theme === 'light' ? (
          <Moon className="w-5 h-5 text-gray-700 dark:text-gray-300 group-hover:scale-110 transition-transform duration-300" />
        ) : (
          <Sun className="w-5 h-5 text-amber-500 group-hover:scale-110 transition-transform duration-300" />
        )}
        
        {/* Animated background glow */}
        <div className="absolute inset-0 rounded-2xl bg-gradient-to-r from-blue-400 to-purple-400 opacity-0 group-hover:opacity-20 transition-opacity duration-300 blur-sm"></div>
      </div>
      
      {/* Tooltip */}
      <div className="absolute -bottom-12 left-1/2 transform -translate-x-1/2 px-3 py-1.5 bg-gray-900 dark:bg-white text-white dark:text-gray-900 text-xs font-medium rounded-lg opacity-0 group-hover:opacity-100 transition-opacity duration-300 pointer-events-none whitespace-nowrap">
        {theme === 'light' ? 'Dark mode' : 'Light mode'}
        <div className="absolute -top-1 left-1/2 transform -translate-x-1/2 w-2 h-2 bg-gray-900 dark:bg-white rotate-45"></div>
      </div>
    </button>
  );
}
