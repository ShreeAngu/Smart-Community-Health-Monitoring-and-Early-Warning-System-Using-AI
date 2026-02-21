import React, { useState, useEffect } from 'react';
import { X, TrendingUp, Activity, Droplet, AlertTriangle, Info, Zap, Target } from 'lucide-react';
import { predictionsAPI } from '../services/api';

interface RiskDriver {
  feature: string;
  feature_display: string;
  current_value: number;
  safe_value: number | string;
  risk_level: string;
  hybrid_score: number;
  bayesian_score: number;
  ml_importance: number;
  deviation_score: number;
  sample_count: number;
  std_dev: number;
  recommendation: string;
  icon: string;
  // New fields from updated backend
  bayesian_probability?: number;
  bayesian_label?: string;
  model_importance?: number;
  model_label?: string;
  hybrid_score_percentage?: number;
  hybrid_label?: string;
  current_value_display?: string;
  safe_value_display?: string;
  deviation_percentage?: number;
  deviation_direction?: string;
}

interface Summary {
  region: string;
  analysis_period_days: number;
  reports_analyzed: number;
  risk_drivers_identified: number;
  top_driver?: string;
  top_driver_score?: number;
  critical_factors?: number;
  recommendation: string;
  message?: string;
}

interface DriversData {
  region: string;
  days: number;
  report_count: number;
  drivers: RiskDriver[];
  summary: Summary;
  methodology: any;
  metadata: any;
}

interface BayesianDriversModalProps {
  region: string;
  isOpen: boolean;
  onClose: () => void;
  days?: number;
}

const BayesianDriversModal: React.FC<BayesianDriversModalProps> = ({
  region,
  isOpen,
  onClose,
  days = 7
}) => {
  const [data, setData] = useState<DriversData | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (isOpen && region) {
      fetchDrivers();
    }
  }, [isOpen, region, days]);

  const fetchDrivers = async () => {
    setLoading(true);
    setError(null);
    
    try {
      const response = await predictionsAPI.getRegionalDrivers(region, days);
      setData(response.data);
    } catch (err: any) {
      console.error('Error fetching risk drivers:', err);
      setError(err.response?.data?.detail || 'Failed to load risk drivers');
    } finally {
      setLoading(false);
    }
  };

  const getFeatureIcon = (feature: string): React.ReactElement => {
    const iconMap: { [key: string]: React.ReactElement } = {
      'fecal_coliform': <Droplet className="h-6 w-6" />,
      'turbidity': <Activity className="h-6 w-6" />,
      'ph': <TrendingUp className="h-6 w-6" />,
      'bod': <AlertTriangle className="h-6 w-6" />,
      'tds': <Zap className="h-6 w-6" />,
      'fluoride': <Target className="h-6 w-6" />,
      'arsenic': <AlertTriangle className="h-6 w-6" />,
      'nitrate': <Activity className="h-6 w-6" />,
    };

    const key = Object.keys(iconMap).find(k => feature.toLowerCase().includes(k));
    return key ? iconMap[key] : <Activity className="h-6 w-6" />;
  };

  const getRankBadgeColor = (rank: number) => {
    switch (rank) {
      case 1: return 'bg-gradient-to-r from-yellow-400 to-yellow-600';
      case 2: return 'bg-gradient-to-r from-gray-300 to-gray-500';
      case 3: return 'bg-gradient-to-r from-orange-400 to-orange-600';
      default: return 'bg-gradient-to-r from-blue-400 to-blue-600';
    }
  };

  const getScoreColor = (score: number) => {
    if (score >= 0.7) return 'text-red-600';
    if (score >= 0.5) return 'text-orange-600';
    if (score >= 0.3) return 'text-yellow-600';
    return 'text-green-600';
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 bg-black bg-opacity-60 flex items-center justify-center z-[9999] p-4 backdrop-blur-sm">
      <div className="bg-white rounded-2xl shadow-2xl max-w-5xl w-full max-h-[90vh] overflow-hidden">
        {/* Header */}
        <div className="bg-gradient-to-r from-blue-600 via-purple-600 to-indigo-600 text-white p-6">
          <div className="flex items-center justify-between">
            <div className="flex-1">
              <div className="flex items-center space-x-3 mb-2">
                <div className="bg-white bg-opacity-20 p-2 rounded-lg backdrop-blur-sm">
                  <Zap className="h-6 w-6" />
                </div>
                <div>
                  <h2 className="text-2xl font-bold">{region}</h2>
                  <p className="text-blue-100 text-sm">Hybrid Bayesian + XGBoost Analysis</p>
                </div>
              </div>
            </div>
            <button
              onClick={onClose}
              className="text-white hover:bg-white hover:bg-opacity-20 p-2 rounded-lg transition-colors"
            >
              <X className="h-6 w-6" />
            </button>
          </div>
        </div>

        {/* Content */}
        <div className="overflow-y-auto max-h-[calc(90vh-120px)]">
          {loading && (
            <div className="flex items-center justify-center py-20">
              <div className="text-center">
                <div className="animate-spin rounded-full h-16 w-16 border-b-4 border-blue-600 mx-auto mb-4"></div>
                <p className="text-gray-600 text-lg">Analyzing risk drivers...</p>
                <p className="text-gray-500 text-sm mt-2">Processing {region} data</p>
              </div>
            </div>
          )}

          {error && (
            <div className="p-6">
              <div className="bg-red-50 border-l-4 border-red-500 p-6 rounded-lg">
                <div className="flex items-center space-x-3">
                  <AlertTriangle className="h-6 w-6 text-red-600" />
                  <div>
                    <h3 className="text-red-800 font-semibold text-lg">Error Loading Data</h3>
                    <p className="text-red-700 mt-1">{error}</p>
                  </div>
                </div>
              </div>
            </div>
          )}

          {!loading && !error && data && (
            <div className="p-6 space-y-6">
              {/* Summary Card */}
              <div className="bg-gradient-to-br from-blue-50 to-indigo-50 border border-blue-200 rounded-xl p-6 shadow-sm">
                <div className="flex items-start space-x-4">
                  <div className="bg-blue-600 p-3 rounded-lg">
                    <Info className="h-6 w-6 text-white" />
                  </div>
                  <div className="flex-1">
                    <h3 className="text-lg font-bold text-gray-900 mb-3">AI Analysis Summary</h3>
                    
                    {data.summary.message ? (
                      <p className="text-gray-700">{data.summary.message}</p>
                    ) : (
                      <>
                        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-4">
                          <div className="bg-white bg-opacity-60 p-3 rounded-lg">
                            <p className="text-xs text-gray-600 mb-1">Reports Analyzed</p>
                            <p className="text-2xl font-bold text-blue-600">{data.summary.reports_analyzed}</p>
                          </div>
                          <div className="bg-white bg-opacity-60 p-3 rounded-lg">
                            <p className="text-xs text-gray-600 mb-1">Time Period</p>
                            <p className="text-2xl font-bold text-purple-600">{data.summary.analysis_period_days}d</p>
                          </div>
                          <div className="bg-white bg-opacity-60 p-3 rounded-lg">
                            <p className="text-xs text-gray-600 mb-1">Risk Drivers</p>
                            <p className="text-2xl font-bold text-orange-600">{data.summary.risk_drivers_identified}</p>
                          </div>
                          <div className="bg-white bg-opacity-60 p-3 rounded-lg">
                            <p className="text-xs text-gray-600 mb-1">Critical Factors</p>
                            <p className="text-2xl font-bold text-red-600">{data.summary.critical_factors || 0}</p>
                          </div>
                        </div>

                        <div className="bg-white bg-opacity-80 p-4 rounded-lg border-l-4 border-blue-600">
                          <p className="text-sm font-semibold text-gray-700 mb-1">Recommendation</p>
                          <p className="text-gray-900">{data.summary.recommendation}</p>
                        </div>
                      </>
                    )}
                  </div>
                </div>
              </div>

              {/* Risk Drivers List */}
              {data.drivers && data.drivers.length > 0 && (
                <div>
                  <h3 className="text-xl font-bold text-gray-900 mb-4 flex items-center space-x-2">
                    <TrendingUp className="h-6 w-6 text-red-600" />
                    <span>Top Risk Drivers</span>
                  </h3>

                  <div className="space-y-4">
                    {data.drivers.map((driver, index) => (
                      <div
                        key={index}
                        className="bg-white border-2 border-gray-200 rounded-xl p-6 shadow-lg hover:shadow-xl transition-shadow"
                      >
                        {/* Driver Header */}
                        <div className="flex items-start space-x-4 mb-4">
                          {/* Rank Badge */}
                          <div className={`${getRankBadgeColor(index + 1)} text-white font-bold text-xl px-4 py-2 rounded-lg shadow-md`}>
                            #{index + 1}
                          </div>

                          {/* Feature Icon */}
                          <div className="bg-gradient-to-br from-blue-500 to-purple-600 text-white p-3 rounded-lg">
                            {getFeatureIcon(driver.feature)}
                          </div>

                          {/* Feature Name */}
                          <div className="flex-1">
                            <h4 className="text-xl font-bold text-gray-900">{driver.feature_display}</h4>
                            <div className="flex items-center space-x-2 mt-1">
                              <span className="text-2xl">{driver.icon}</span>
                              <span className={`px-2 py-1 rounded-full text-xs font-semibold ${
                                driver.risk_level === 'high_risk' ? 'bg-red-100 text-red-800' :
                                driver.risk_level === 'elevated' ? 'bg-yellow-100 text-yellow-800' :
                                'bg-green-100 text-green-800'
                              }`}>
                                {driver.risk_level.replace('_', ' ').toUpperCase()}
                              </span>
                            </div>
                          </div>

                          {/* Hybrid Score */}
                          <div className="text-right">
                            <p className="text-xs text-gray-600 mb-1">Hybrid Score</p>
                            <p className={`text-3xl font-bold ${getScoreColor(driver.hybrid_score)}`}>
                              {(driver.hybrid_score * 100).toFixed(1)}
                            </p>
                          </div>
                        </div>

                        {/* Probability Section - Enhanced */}
                        <div className="grid grid-cols-2 gap-3 mt-4">
                          {/* Bayesian Probability */}
                          <div className="bg-gradient-to-br from-purple-50 to-purple-100 p-3 rounded-lg border border-purple-200">
                            <div className="flex items-center gap-2 mb-2">
                              <span className="text-lg">🎯</span>
                              <span className="text-xs font-bold text-purple-700">BAYESIAN PROBABILITY</span>
                            </div>
                            <div className="text-2xl font-bold text-purple-800">
                              {driver.bayesian_probability || (driver.bayesian_score * 100).toFixed(1)}%
                            </div>
                            <div className="text-xs text-purple-600 mt-1">
                              {driver.bayesian_label || 'P(High Risk | Feature Elevated)'}
                            </div>
                            <div className="mt-2 w-full bg-purple-200 rounded-full h-1.5">
                              <div 
                                className="h-1.5 rounded-full bg-purple-600 transition-all duration-500" 
                                style={{ width: `${Math.min(driver.bayesian_probability || (driver.bayesian_score * 100), 100)}%` }}
                              />
                            </div>
                          </div>

                          {/* Model Feature Importance */}
                          <div className="bg-gradient-to-br from-blue-50 to-blue-100 p-3 rounded-lg border border-blue-200">
                            <div className="flex items-center gap-2 mb-2">
                              <span className="text-lg">🤖</span>
                              <span className="text-xs font-bold text-blue-700">ML FEATURE IMPORTANCE</span>
                            </div>
                            <div className="text-2xl font-bold text-blue-800">
                              {driver.model_importance || (driver.ml_importance * 100).toFixed(2)}%
                            </div>
                            <div className="text-xs text-blue-600 mt-1">
                              {driver.model_label || 'XGBoost Feature Weight'}
                            </div>
                            <div className="mt-2 w-full bg-blue-200 rounded-full h-1.5">
                              <div 
                                className="h-1.5 rounded-full bg-blue-600 transition-all duration-500" 
                                style={{ width: `${Math.min(driver.model_importance || (driver.ml_importance * 100), 100)}%` }}
                              />
                            </div>
                          </div>
                        </div>

                        {/* Hybrid Score - Full Width */}
                        <div className="mt-4 bg-gradient-to-r from-red-50 to-orange-50 p-3 rounded-lg border border-red-200">
                          <div className="flex justify-between items-center mb-2">
                            <div className="flex items-center gap-2">
                              <span className="text-lg">⚡</span>
                              <span className="text-xs font-bold text-red-700">COMBINED RISK DRIVER SCORE</span>
                            </div>
                            <span className="text-lg font-bold text-red-800">
                              {driver.hybrid_score_percentage || (driver.hybrid_score * 100).toFixed(2)}%
                            </span>
                          </div>
                          <div className="text-xs text-red-600 mb-2">
                            {driver.hybrid_label || 'Hybrid Bayesian + ML + Deviation Score'}
                          </div>
                          <div className="w-full bg-red-200 rounded-full h-3">
                            <div 
                              className={`h-3 rounded-full transition-all duration-500 ${
                                (driver.hybrid_score_percentage || (driver.hybrid_score * 100)) > 70 ? 'bg-red-600' :
                                (driver.hybrid_score_percentage || (driver.hybrid_score * 100)) > 40 ? 'bg-orange-500' : 
                                'bg-yellow-500'
                              }`}
                              style={{ width: `${Math.min(driver.hybrid_score_percentage || (driver.hybrid_score * 100), 100)}%` }}
                            />
                          </div>
                          <div className="flex justify-between text-xs text-gray-500 mt-1">
                            <span>Low Priority</span>
                            <span>Medium</span>
                            <span>High Priority</span>
                          </div>
                        </div>

                        {/* Current vs Safe Values */}
                        <div className="grid grid-cols-2 gap-4 mt-4 mb-4">
                          <div className="bg-red-50 p-4 rounded-lg border-l-4 border-red-500">
                            <p className="text-xs text-red-700 font-semibold mb-1">Current Value</p>
                            <p className="text-2xl font-bold text-red-900">
                              {driver.current_value_display || driver.current_value}
                            </p>
                            <p className="text-xs text-red-600 mt-1">{driver.sample_count} samples</p>
                          </div>
                          <div className="bg-green-50 p-4 rounded-lg border-l-4 border-green-500">
                            <p className="text-xs text-green-700 font-semibold mb-1">Safe Threshold</p>
                            <p className="text-2xl font-bold text-green-900">
                              {driver.safe_value_display || driver.safe_value}
                            </p>
                            <p className="text-xs text-green-600 mt-1">WHO/BIS Standard</p>
                          </div>
                        </div>

                        {/* Recommendation */}
                        <div className="bg-blue-50 p-4 rounded-lg border border-blue-200">
                          <div className="flex items-start space-x-2">
                            <AlertTriangle className="h-5 w-5 text-blue-600 mt-0.5 flex-shrink-0" />
                            <div>
                              <p className="text-sm font-semibold text-blue-900 mb-1">Recommended Action</p>
                              <p className="text-sm text-blue-800">{driver.recommendation}</p>
                            </div>
                          </div>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </div>
          )}
        </div>

        {/* Footer */}
        <div className="bg-gray-50 px-6 py-4 border-t border-gray-200">
          <div className="flex items-center justify-between">
            <p className="text-sm text-gray-600">
              Powered by Hybrid Bayesian-ML Analysis
            </p>
            <button
              onClick={onClose}
              className="px-6 py-2 bg-gradient-to-r from-blue-600 to-purple-600 text-white rounded-lg hover:from-blue-700 hover:to-purple-700 transition-all shadow-md hover:shadow-lg font-semibold"
            >
              Close
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default BayesianDriversModal;
