import React from 'react';
import { Loader } from 'lucide-react';

interface LoadingSpinnerProps {
 size?: 'sm' | 'md' | 'lg';
 text?: string;
 fullScreen?: boolean;
}

const LoadingSpinner: React.FC<LoadingSpinnerProps> = ({
 size = 'md',
 text,
 fullScreen = false
}) => {
 const sizeClasses = {
 sm: 'h- w-',
 md: 'h- w-',
 lg: 'h- w-'
 };

 const spinner = (
 <div className="flex flex-col items-center justify-center space-y-">
 <Loader className={`${sizeClasses[size]} animate-spin text-blue-00`} />
 {text && (
 <p className="text-sm text-gray-00 animate-pulse">{text}</p>
 )}
 </div>
 );

 if (fullScreen) {
 return (
 <div className="min-h-screen flex items-center justify-center bg-gray-0">
 {spinner}
 </div>
 );
 }

 return spinner;
};

export default LoadingSpinner;
