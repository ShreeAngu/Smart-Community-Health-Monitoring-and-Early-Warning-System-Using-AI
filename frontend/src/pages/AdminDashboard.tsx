import React, { useState, useEffect, useCallback, useMemo } from 'react';
import { useAuth } from '../context/AuthContext';
import { predictionsAPI, alertsAPI, reportsAPI } from '../services/api';
import { MapContainer, TileLayer, CircleMarker, Popup } from 'react-leaflet';
import type { LatLngExpression } from 'leaflet';
import { PieChart, Pie, Cell, BarChart, Bar, LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import 'leaflet/dist/leaflet.css';
import LoadingSpinner from '../components/LoadingSpinner';
import WeeklyReports from '../components/WeeklyReports';
import BayesianDriversModal from '../components/BayesianDriversModal';
import {
 Shield,
 LogOut,
 MapPin,
 BarChart,
 TrendingUp,
 Activity,
 User,
 Download,
 Calendar,
 TrendingDown,
 X
} from 'lucide-react';

interface RegionalRiskData {
 region: string;
 risk_index: number;
 risk_level: string;
 trend: string;
 trend_emoji: string;
 trend_percentage: number;
 total_predictions: number;
 avg_fecal_coliform: number;
 base_risk: number;
 lat?: number;
 lng?: number;
}

interface FeatureImportance {
 feature: string;
 importance: number;
 importance_percentage: number;
}

interface DashboardStats {
 total_reports: number;
 total_predictions: number;
 high_risk_regions: number;
 recent_alerts: number;
 disease_distribution: Record<string, number>;
 risk_by_region: Record<string, string>;
}

interface Alert {
 id: number;
 region: string;
 alert_message: string;
 alert_type: string;
 risk_index?: number;
 timestamp: string;
 is_read: boolean;
 status?: string;
 resolved_at?: string;
 resolved_by?: number;
}

interface WeeklySummary {
 total_reports: number;
 by_region: Array<{
 region: string;
 count: number;
 high_risk_count: number;
 }>;
 by_symptom: Array<{
 symptom: string;
 count: number;
 }>;
 trend: string;
 trend_percentage: number;
 period: {
 start: string;
 end: string;
 };
}

// Sample coordinates for Tamil Nadu regions (you can adjust these)
const REGION_COORDINATES: Record<string, LatLngExpression> = {
 'Chennai': [.0, 0.0],
 'Coimbatore': [.0, .],
 'Madurai': [., .],
 'Tiruchirappalli': [0.0, .0],
 'Salem': [., .0],
 'Tirunelveli': [., .],
 'Vellore': [., .],
 'Erode': [.0, .],
 'Thanjavur': [0.0, .],
 'Dindigul': [0., .0],
};

const COLORS = ['#00FE', '#00CF', '#FFBB', '#FF0', '#D', '#CAD', '#FFC', '#FFBD'];

// Memoized chart components for performance
const DiseaseDistributionChart = React.memo(({ data }: { data: any[] }) => {
 if (!data || data.length === 0) {
 return (
 <div className="flex items-center justify-center h-[00px] text-gray-00">
 <div className="text-center">
 <p className="text-lg mb-">No disease data available</p>
 <p className="text-sm">Submit reports to see disease distribution</p>
 </div>
 </div>
 );
 }

 return (
 <ResponsiveContainer width="00%" height={00}>
 <PieChart>
 <Pie
 data={data}
 cx="0%"
 cy="0%"
 labelLine={false}
 label={({ name, percent }) => `${name}: ${((percent || 0) * 00).toFixed(0)}%`}
 outerRadius={0}
 fill="#d"
 dataKey="value"
 >
 {data.map((_, index) => (
 <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
 ))}
 </Pie>
 <Tooltip />
 </PieChart>
 </ResponsiveContainer>
 );
});

const FeatureImportanceChart = React.memo(({ data }: { data: any[] }) => (
 <ResponsiveContainer width="00%" height={00}>
 <BarChart data={data} layout="vertical">
 <CartesianGrid strokeDasharray=" " />
 <XAxis type="number" />
 <YAxis dataKey="name" type="category" width={0} tick={{ fontSize: }} />
 <Tooltip />
 <Bar dataKey="importance" fill="#0B" />
 </BarChart>
 </ResponsiveContainer>
));

const RainfallDiseaseChart = React.memo(({ data }: { data: any[] }) => (
 <ResponsiveContainer width="00%" height={00}>
 <LineChart data={data}>
 <CartesianGrid strokeDasharray=" " />
 <XAxis dataKey="month" />
 <YAxis yAxisId="left" />
 <YAxis yAxisId="right" orientation="right" />
 <Tooltip />
 <Legend />
 <Line yAxisId="left" type="monotone" dataKey="rainfall" stroke="#BF" name="Rainfall (mm)" strokeWidth={} />
 <Line yAxisId="right" type="monotone" dataKey="cases" stroke="#EF" name="Disease Cases" strokeWidth={} />
 </LineChart>
 </ResponsiveContainer>
));

const AdminDashboard: React.FC = () => {
 const { user, logout } = useAuth();
 const [regionalRisk, setRegionalRisk] = useState<RegionalRiskData[]>([]);
 const [featureImportance, setFeatureImportance] = useState<FeatureImportance[]>([]);
 const [stats, setStats] = useState<DashboardStats | null>(null);
 const [alerts, setAlerts] = useState<Alert[]>([]);
 const [weeklySummary, setWeeklySummary] = useState<WeeklySummary | null>(null);
 const [loading, setLoading] = useState(true);
 const [refreshing, setRefreshing] = useState(false);
 const [selectedRegion, setSelectedRegion] = useState<string>('all');
 const [lastRefresh, setLastRefresh] = useState<Date>(new Date());
 const [showAlertModal, setShowAlertModal] = useState(false);
 const [alertForm, setAlertForm] = useState({
 region: '',
 alert_type: 'warning',
 alert_message: '',
 priority: 'medium'
 });
 const [submittingAlert, setSubmittingAlert] = useState(false);
 const [showDriversModal, setShowDriversModal] = useState(false);
 const [selectedRegionForDrivers, setSelectedRegionForDrivers] = useState<string>('');

 // Fetch dashboard data function
 const fetchDashboardData = useCallback(async (showLoading = true) => {
 try {
 if (showLoading) {
 setLoading(true);
 } else {
 setRefreshing(true);
 }

 // Fetch all data in parallel
 const [riskResponse, featureResponse, alertsResponse, weeklyResponse] = await Promise.all([
 predictionsAPI.getRegionalRisk(),
 predictionsAPI.getFeatureImportance(),
 alertsAPI.getAlerts(),
 reportsAPI.getWeeklySummary()
 ]);

 setRegionalRisk(riskResponse.data || []);
 setFeatureImportance(featureResponse.data.top_0_features || []);
 setAlerts(alertsResponse.data || []);
 setWeeklySummary(weeklyResponse.data || null);
 setLastRefresh(new Date());

 // Calculate stats from regional risk data
 if (riskResponse.data && Array.isArray(riskResponse.data)) {
 const risks = riskResponse.data;
 const totalPredictions = risks.reduce((sum, r) => sum + (r.total_predictions || 0), 0);
 const highRiskRegions = risks.filter(r => r.risk_level === 'High').length;
 const recentAlerts = alertsResponse.data?.filter((a: Alert) => !a.is_read).length || 0;

 setStats({
 total_reports: weeklyResponse.data?.total_reports || totalPredictions,
 total_predictions: totalPredictions,
 high_risk_regions: highRiskRegions,
 recent_alerts: recentAlerts,
 disease_distribution: weeklyResponse.data?.disease_distribution || {},
 risk_by_region: Object.fromEntries(
 risks.map(r => [r.region, r.risk_level])
 )
 });
 }

 } catch (error) {
 console.error('Error fetching dashboard data:', error);
 } finally {
 setLoading(false);
 setRefreshing(false);
 }
 }, []);

 // Initial data fetch
 useEffect(() => {
 fetchDashboardData(true);
 }, [fetchDashboardData]);

 // Auto-refresh polling every 0 seconds
 useEffect(() => {
 const intervalId = setInterval(() => {
 fetchDashboardData(false); // Don't show loading spinner for auto-refresh
 }, 0000); // 0 seconds

 // Cleanup interval on unmount
 return () => clearInterval(intervalId);
 }, [fetchDashboardData]);

 // Manual refresh handler
 const handleManualRefresh = () => {
 fetchDashboardData(false);
 };

 // Export reports handler
 const handleExportReports = async () => {
 try {
 const response = await reportsAPI.exportReports();
 const url = window.URL.createObjectURL(new Blob([response.data]));
 const link = document.createElement('a');
 link.href = url;
 link.setAttribute('download', `reports_last__days_${new Date().toISOString().split('T')[0]}.csv`);
 document.body.appendChild(link);
 link.click();
 link.remove();
 } catch (error) {
 console.error('Error exporting reports:', error);
 alert('Failed to export reports. Please try again.');
 }
 };

 // Handle alert submission
 const handleSubmitAlert = async (e: React.FormEvent) => {
 e.preventDefault();

 console.log('Sending alert:', alertForm);

 if (!alertForm.region || !alertForm.alert_message) {
 alert('Please fill in all required fields');
 return;
 }

 setSubmittingAlert(true);

 try {
 await alertsAPI.createAlert({
 region: alertForm.region,
 alert_message: alertForm.alert_message,
 alert_type: alertForm.alert_type
 });

 alert('Alert created successfully!');

 // Reset form and close modal
 setAlertForm({
 region: '',
 alert_type: 'warning',
 alert_message: '',
 priority: 'medium'
 });
 setShowAlertModal(false);

 // Refresh alerts
 fetchDashboardData(false);

 } catch (error: any) {
 console.error('Error creating alert:', error);
 alert(error.response?.data?.detail || 'Failed to create alert. Please try again.');
 } finally {
 setSubmittingAlert(false);
 }
 };

 // Handle dismiss alert
 const handleDismissAlert = async (alertId: number) => {
 if (!confirm('Are you sure you want to dismiss this alert?')) {
 return;
 }

 try {
 await alertsAPI.dismissAlert(alertId, user?.id);

 // Refresh alerts
 fetchDashboardData(false);

 } catch (error: any) {
 console.error('Error dismissing alert:', error);
 alert(error.response?.data?.detail || 'Failed to dismiss alert. Please try again.');
 }
 };

 // Handle resolve alert
 const handleResolveAlert = async (alertId: number) => {
 if (!confirm('Mark this alert as resolved?')) {
 return;
 }

 try {
 await alertsAPI.resolveAlert(alertId, user?.id);

 // Refresh alerts
 fetchDashboardData(false);

 } catch (error: any) {
 console.error('Error resolving alert:', error);
 alert(error.response?.data?.detail || 'Failed to resolve alert. Please try again.');
 }
 };

 const getRiskColor = (riskIndex: number) => {
 if (riskIndex < ) return '#0B'; // Green for low risk
 if (riskIndex >= && riskIndex < 0) return '#FE0B'; // Yellow for medium risk
 return '#EF'; // Red for high risk (>= 0)
 };

 const getMarkerRadius = (riskIndex: number) => {
 if (riskIndex >= 0) return ;
 if (riskIndex >= ) return 0;
 return ;
 };

 const getTrendColor = (trend: string) => {
 if (trend === 'rising') return '#EF'; // Red
 if (trend === 'falling') return '#0B'; // Green
 return '#B0'; // Gray
 };

 const getTrendMessage = (trend: string, percentage: number) => {
 if (trend === 'rising') {
 return ` Risk rising by ${Math.abs(percentage).toFixed()}% vs last week`;
 } else if (trend === 'falling') {
 return ` Risk falling by ${Math.abs(percentage).toFixed()}% vs last week`;
 }
 return ` Risk stable (${percentage >= 0 ? '+' : ''}${percentage.toFixed()}% change)`;
 };

 // Prepare disease distribution data for pie chart - memoized
 const diseaseChartData = useMemo(() => {
 if (selectedRegion === 'all') {
 // Global disease distribution from weekly summary
 return stats?.disease_distribution
 ? Object.entries(stats.disease_distribution).map(([name, value]) => ({
 name: name.replace(/_/g, ' '),
 value
 }))
 : [];
 } else {
 // Region-specific disease distribution
 const regionData = regionalRisk.find(r => r.region === selectedRegion);
 if (regionData && (regionData as any).disease_distribution) {
 return Object.entries((regionData as any).disease_distribution).map(([name, value]) => ({
 name: name.replace(/_/g, ' '),
 value
 }));
 }
 return [];
 }
 }, [stats, regionalRisk, selectedRegion]);

 // Prepare feature importance data for bar chart - memoized
 const featureChartData = useMemo(() =>
 featureImportance.map(f => ({
 name: f.feature.replace(/_/g, ' ').substring(0, 0),
 importance: f.importance_percentage
 }))
 , [featureImportance]);

 // Prepare rainfall vs disease data (simulated for demo)
 const rainfallDiseaseData = [
 { month: 'Jan', rainfall: 0, cases: 0 },
 { month: 'Feb', rainfall: 0, cases: 00 },
 { month: 'Mar', rainfall: 0, cases: 0 },
 { month: 'Apr', rainfall: 0, cases: 0 },
 { month: 'May', rainfall: 0, cases: 0 },
 { month: 'Jun', rainfall: 0, cases: 0 },
 { month: 'Jul', rainfall: 0, cases: 0 },
 { month: 'Aug', rainfall: 0, cases: 0 },
 { month: 'Sep', rainfall: 0, cases: 0 },
 { month: 'Oct', rainfall: 00, cases: 0 },
 { month: 'Nov', rainfall: 0, cases: 0 },
 { month: 'Dec', rainfall: 00, cases: 00 },
 ];

 if (loading) {
 return <LoadingSpinner fullScreen text="Loading dashboard data..." />;
 }

 return (
 <div className="min-h-screen bg-gray-0">
 {/* Header */}
 <header className="bg-white shadow-sm border-b border-red-00">
 <div className="max-w-xl mx-auto px- sm:px- lg:px-">
 <div className="flex justify-between items-center py-">
 <div className="flex items-center space-x-">
 <Shield className="h- w- text-red-00" />
 <div>
 <h className="text-xl font-bold text-gray-00">Admin Dashboard</h>
 <p className="text-sm text-gray-00">Health Authority Control Panel</p>
 </div>
 </div>
 <div className="flex items-center space-x-">
 {/* Live CSV Sync Indicator */}
 <div className="flex items-center space-x- px- py-. bg-green-0 border border-green-00 rounded-md">
 <div className="flex items-center space-x-.">
 <div className="w- h- bg-green-00 rounded-full animate-pulse"></div>
 <span className="text-xs font-medium text-green-00">Live CSV Sync Active</span>
 </div>
 </div>

 {/* Refresh Button */}
 <button
 onClick={handleManualRefresh}
 disabled={refreshing}
 className="flex items-center space-x- px- py-. bg-blue-0 text-blue-00 rounded-md hover:bg-blue-00 transition-colors disabled:opacity-0 disabled:cursor-not-allowed"
 title="Refresh dashboard data"
 >
 <Activity className={`h- w- ${refreshing ? 'animate-spin' : ''}`} />
 <span className="text-sm font-medium">Refresh</span>
 </button>

 {/* Last Refresh Time */}
 <div className="text-xs text-gray-00">
 Updated: {lastRefresh.toLocaleTimeString()}
 </div>

 <div className="flex items-center space-x- text-sm">
 <User className="h- w- text-gray-00" />
 <span className="text-gray-00">{user?.email}</span>
 <span className="px- py- bg-red-00 text-red-00 rounded-full text-xs font-medium">
 ADMIN
 </span>
 </div>
 <button
 onClick={logout}
 className="flex items-center space-x- text-gray-00 hover:text-gray-00 transition-colors"
 >
 <LogOut className="h- w-" />
 <span className="hidden sm:inline">Logout</span>
 </button>
 </div>
 </div>
 </div>
 </header>

 <div className="max-w-xl mx-auto px- sm:px- lg:px- py-">
 {/* Interactive Map */}
 <div className="bg-white rounded-lg shadow-sm border mb-">
 <div className="p- border-b">
 <div className="flex items-center space-x-">
 <MapPin className="h- w- text-blue-00" />
 <h className="text-lg font-semibold text-gray-00">Regional Risk Heatmap (-Day Rolling Window)</h>
 </div>
 <p className="text-sm text-gray-00 mt-">
 Click on markers to view detailed risk information with trend analysis
 </p>
 </div>
 <div className="p-">
 <div className="h-[0px] rounded-lg overflow-hidden border">
 <MapContainer
 center={[.0, .0] as LatLngExpression}
 zoom={}
 style={{ height: '00%', width: '00%' }}
 >
 <TileLayer
 url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
 />
 {regionalRisk.map((data) => {
 const coords: LatLngExpression = data.lat && data.lng
 ? [data.lat, data.lng]
 : REGION_COORDINATES[data.region] || [.0, .0];

 return (
 <CircleMarker
 key={data.region}
 center={coords}
 pathOptions={{
 fillColor: getRiskColor(data.risk_index),
 color: getTrendColor(data.trend),
 weight: ,
 opacity: ,
 fillOpacity: 0.
 }}
 radius={getMarkerRadius(data.risk_index)}
 >
 <Popup>
 <div className="p- min-w-[0px]">
 <h className="font-bold text-lg mb-">{data.region}</h>

 <div className="space-y- mb-">
 <p className="text-sm">
 <span className="font-semibold">Risk Index:</span> {data.risk_index.toFixed()}/00
 </p>
 <p className="text-sm">
 <span className="font-semibold">Risk Level:</span>{' '}
 <span className={`font-bold ${
 data.risk_level === 'High' ? 'text-red-00' :
 data.risk_level === 'Medium' ? 'text-yellow-00' :
 'text-green-00'
 }`}>
 {data.risk_level}
 </span>
 </p>
 <p className="text-sm">
 <span className="font-semibold">Reports (d):</span> {data.total_predictions}
 </p>
 </div>

 <div className="border-t pt- mt-">
 <p className="text-xs font-semibold text-gray-00 mb-">Trend Analysis:</p>
 <div className={`text-sm p- rounded ${
 data.trend === 'rising' ? 'bg-red-0 text-red-00' :
 data.trend === 'falling' ? 'bg-green-0 text-green-00' :
 'bg-gray-0 text-gray-00'
 }`}>
 {getTrendMessage(data.trend, data.trend_percentage)}
 </div>
 </div>

 <div className="border-t pt- mt- text-xs text-gray-00">
 <p className="font-semibold mb-">Additional Info:</p>
 <p>• Base Risk: {data.base_risk.toFixed()}%</p>
 <p>• Avg Fecal Coliform: {data.avg_fecal_coliform.toFixed(0)} per 00ml</p>
 </div>

 {/* AI Risk Analysis Button - Available for all regions */}
 <div className="border-t pt- mt-">
 <button
 onClick={() => {
 console.log("Opening AI Risk Analysis for:", data.region);
 setSelectedRegionForDrivers(data.region);
 setShowDriversModal(true);
 }}
 className="w-full px- py- bg-gradient-to-r from-blue-00 to-purple-00 text-white text-sm font-semibold rounded-lg hover:from-blue-00 hover:to-purple-00 transition-all shadow-md hover:shadow-lg flex items-center justify-center gap-"
 >
 View AI Risk Analysis
 </button>
 </div>
 </div>
 </Popup>
 </CircleMarker>
 );
 })}
 </MapContainer>
 </div>

 {/* Legend */}
 <div className="mt-">
 <div className="flex items-center justify-center space-x- mb-">
 <div className="flex items-center space-x-">
 <div className="w- h- rounded-full bg-green-00"></div>
 <span className="text-sm text-gray-00">Low Risk (&lt;)</span>
 </div>
 <div className="flex items-center space-x-">
 <div className="w- h- rounded-full bg-yellow-00"></div>
 <span className="text-sm text-gray-00">Medium Risk (-0)</span>
 </div>
 <div className="flex items-center space-x-">
 <div className="w- h- rounded-full bg-red-00"></div>
 <span className="text-sm text-gray-00">High Risk (&gt;0)</span>
 </div>
 </div>
 <div className="flex items-center justify-center space-x-">
 <div className="flex items-center space-x-">
 <div className="w- h- rounded-full border- border-red-00"></div>
 <span className="text-sm text-gray-00"> Rising Trend</span>
 </div>
 <div className="flex items-center space-x-">
 <div className="w- h- rounded-full border- border-green-00"></div>
 <span className="text-sm text-gray-00"> Falling Trend</span>
 </div>
 <div className="flex items-center space-x-">
 <div className="w- h- rounded-full border- border-gray-00"></div>
 <span className="text-sm text-gray-00"> Stable Trend</span>
 </div>
 </div>
 </div>
 </div>
 </div>

 {/* Weekly Reports Summary */}
 {weeklySummary && (
 <div className="bg-white rounded-lg shadow-sm border mb-">
 <div className="p- border-b">
 <div className="flex items-center justify-between">
 <div className="flex items-center space-x-">
 <Calendar className="h- w- text-purple-00" />
 <h className="text-lg font-semibold text-gray-00"> Weekly Report Summary</h>
 </div>
 <button
 onClick={handleExportReports}
 className="flex items-center space-x- px- py- bg-green-00 text-white rounded-md hover:bg-green-00 transition-colors"
 >
 <Download className="h- w-" />
 <span>Export CSV</span>
 </button>
 </div>
 <p className="text-sm text-gray-00 mt-">
 Last days • {new Date(weeklySummary.period.start).toLocaleDateString()} - {new Date(weeklySummary.period.end).toLocaleDateString()}
 </p>
 </div>

 <div className="p-">
 <div className="grid grid-cols- md:grid-cols- gap- mb-">
 {/* Total Reports */}
 <div className="bg-gradient-to-br from-blue-0 to-blue-00 p- rounded-lg">
 <div className="flex items-center justify-between">
 <div>
 <p className="text-sm text-blue-00 font-medium">Total Reports</p>
 <p className="text-xl font-bold text-blue-00 mt-">{weeklySummary.total_reports}</p>
 </div>
 <Activity className="h-0 w-0 text-blue-00 opacity-0" />
 </div>
 </div>

 {/* Top Region */}
 <div className="bg-gradient-to-br from-purple-0 to-purple-00 p- rounded-lg">
 <div>
 <p className="text-sm text-purple-00 font-medium">Top Region</p>
 <p className="text-lg font-bold text-purple-00 mt-">
 {weeklySummary.by_region[0]?.region || 'N/A'}
 </p>
 <p className="text-sm text-purple-00 mt-">
 {weeklySummary.by_region[0]?.count || 0} reports
 </p>
 </div>
 </div>

 {/* Top Symptom */}
 <div className="bg-gradient-to-br from-orange-0 to-orange-00 p- rounded-lg">
 <div>
 <p className="text-sm text-orange-00 font-medium">Top Symptom</p>
 <p className="text-lg font-bold text-orange-00 mt- capitalize">
 {weeklySummary.by_symptom[0]?.symptom.replace('_', ' ') || 'N/A'}
 </p>
 <p className="text-sm text-orange-00 mt-">
 {weeklySummary.by_symptom[0]?.count || 0} cases
 </p>
 </div>
 </div>
 </div>

 <div className="grid grid-cols- lg:grid-cols- gap-">
 {/* Top Affected Regions */}
 <div>
 <h className="text-sm font-semibold text-gray-00 mb-">Top Affected Regions</h>
 <div className="space-y-">
 {weeklySummary.by_region.slice(0, ).map((region, index) => (
 <div key={region.region} className="flex items-center justify-between p- bg-gray-0 rounded-lg">
 <div className="flex items-center space-x-">
 <div className={`w- h- rounded-full flex items-center justify-center font-bold text-white ${
 index === 0 ? 'bg-yellow-00' : index === ? 'bg-gray-00' : 'bg-orange-00'
 }`}>
 {index + }
 </div>
 <div>
 <p className="font-medium text-gray-00">{region.region}</p>
 <p className="text-xs text-gray-00">
 {region.high_risk_count} high-risk cases
 </p>
 </div>
 </div>
 <div className="text-right">
 <p className="text-lg font-bold text-gray-00">{region.count}</p>
 <p className="text-xs text-gray-00">reports</p>
 </div>
 </div>
 ))}
 </div>
 </div>

 {/* Top Common Symptoms */}
 <div>
 <h className="text-sm font-semibold text-gray-00 mb-">Top Common Symptoms</h>
 <div className="space-y-">
 {weeklySummary.by_symptom.slice(0, ).map((symptom, index) => {
 const maxCount = weeklySummary.by_symptom[0]?.count || ;
 const percentage = (symptom.count / maxCount) * 00;

 return (
 <div key={symptom.symptom} className="p- bg-gray-0 rounded-lg">
 <div className="flex items-center justify-between mb-">
 <p className="font-medium text-gray-00 capitalize">
 {symptom.symptom.replace('_', ' ')}
 </p>
 <p className="text-sm font-bold text-gray-00">{symptom.count}</p>
 </div>
 <div className="w-full bg-gray-00 rounded-full h-">
 <div
 className={`h- rounded-full ${
 index === 0 ? 'bg-red-00' : index === ? 'bg-orange-00' : 'bg-yellow-00'
 }`}
 style={{ width: `${percentage}%` }}
 ></div>
 </div>
 </div>
 );
 })}
 </div>
 </div>
 </div>
 </div>
 </div>
 )}

 {/* Weekly Reports Live View */}
 <WeeklyReports />

 {/* Charts Grid */}
 <div className="grid grid-cols- lg:grid-cols- gap- mb-">
 {/* Disease Distribution Pie Chart */}
 <div className="bg-white rounded-lg shadow-sm border">
 <div className="p- border-b">
 <div className="flex items-center justify-between">
 <div>
 <h className="text-lg font-semibold text-gray-00">Disease Distribution</h>
 <p className="text-sm text-gray-00">Breakdown of reported diseases (Last days)</p>
 </div>
 <select
 value={selectedRegion}
 onChange={(e) => setSelectedRegion(e.target.value)}
 className="px- py- border border-gray-00 rounded-lg text-sm focus:ring- focus:ring-blue-00 focus:border-blue-00"
 >
 <option value="all">All Regions</option>
 {regionalRisk.map((risk) => (
 <option key={risk.region} value={risk.region}>
 {risk.region}
 </option>
 ))}
 </select>
 </div>
 </div>
 <div className="p-">
 <DiseaseDistributionChart data={diseaseChartData} />
 </div>
 </div>

 {/* Feature Importance Bar Chart */}
 <div className="bg-white rounded-lg shadow-sm border">
 <div className="p- border-b">
 <div className="flex items-center space-x-">
 <BarChart className="h- w- text-green-00" />
 <h className="text-lg font-semibold text-gray-00">Top Risk Drivers</h>
 </div>
 <p className="text-sm text-gray-00">ML model feature importance</p>
 </div>
 <div className="p-">
 <FeatureImportanceChart data={featureChartData} />
 </div>
 </div>
 </div>

 {/* Rainfall vs Disease Cases Line Chart */}
 <div className="bg-white rounded-lg shadow-sm border mb-">
 <div className="p- border-b">
 <h className="text-lg font-semibold text-gray-00">Rainfall vs Disease Cases</h>
 <p className="text-sm text-gray-00">Monthly correlation analysis</p>
 </div>
 <div className="p-">
 <RainfallDiseaseChart data={rainfallDiseaseData} />
 </div>
 </div>

 {/* Alert Stats Cards */}
 <div className="grid grid-cols- md:grid-cols- gap- mb-">
 <div className="bg-gradient-to-br from-red-0 to-red-00 p- rounded-lg shadow-sm border border-red-00">
 <div className="flex items-center justify-between">
 <div>
 <p className="text-sm text-red-00 font-medium">Active Alerts</p>
 <p className="text-xl font-bold text-red-00 mt-">
 {alerts.filter(a => a.status === 'active' || !a.status).length}
 </p>
 </div>
 <div className="text-xl"></div>
 </div>
 <p className="text-xs text-red-00 mt-">Requires immediate attention</p>
 </div>

 <div className="bg-gradient-to-br from-green-0 to-green-00 p- rounded-lg shadow-sm border border-green-00">
 <div className="flex items-center justify-between">
 <div>
 <p className="text-sm text-green-00 font-medium">Resolved</p>
 <p className="text-xl font-bold text-green-00 mt-">
 {alerts.filter(a => a.status === 'resolved').length}
 </p>
 </div>
 <div className="text-xl"></div>
 </div>
 <p className="text-xs text-green-00 mt-">Successfully addressed</p>
 </div>

 <div className="bg-gradient-to-br from-gray-0 to-gray-00 p- rounded-lg shadow-sm border border-gray-00">
 <div className="flex items-center justify-between">
 <div>
 <p className="text-sm text-gray-00 font-medium">Dismissed</p>
 <p className="text-xl font-bold text-gray-00 mt-">
 {alerts.filter(a => a.status === 'dismissed').length}
 </p>
 </div>
 <div className="text-xl"></div>
 </div>
 <p className="text-xs text-gray-00 mt-">Marked as false positive</p>
 </div>
 </div>

 {/* Alert Table */}
 <div className="bg-white rounded-lg shadow-sm border">
 <div className="p- border-b">
 <div className="flex items-center justify-between">
 <div>
 <h className="text-lg font-semibold text-gray-00">Active Alerts</h>
 <p className="text-sm text-gray-00">System-wide health alerts</p>
 </div>
 <button
 onClick={() => setShowAlertModal(true)}
 className="bg-red-00 text-white px- py- rounded-md text-sm hover:bg-red-00 transition-colors"
 >
 Create Alert
 </button>
 </div>
 </div>
 <div className="overflow-x-auto">
 <table className="min-w-full divide-y divide-gray-00">
 <thead className="bg-gray-0">
 <tr>
 <th className="px- py- text-left text-xs font-medium text-gray-00 uppercase tracking-wider">
 Region
 </th>
 <th className="px- py- text-left text-xs font-medium text-gray-00 uppercase tracking-wider">
 Risk Level
 </th>
 <th className="px- py- text-left text-xs font-medium text-gray-00 uppercase tracking-wider">
 Message
 </th>
 <th className="px- py- text-left text-xs font-medium text-gray-00 uppercase tracking-wider">
 Type
 </th>
 <th className="px- py- text-left text-xs font-medium text-gray-00 uppercase tracking-wider">
 Status
 </th>
 <th className="px- py- text-left text-xs font-medium text-gray-00 uppercase tracking-wider">
 Timestamp
 </th>
 <th className="px- py- text-left text-xs font-medium text-gray-00 uppercase tracking-wider">
 Actions
 </th>
 </tr>
 </thead>
 <tbody className="bg-white divide-y divide-gray-00">
 {alerts.length === 0 ? (
 <tr>
 <td colSpan={} className="px- py- text-center text-gray-00">
 No active alerts
 </td>
 </tr>
 ) : (
 alerts.map((alert) => (
 <tr key={alert.id} className="hover:bg-gray-0">
 <td className="px- py- whitespace-nowrap">
 <div className="flex items-center">
 <MapPin className="h- w- text-gray-00 mr-" />
 <span className="text-sm font-medium text-gray-00">{alert.region}</span>
 </div>
 </td>
 <td className="px- py- whitespace-nowrap">
 {alert.risk_index && (
 <span className="text-sm text-gray-00">{alert.risk_index}%</span>
 )}
 </td>
 <td className="px- py-">
 <span className="text-sm text-gray-00">{alert.alert_message}</span>
 </td>
 <td className="px- py- whitespace-nowrap">
 <span className={`px- py- text-xs font-medium rounded-full ${
 alert.alert_type === 'critical'
 ? 'bg-red-00 text-red-00'
 : 'bg-yellow-00 text-yellow-00'
 }`}>
 {alert.alert_type}
 </span>
 </td>
 <td className="px- py- whitespace-nowrap">
 <span className={`px- py- text-xs font-medium rounded-full ${
 alert.status === 'dismissed'
 ? 'bg-gray-00 text-gray-00'
 : alert.status === 'resolved'
 ? 'bg-green-00 text-green-00'
 : alert.is_read
 ? 'bg-blue-00 text-blue-00'
 : 'bg-yellow-00 text-yellow-00'
 }`}>
 {alert.status === 'dismissed' ? 'Dismissed' : alert.status === 'resolved' ? 'Resolved' : alert.is_read ? 'Read' : 'Unread'}
 </span>
 </td>
 <td className="px- py- whitespace-nowrap text-sm text-gray-00">
 {new Date(alert.timestamp).toLocaleString()}
 </td>
 <td className="px- py- whitespace-nowrap text-sm">
 <div className="flex items-center space-x-">
 <button
 onClick={() => handleResolveAlert(alert.id)}
 className="text-green-00 hover:text-green-00 font-medium"
 title="Mark as resolved"
 >
 Resolve
 </button>
 <span className="text-gray-00">|</span>
 <button
 onClick={() => handleDismissAlert(alert.id)}
 className="text-red-00 hover:text-red-00 font-medium"
 title="Dismiss alert"
 >
 Dismiss
 </button>
 </div>
 </td>
 </tr>
 ))
 )}
 </tbody>
 </table>
 </div>
 </div>
 </div>

 {/* Create Alert Modal */}
 {showAlertModal && (
 <div className="fixed inset-0 bg-black bg-opacity-0 flex items-center justify-center z-0 p-">
 <div className="bg-white rounded-lg shadow-xl max-w-md w-full">
 <div className="p- border-b flex items-center justify-between">
 <h className="text-lg font-semibold text-gray-00">Create New Alert</h>
 <button
 onClick={() => setShowAlertModal(false)}
 className="text-gray-00 hover:text-gray-00"
 >
 <X className="h- w-" />
 </button>
 </div>

 <form onSubmit={handleSubmitAlert} className="p- space-y-">
 {/* Region */}
 <div>
 <label className="block text-sm font-medium text-gray-00 mb-">
 Region <span className="text-red-00">*</span>
 </label>
 <select
 value={alertForm.region}
 onChange={(e) => setAlertForm({ ...alertForm, region: e.target.value })}
 className="w-full px- py- border border-gray-00 rounded-md focus:outline-none focus:ring- focus:ring-red-00"
 required
 >
 <option value="">Select Region</option>
 {regionalRisk.map((risk) => (
 <option key={risk.region} value={risk.region}>
 {risk.region}
 </option>
 ))}
 <option value="All Regions">All Regions</option>
 </select>
 </div>

 {/* Alert Type */}
 <div>
 <label className="block text-sm font-medium text-gray-00 mb-">
 Alert Type <span className="text-red-00">*</span>
 </label>
 <select
 value={alertForm.alert_type}
 onChange={(e) => setAlertForm({ ...alertForm, alert_type: e.target.value })}
 className="w-full px- py- border border-gray-00 rounded-md focus:outline-none focus:ring- focus:ring-red-00"
 required
 >
 <option value="info">Health Advisory</option>
 <option value="warning">Water Contamination</option>
 <option value="critical">Evacuation</option>
 <option value="other">Other</option>
 </select>
 </div>

 {/* Priority */}
 <div>
 <label className="block text-sm font-medium text-gray-00 mb-">
 Priority
 </label>
 <select
 value={alertForm.priority}
 onChange={(e) => setAlertForm({ ...alertForm, priority: e.target.value })}
 className="w-full px- py- border border-gray-00 rounded-md focus:outline-none focus:ring- focus:ring-red-00"
 >
 <option value="low">Low</option>
 <option value="medium">Medium</option>
 <option value="high">High</option>
 </select>
 </div>

 {/* Message */}
 <div>
 <label className="block text-sm font-medium text-gray-00 mb-">
 Alert Message <span className="text-red-00">*</span>
 </label>
 <textarea
 value={alertForm.alert_message}
 onChange={(e) => setAlertForm({ ...alertForm, alert_message: e.target.value })}
 className="w-full px- py- border border-gray-00 rounded-md focus:outline-none focus:ring- focus:ring-red-00"
 rows={}
 placeholder="Enter alert message..."
 required
 />
 <p className="text-xs text-gray-00 mt-">
 {alertForm.alert_message.length} characters
 </p>
 </div>

 {/* Buttons */}
 <div className="flex space-x- pt-">
 <button
 type="button"
 onClick={() => setShowAlertModal(false)}
 className="flex- px- py- border border-gray-00 text-gray-00 rounded-md hover:bg-gray-0 transition-colors"
 disabled={submittingAlert}
 >
 Cancel
 </button>
 <button
 type="submit"
 className="flex- px- py- bg-red-00 text-white rounded-md hover:bg-red-00 transition-colors disabled:opacity-0 disabled:cursor-not-allowed"
 disabled={submittingAlert}
 >
 {submittingAlert ? 'Creating...' : 'Create Alert'}
 </button>
 </div>
 </form>
 </div>
 </div>
 )}

 {/* Bayesian Risk Drivers Modal */}
 <BayesianDriversModal
 region={selectedRegionForDrivers}
 isOpen={showDriversModal}
 onClose={() => setShowDriversModal(false)}
 days={}
 />
 </div>
 );
};

export default AdminDashboard;