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
 days =
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
 'fecal_coliform': <Droplet className="h- w-" />,
 'turbidity': <Activity className="h- w-" />,
 'ph': <TrendingUp className="h- w-" />,
 'bod': <AlertTriangle className="h- w-" />,
 'tds': <Zap className="h- w-" />,
 'fluoride': <Target className="h- w-" />,
 'arsenic': <AlertTriangle className="h- w-" />,
 'nitrate': <Activity className="h- w-" />,
 };

 const key = Object.keys(iconMap).find(k => feature.toLowerCase().includes(k));
 return key ? iconMap[key] : <Activity className="h- w-" />;
 };

 const getRankBadgeColor = (rank: number) => {
 switch (rank) {
 case : return 'bg-gradient-to-r from-yellow-00 to-yellow-00';
 case : return 'bg-gradient-to-r from-gray-00 to-gray-00';
 case : return 'bg-gradient-to-r from-orange-00 to-orange-00';
 default: return 'bg-gradient-to-r from-blue-00 to-blue-00';
 }
 };

 const getScoreColor = (score: number) => {
 if (score >= 0.) return 'text-red-00';
 if (score >= 0.) return 'text-orange-00';
 if (score >= 0.) return 'text-yellow-00';
 return 'text-green-00';
 };

 if (!isOpen) return null;

 return (
 <div className="fixed inset-0 bg-black bg-opacity-0 flex items-center justify-center z-[] p- backdrop-blur-sm">
 <div className="bg-white rounded-xl shadow-xl max-w-xl w-full max-h-[0vh] overflow-hidden">
 {/* Header */}
 <div className="bg-gradient-to-r from-blue-00 via-purple-00 to-indigo-00 text-white p-">
 <div className="flex items-center justify-between">
 <div className="flex-">
 <div className="flex items-center space-x- mb-">
 <div className="bg-white bg-opacity-0 p- rounded-lg backdrop-blur-sm">
 <Zap className="h- w-" />
 </div>
 <div>
 <h className="text-xl font-bold">{region}</h>
 <p className="text-blue-00 text-sm">Hybrid Bayesian + XGBoost Analysis</p>
 </div>
 </div>
 </div>
 <button
 onClick={onClose}
 className="text-white hover:bg-white hover:bg-opacity-0 p- rounded-lg transition-colors"
 >
 <X className="h- w-" />
 </button>
 </div>
 </div>

 {/* Content */}
 <div className="overflow-y-auto max-h-[calc(0vh-0px)]">
 {loading && (
 <div className="flex items-center justify-center py-0">
 <div className="text-center">
 <div className="animate-spin rounded-full h- w- border-b- border-blue-00 mx-auto mb-"></div>
 <p className="text-gray-00 text-lg">Analyzing risk drivers...</p>
 <p className="text-gray-00 text-sm mt-">Processing {region} data</p>
 </div>
 </div>
 )}

 {error && (
 <div className="p-">
 <div className="bg-red-0 border-l- border-red-00 p- rounded-lg">
 <div className="flex items-center space-x-">
 <AlertTriangle className="h- w- text-red-00" />
 <div>
 <h className="text-red-00 font-semibold text-lg">Error Loading Data</h>
 <p className="text-red-00 mt-">{error}</p>
 </div>
 </div>
 </div>
 </div>
 )}

 {!loading && !error && data && (
 <div className="p- space-y-">
 {/* Summary Card */}
 <div className="bg-gradient-to-br from-blue-0 to-indigo-0 border border-blue-00 rounded-xl p- shadow-sm">
 <div className="flex items-start space-x-">
 <div className="bg-blue-00 p- rounded-lg">
 <Info className="h- w- text-white" />
 </div>
 <div className="flex-">
 <h className="text-lg font-bold text-gray-00 mb-">AI Analysis Summary</h>

 {data.summary.message ? (
 <p className="text-gray-00">{data.summary.message}</p>
 ) : (
 <>
 <div className="grid grid-cols- md:grid-cols- gap- mb-">
 <div className="bg-white bg-opacity-0 p- rounded-lg">
 <p className="text-xs text-gray-00 mb-">Reports Analyzed</p>
 <p className="text-xl font-bold text-blue-00">{data.summary.reports_analyzed}</p>
 </div>
 <div className="bg-white bg-opacity-0 p- rounded-lg">
 <p className="text-xs text-gray-00 mb-">Time Period</p>
 <p className="text-xl font-bold text-purple-00">{data.summary.analysis_period_days}d</p>
 </div>
 <div className="bg-white bg-opacity-0 p- rounded-lg">
 <p className="text-xs text-gray-00 mb-">Risk Drivers</p>
 <p className="text-xl font-bold text-orange-00">{data.summary.risk_drivers_identified}</p>
 </div>
 <div className="bg-white bg-opacity-0 p- rounded-lg">
 <p className="text-xs text-gray-00 mb-">Critical Factors</p>
 <p className="text-xl font-bold text-red-00">{data.summary.critical_factors || 0}</p>
 </div>
 </div>

 <div className="bg-white bg-opacity-0 p- rounded-lg border-l- border-blue-00">
 <p className="text-sm font-semibold text-gray-00 mb-">Recommendation</p>
 <p className="text-gray-00">{data.summary.recommendation}</p>
 </div>
 </>
 )}
 </div>
 </div>
 </div>

 {/* Risk Drivers List */}
 {data.drivers && data.drivers.length > 0 && (
 <div>
 <h className="text-xl font-bold text-gray-00 mb- flex items-center space-x-">
 <TrendingUp className="h- w- text-red-00" />
 <span>Top Risk Drivers</span>
 </h>

 <div className="space-y-">
 {data.drivers.map((driver, index) => (
 <div
 key={index}
 className="bg-white border- border-gray-00 rounded-xl p- shadow-lg hover:shadow-xl transition-shadow"
 >
 {/* Driver Header */}
 <div className="flex items-start space-x- mb-">
 {/* Rank Badge */}
 <div className={`${getRankBadgeColor(index + )} text-white font-bold text-xl px- py- rounded-lg shadow-md`}>
 #{index + }
 </div>

 {/* Feature Icon */}
 <div className="bg-gradient-to-br from-blue-00 to-purple-00 text-white p- rounded-lg">
 {getFeatureIcon(driver.feature)}
 </div>

 {/* Feature Name */}
 <div className="flex-">
 <h className="text-xl font-bold text-gray-00">{driver.feature_display}</h>
 <div className="flex items-center space-x- mt-">
 <span className="text-xl">{driver.icon}</span>
 <span className={`px- py- rounded-full text-xs font-semibold ${
 driver.risk_level === 'high_risk' ? 'bg-red-00 text-red-00' :
 driver.risk_level === 'elevated' ? 'bg-yellow-00 text-yellow-00' :
 'bg-green-00 text-green-00'
 }`}>
 {driver.risk_level.replace('_', ' ').toUpperCase()}
 </span>
 </div>
 </div>

 {/* Hybrid Score */}
 <div className="text-right">
 <p className="text-xs text-gray-00 mb-">Hybrid Score</p>
 <p className={`text-xl font-bold ${getScoreColor(driver.hybrid_score)}`}>
 {(driver.hybrid_score * 00).toFixed()}
 </p>
 </div>
 </div>

 {/* Probability Section - Enhanced */}
 <div className="grid grid-cols- gap- mt-">
 {/* Bayesian Probability */}
 <div className="bg-gradient-to-br from-purple-0 to-purple-00 p- rounded-lg border border-purple-00">
 <div className="flex items-center gap- mb-">
 <span className="text-lg"></span>
 <span className="text-xs font-bold text-purple-00">BAYESIAN PROBABILITY</span>
 </div>
 <div className="text-xl font-bold text-purple-00">
 {driver.bayesian_probability || (driver.bayesian_score * 00).toFixed()}%
 </div>
 <div className="text-xs text-purple-00 mt-">
 {driver.bayesian_label || 'P(High Risk | Feature Elevated)'}
 </div>
 <div className="mt- w-full bg-purple-00 rounded-full h-.">
 <div
 className="h-. rounded-full bg-purple-00 transition-all duration-00"
 style={{ width: `${Math.min(driver.bayesian_probability || (driver.bayesian_score * 00), 00)}%` }}
 />
 </div>
 </div>

 {/* Model Feature Importance */}
 <div className="bg-gradient-to-br from-blue-0 to-blue-00 p- rounded-lg border border-blue-00">
 <div className="flex items-center gap- mb-">
 <span className="text-lg"></span>
 <span className="text-xs font-bold text-blue-00">ML FEATURE IMPORTANCE</span>
 </div>
 <div className="text-xl font-bold text-blue-00">
 {driver.model_importance || (driver.ml_importance * 00).toFixed()}%
 </div>
 <div className="text-xs text-blue-00 mt-">
 {driver.model_label || 'XGBoost Feature Weight'}
 </div>
 <div className="mt- w-full bg-blue-00 rounded-full h-.">
 <div
 className="h-. rounded-full bg-blue-00 transition-all duration-00"
 style={{ width: `${Math.min(driver.model_importance || (driver.ml_importance * 00), 00)}%` }}
 />
 </div>
 </div>
 </div>

 {/* Hybrid Score - Full Width */}
 <div className="mt- bg-gradient-to-r from-red-0 to-orange-0 p- rounded-lg border border-red-00">
 <div className="flex justify-between items-center mb-">
 <div className="flex items-center gap-">
 <span className="text-lg"></span>
 <span className="text-xs font-bold text-red-00">COMBINED RISK DRIVER SCORE</span>
 </div>
 <span className="text-lg font-bold text-red-00">
 {driver.hybrid_score_percentage || (driver.hybrid_score * 00).toFixed()}%
 </span>
 </div>
 <div className="text-xs text-red-00 mb-">
 {driver.hybrid_label || 'Hybrid Bayesian + ML + Deviation Score'}
 </div>
 <div className="w-full bg-red-00 rounded-full h-">
 <div
 className={`h- rounded-full transition-all duration-00 ${
 (driver.hybrid_score_percentage || (driver.hybrid_score * 00)) > 0 ? 'bg-red-00' :
 (driver.hybrid_score_percentage || (driver.hybrid_score * 00)) > 0 ? 'bg-orange-00' :
 'bg-yellow-00'
 }`}
 style={{ width: `${Math.min(driver.hybrid_score_percentage || (driver.hybrid_score * 00), 00)}%` }}
 />
 </div>
 <div className="flex justify-between text-xs text-gray-00 mt-">
 <span>Low Priority</span>
 <span>Medium</span>
 <span>High Priority</span>
 </div>
 </div>

 {/* Current vs Safe Values */}
 <div className="grid grid-cols- gap- mt- mb-">
 <div className="bg-red-0 p- rounded-lg border-l- border-red-00">
 <p className="text-xs text-red-00 font-semibold mb-">Current Value</p>
 <p className="text-xl font-bold text-red-00">
 {driver.current_value_display || driver.current_value}
 </p>
 <p className="text-xs text-red-00 mt-">{driver.sample_count} samples</p>
 </div>
 <div className="bg-green-0 p- rounded-lg border-l- border-green-00">
 <p className="text-xs text-green-00 font-semibold mb-">Safe Threshold</p>
 <p className="text-xl font-bold text-green-00">
 {driver.safe_value_display || driver.safe_value}
 </p>
 <p className="text-xs text-green-00 mt-">WHO/BIS Standard</p>
 </div>
 </div>

 {/* Recommendation */}
 <div className="bg-blue-0 p- rounded-lg border border-blue-00">
 <div className="flex items-start space-x-">
 <AlertTriangle className="h- w- text-blue-00 mt-0. flex-shrink-0" />
 <div>
 <p className="text-sm font-semibold text-blue-00 mb-">Recommended Action</p>
 <p className="text-sm text-blue-00">{driver.recommendation}</p>
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
 <div className="bg-gray-0 px- py- border-t border-gray-00">
 <div className="flex items-center justify-between">
 <p className="text-sm text-gray-00">
 Powered by Hybrid Bayesian-ML Analysis
 </p>
 <button
 onClick={onClose}
 className="px- py- bg-gradient-to-r from-blue-00 to-purple-00 text-white rounded-lg hover:from-blue-00 hover:to-purple-00 transition-all shadow-md hover:shadow-lg font-semibold"
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
