import React from 'react';
import { X, Activity, TrendingUp, AlertCircle, CheckCircle } from 'lucide-react';
import ProbabilityChart from './ProbabilityChart';

interface DiseaseProbability {
 disease: string;
 probability: number;
}

interface PredictionResult {
 predicted_disease: string;
 confidence: number;
 risk_score: number;
 risk_level: string;
 all_class_probabilities?: DiseaseProbability[];
}

interface PredictionResultModalProps {
 isOpen: boolean;
 onClose: () => void;
 prediction: PredictionResult;
}

const PredictionResultModal: React.FC<PredictionResultModalProps> = ({
 isOpen,
 onClose,
 prediction
}) => {
 if (!isOpen) return null;

 const getRiskColor = (riskLevel: string) => {
 switch (riskLevel.toLowerCase()) {
 case 'high':
 return 'text-red-00 bg-red-0 border-red-00';
 case 'medium':
 return 'text-yellow-00 bg-yellow-0 border-yellow-00';
 case 'low':
 return 'text-green-00 bg-green-0 border-green-00';
 default:
 return 'text-gray-00 bg-gray-0 border-gray-00';
 }
 };

 const getRiskIcon = (riskLevel: string) => {
 switch (riskLevel.toLowerCase()) {
 case 'high':
 return <AlertCircle className="h- w-" />;
 case 'medium':
 return <Activity className="h- w-" />;
 case 'low':
 return <CheckCircle className="h- w-" />;
 default:
 return <Activity className="h- w-" />;
 }
 };

 const formatDiseaseName = (disease: string) => {
 return disease.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase());
 };

 return (
 <div className="fixed inset-0 bg-black bg-opacity-0 flex items-center justify-center z-0 p-">
 <div className="bg-white rounded-lg shadow-xl max-w-xl w-full max-h-[0vh] overflow-y-auto">
 {/* Header */}
 <div className="flex items-center justify-between p- border-b">
 <div className="flex items-center space-x-">
 <div className="p- bg-blue-00 rounded-lg">
 <Activity className="h- w- text-blue-00" />
 </div>
 <div>
 <h className="text-xl font-semibold text-gray-00">Prediction Results</h>
 <p className="text-sm text-gray-00">AI-powered health risk assessment</p>
 </div>
 </div>
 <button
 onClick={onClose}
 className="p- hover:bg-gray-00 rounded-lg transition-colors"
 >
 <X className="h- w- text-gray-00" />
 </button>
 </div>

 {/* Main Content */}
 <div className="p- space-y-">
 {/* Primary Prediction */}
 <div className="text-center space-y-">
 <div>
 <h className="text-xl font-bold text-gray-00 mb-">
 {formatDiseaseName(prediction.predicted_disease)}
 </h>
 <div className={`inline-flex items-center space-x- px- py- rounded-full border ${getRiskColor(prediction.risk_level)}`}>
 {getRiskIcon(prediction.risk_level)}
 <span className="font-medium">
 {prediction.risk_level} Risk ({(prediction.confidence * 00).toFixed()}% confidence)
 </span>
 </div>
 </div>

 {/* Risk Score */}
 <div className="bg-gray-0 rounded-lg p-">
 <div className="flex items-center justify-center space-x- mb-">
 <TrendingUp className="h- w- text-gray-00" />
 <span className="text-sm font-medium text-gray-00">Risk Score</span>
 </div>
 <div className="text-xl font-bold text-gray-00">
 {(prediction.risk_score * 00).toFixed()}%
 </div>
 </div>
 </div>

 {/* Probability Chart */}
 {prediction.all_class_probabilities && prediction.all_class_probabilities.length > 0 && (
 <div className="space-y-">
 <div className="border-t pt-">
 <h className="text-lg font-semibold text-gray-00 mb-">
 All Disease Probabilities
 </h>
 <p className="text-sm text-gray-00 mb-">
 Likelihood of each possible condition based on your symptoms and water quality data
 </p>

 <div className="bg-gray-0 rounded-lg p-">
 <ProbabilityChart probabilities={prediction.all_class_probabilities} />
 </div>
 </div>

 {/* Top Predictions */}
 <div className="space-y-">
 <h className="font-medium text-gray-00">Top Most Likely Conditions:</h>
 <div className="space-y-">
 {prediction.all_class_probabilities.slice(0, ).map((prob, index) => (
 <div key={prob.disease} className="flex items-center justify-between p- bg-white border rounded-lg">
 <div className="flex items-center space-x-">
 <div className={`w- h- rounded-full flex items-center justify-center text-xs font-bold text-white ${
 index === 0 ? 'bg-yellow-00' : index === ? 'bg-gray-00' : 'bg-orange-00'
 }`}>
 {index + }
 </div>
 <span className="font-medium text-gray-00">
 {formatDiseaseName(prob.disease)}
 </span>
 </div>
 <span className="text-sm font-medium text-gray-00">
 {(prob.probability * 00).toFixed()}%
 </span>
 </div>
 ))}
 </div>
 </div>
 </div>
 )}

 {/* Disclaimer */}
 <div className="bg-blue-0 border border-blue-00 rounded-lg p-">
 <div className="flex items-start space-x-">
 <AlertCircle className="h- w- text-blue-00 mt-0. flex-shrink-0" />
 <div className="text-sm text-blue-00">
 <p className="font-medium mb-">Important Medical Disclaimer</p>
 <p>
 This AI prediction is for informational purposes only and should not replace professional medical advice.
 Please consult with a healthcare provider for proper diagnosis and treatment.
 </p>
 </div>
 </div>
 </div>
 </div>

 {/* Footer */}
 <div className="flex justify-end p- border-t bg-gray-0">
 <button
 onClick={onClose}
 className="px- py- bg-blue-00 text-white rounded-lg hover:bg-blue-00 transition-colors font-medium"
 >
 Close
 </button>
 </div>
 </div>
 </div>
 );
};

export default PredictionResultModal;