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
        return 'text-red-600 bg-red-50 border-red-200';
      case 'medium':
        return 'text-yellow-600 bg-yellow-50 border-yellow-200';
      case 'low':
        return 'text-green-600 bg-green-50 border-green-200';
      default:
        return 'text-gray-600 bg-gray-50 border-gray-200';
    }
  };

  const getRiskIcon = (riskLevel: string) => {
    switch (riskLevel.toLowerCase()) {
      case 'high':
        return <AlertCircle className="h-5 w-5" />;
      case 'medium':
        return <Activity className="h-5 w-5" />;
      case 'low':
        return <CheckCircle className="h-5 w-5" />;
      default:
        return <Activity className="h-5 w-5" />;
    }
  };

  const formatDiseaseName = (disease: string) => {
    return disease.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase());
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div className="bg-white rounded-lg shadow-xl max-w-2xl w-full max-h-[90vh] overflow-y-auto">
        {/* Header */}
        <div className="flex items-center justify-between p-6 border-b">
          <div className="flex items-center space-x-3">
            <div className="p-2 bg-blue-100 rounded-lg">
              <Activity className="h-6 w-6 text-blue-600" />
            </div>
            <div>
              <h2 className="text-xl font-semibold text-gray-900">Prediction Results</h2>
              <p className="text-sm text-gray-600">AI-powered health risk assessment</p>
            </div>
          </div>
          <button
            onClick={onClose}
            className="p-2 hover:bg-gray-100 rounded-lg transition-colors"
          >
            <X className="h-5 w-5 text-gray-500" />
          </button>
        </div>

        {/* Main Content */}
        <div className="p-6 space-y-6">
          {/* Primary Prediction */}
          <div className="text-center space-y-4">
            <div>
              <h3 className="text-2xl font-bold text-gray-900 mb-2">
                {formatDiseaseName(prediction.predicted_disease)}
              </h3>
              <div className={`inline-flex items-center space-x-2 px-4 py-2 rounded-full border ${getRiskColor(prediction.risk_level)}`}>
                {getRiskIcon(prediction.risk_level)}
                <span className="font-medium">
                  {prediction.risk_level} Risk ({(prediction.confidence * 100).toFixed(1)}% confidence)
                </span>
              </div>
            </div>
            
            {/* Risk Score */}
            <div className="bg-gray-50 rounded-lg p-4">
              <div className="flex items-center justify-center space-x-2 mb-2">
                <TrendingUp className="h-4 w-4 text-gray-600" />
                <span className="text-sm font-medium text-gray-600">Risk Score</span>
              </div>
              <div className="text-3xl font-bold text-gray-900">
                {(prediction.risk_score * 100).toFixed(1)}%
              </div>
            </div>
          </div>

          {/* Probability Chart */}
          {prediction.all_class_probabilities && prediction.all_class_probabilities.length > 0 && (
            <div className="space-y-4">
              <div className="border-t pt-6">
                <h4 className="text-lg font-semibold text-gray-900 mb-2">
                  All Disease Probabilities
                </h4>
                <p className="text-sm text-gray-600 mb-4">
                  Likelihood of each possible condition based on your symptoms and water quality data
                </p>
                
                <div className="bg-gray-50 rounded-lg p-4">
                  <ProbabilityChart probabilities={prediction.all_class_probabilities} />
                </div>
              </div>

              {/* Top 3 Predictions */}
              <div className="space-y-3">
                <h5 className="font-medium text-gray-900">Top 3 Most Likely Conditions:</h5>
                <div className="space-y-2">
                  {prediction.all_class_probabilities.slice(0, 3).map((prob, index) => (
                    <div key={prob.disease} className="flex items-center justify-between p-3 bg-white border rounded-lg">
                      <div className="flex items-center space-x-3">
                        <div className={`w-6 h-6 rounded-full flex items-center justify-center text-xs font-bold text-white ${
                          index === 0 ? 'bg-yellow-500' : index === 1 ? 'bg-gray-400' : 'bg-orange-400'
                        }`}>
                          {index + 1}
                        </div>
                        <span className="font-medium text-gray-900">
                          {formatDiseaseName(prob.disease)}
                        </span>
                      </div>
                      <span className="text-sm font-medium text-gray-600">
                        {(prob.probability * 100).toFixed(1)}%
                      </span>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          )}

          {/* Disclaimer */}
          <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
            <div className="flex items-start space-x-3">
              <AlertCircle className="h-5 w-5 text-blue-600 mt-0.5 flex-shrink-0" />
              <div className="text-sm text-blue-800">
                <p className="font-medium mb-1">Important Medical Disclaimer</p>
                <p>
                  This AI prediction is for informational purposes only and should not replace professional medical advice. 
                  Please consult with a healthcare provider for proper diagnosis and treatment.
                </p>
              </div>
            </div>
          </div>
        </div>

        {/* Footer */}
        <div className="flex justify-end p-6 border-t bg-gray-50">
          <button
            onClick={onClose}
            className="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors font-medium"
          >
            Close
          </button>
        </div>
      </div>
    </div>
  );
};

export default PredictionResultModal;