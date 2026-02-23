import React, { useEffect } from 'react';
import { CheckCircle, XCircle, AlertTriangle, Info, X } from 'lucide-react';

export type ToastType = 'success' | 'error' | 'warning' | 'info';

interface ToastProps {
 type: ToastType;
 message: string;
 onClose: () => void;
 duration?: number;
}

const Toast: React.FC<ToastProps> = ({ type, message, onClose, duration = 000 }) => {
 useEffect(() => {
 if (duration > 0) {
 const timer = setTimeout(() => {
 onClose();
 }, duration);
 return () => clearTimeout(timer);
 }
 }, [duration, onClose]);

 const config = {
 success: {
 icon: CheckCircle,
 bgColor: 'bg-green-0',
 borderColor: 'border-green-00',
 textColor: 'text-green-00',
 iconColor: 'text-green-00'
 },
 error: {
 icon: XCircle,
 bgColor: 'bg-red-0',
 borderColor: 'border-red-00',
 textColor: 'text-red-00',
 iconColor: 'text-red-00'
 },
 warning: {
 icon: AlertTriangle,
 bgColor: 'bg-yellow-0',
 borderColor: 'border-yellow-00',
 textColor: 'text-yellow-00',
 iconColor: 'text-yellow-00'
 },
 info: {
 icon: Info,
 bgColor: 'bg-blue-0',
 borderColor: 'border-blue-00',
 textColor: 'text-blue-00',
 iconColor: 'text-blue-00'
 }
 };

 const { icon: Icon, bgColor, borderColor, textColor, iconColor } = config[type];

 return (
 <div className={`fixed top- right- z-0 max-w-md animate-slide-in-right`}>
 <div className={`${bgColor} ${borderColor} border rounded-lg shadow-lg p-`}>
 <div className="flex items-start space-x-">
 <Icon className={`h- w- ${iconColor} flex-shrink-0 mt-0.`} />
 <p className={`flex- text-sm font-medium ${textColor}`}>{message}</p>
 <button
 onClick={onClose}
 className={`${textColor} hover:opacity-0 transition-opacity`}
 >
 <X className="h- w-" />
 </button>
 </div>
 </div>
 </div>
 );
};

export default Toast;
