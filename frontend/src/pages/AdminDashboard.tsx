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
  BarChart3,
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
  'Chennai': [13.0827, 80.2707],
  'Coimbatore': [11.0168, 76.9558],
  'Madurai': [9.9252, 78.1198],
  'Tiruchirappalli': [10.7905, 78.7047],
  'Salem': [11.6643, 78.1460],
  'Tirunelveli': [8.7139, 77.7567],
  'Vellore': [12.9165, 79.1325],
  'Erode': [11.3410, 77.7172],
  'Thanjavur': [10.7870, 79.1378],
  'Dindigul': [10.3673, 77.9803],
};

const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042', '#8884D8', '#82CA9D', '#FFC658', '#FF6B9D'];

// Memoized chart components for performance
const DiseaseDistributionChart = React.memo(({ data }: { data: any[] }) => {
  if (!data || data.length === 0) {
    return (
      <div className="flex items-center justify-center h-[300px] text-gray-500">
        <div className="text-center">
          <p className="text-lg mb-2">No disease data available</p>
          <p className="text-sm">Submit reports to see disease distribution</p>
        </div>
      </div>
    );
  }
  
  return (
    <ResponsiveContainer width="100%" height={300}>
      <PieChart>
        <Pie
          data={data}
          cx="50%"
          cy="50%"
          labelLine={false}
          label={({ name, percent }) => `${name}: ${((percent || 0) * 100).toFixed(0)}%`}
          outerRadius={80}
          fill="#8884d8"
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
  <ResponsiveContainer width="100%" height={300}>
    <BarChart data={data} layout="vertical">
      <CartesianGrid strokeDasharray="3 3" />
      <XAxis type="number" />
      <YAxis dataKey="name" type="category" width={150} tick={{ fontSize: 12 }} />
      <Tooltip />
      <Bar dataKey="importance" fill="#10B981" />
    </BarChart>
  </ResponsiveContainer>
));

const RainfallDiseaseChart = React.memo(({ data }: { data: any[] }) => (
  <ResponsiveContainer width="100%" height={300}>
    <LineChart data={data}>
      <CartesianGrid strokeDasharray="3 3" />
      <XAxis dataKey="month" />
      <YAxis yAxisId="left" />
      <YAxis yAxisId="right" orientation="right" />
      <Tooltip />
      <Legend />
      <Line yAxisId="left" type="monotone" dataKey="rainfall" stroke="#3B82F6" name="Rainfall (mm)" strokeWidth={2} />
      <Line yAxisId="right" type="monotone" dataKey="cases" stroke="#EF4444" name="Disease Cases" strokeWidth={2} />
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
      setFeatureImportance(featureResponse.data.top_10_features || []);
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

  // Auto-refresh polling every 10 seconds
  useEffect(() => {
    const intervalId = setInterval(() => {
      fetchDashboardData(false); // Don't show loading spinner for auto-refresh
    }, 10000); // 10 seconds

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
      const response = await reportsAPI.exportReports(7);
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', `reports_last_7_days_${new Date().toISOString().split('T')[0]}.csv`);
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
    if (riskIndex < 25) return '#10B981'; // Green for low risk
    if (riskIndex >= 25 && riskIndex < 50) return '#F59E0B'; // Yellow for medium risk
    return '#EF4444'; // Red for high risk (>= 50)
  };

  const getMarkerRadius = (riskIndex: number) => {
    if (riskIndex >= 50) return 15;
    if (riskIndex >= 25) return 10;
    return 7;
  };

  const getTrendColor = (trend: string) => {
    if (trend === 'rising') return '#EF4444'; // Red
    if (trend === 'falling') return '#10B981'; // Green
    return '#6B7280'; // Gray
  };

  const getTrendMessage = (trend: string, percentage: number) => {
    if (trend === 'rising') {
      return `⚠️ Risk rising by ${Math.abs(percentage).toFixed(1)}% vs last week`;
    } else if (trend === 'falling') {
      return `✅ Risk falling by ${Math.abs(percentage).toFixed(1)}% vs last week`;
    }
    return `➖ Risk stable (${percentage >= 0 ? '+' : ''}${percentage.toFixed(1)}% change)`;
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
      name: f.feature.replace(/_/g, ' ').substring(0, 20),
      importance: f.importance_percentage
    }))
  , [featureImportance]);

  // Prepare rainfall vs disease data (simulated for demo)
  const rainfallDiseaseData = [
    { month: 'Jan', rainfall: 50, cases: 120 },
    { month: 'Feb', rainfall: 40, cases: 100 },
    { month: 'Mar', rainfall: 60, cases: 140 },
    { month: 'Apr', rainfall: 80, cases: 180 },
    { month: 'May', rainfall: 120, cases: 250 },
    { month: 'Jun', rainfall: 150, cases: 320 },
    { month: 'Jul', rainfall: 180, cases: 380 },
    { month: 'Aug', rainfall: 160, cases: 340 },
    { month: 'Sep', rainfall: 140, cases: 290 },
    { month: 'Oct', rainfall: 200, cases: 420 },
    { month: 'Nov', rainfall: 180, cases: 380 },
    { month: 'Dec', rainfall: 100, cases: 200 },
  ];

  if (loading) {
    return <LoadingSpinner fullScreen text="Loading dashboard data..." />;
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b border-red-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center py-4">
            <div className="flex items-center space-x-3">
              <Shield className="h-8 w-8 text-red-600" />
              <div>
                <h1 className="text-xl font-bold text-gray-900">Admin Dashboard</h1>
                <p className="text-sm text-gray-500">Health Authority Control Panel</p>
              </div>
            </div>
            <div className="flex items-center space-x-4">
              {/* Live CSV Sync Indicator */}
              <div className="flex items-center space-x-2 px-3 py-1.5 bg-green-50 border border-green-200 rounded-md">
                <div className="flex items-center space-x-1.5">
                  <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></div>
                  <span className="text-xs font-medium text-green-700">Live CSV Sync Active</span>
                </div>
              </div>
              
              {/* Refresh Button */}
              <button
                onClick={handleManualRefresh}
                disabled={refreshing}
                className="flex items-center space-x-2 px-3 py-1.5 bg-blue-50 text-blue-700 rounded-md hover:bg-blue-100 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
                title="Refresh dashboard data"
              >
                <Activity className={`h-4 w-4 ${refreshing ? 'animate-spin' : ''}`} />
                <span className="text-sm font-medium">Refresh</span>
              </button>
              
              {/* Last Refresh Time */}
              <div className="text-xs text-gray-500">
                Updated: {lastRefresh.toLocaleTimeString()}
              </div>
              
              <div className="flex items-center space-x-2 text-sm">
                <User className="h-4 w-4 text-gray-400" />
                <span className="text-gray-700">{user?.email}</span>
                <span className="px-2 py-1 bg-red-100 text-red-800 rounded-full text-xs font-medium">
                  ADMIN
                </span>
              </div>
              <button
                onClick={logout}
                className="flex items-center space-x-2 text-gray-500 hover:text-gray-700 transition-colors"
              >
                <LogOut className="h-4 w-4" />
                <span className="hidden sm:inline">Logout</span>
              </button>
            </div>
          </div>
        </div>
      </header>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
        {/* Interactive Map */}
        <div className="bg-white rounded-lg shadow-sm border mb-6">
          <div className="p-6 border-b">
            <div className="flex items-center space-x-2">
              <MapPin className="h-5 w-5 text-blue-500" />
              <h2 className="text-lg font-semibold text-gray-900">Regional Risk Heatmap (7-Day Rolling Window)</h2>
            </div>
            <p className="text-sm text-gray-600 mt-1">
              Click on markers to view detailed risk information with trend analysis
            </p>
          </div>
          <div className="p-6">
            <div className="h-[450px] rounded-lg overflow-hidden border">
              <MapContainer
                center={[11.0, 78.0] as LatLngExpression}
                zoom={7}
                style={{ height: '100%', width: '100%' }}
              >
                <TileLayer
                  url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
                />
                {regionalRisk.map((data) => {
                  const coords: LatLngExpression = data.lat && data.lng 
                    ? [data.lat, data.lng]
                    : REGION_COORDINATES[data.region] || [11.0, 78.0];
                  
                  return (
                    <CircleMarker
                      key={data.region}
                      center={coords}
                      pathOptions={{
                        fillColor: getRiskColor(data.risk_index),
                        color: getTrendColor(data.trend),
                        weight: 3,
                        opacity: 1,
                        fillOpacity: 0.7
                      }}
                      radius={getMarkerRadius(data.risk_index)}
                    >
                      <Popup>
                        <div className="p-2 min-w-[250px]">
                          <h3 className="font-bold text-lg mb-2">{data.region}</h3>
                          
                          <div className="space-y-1 mb-3">
                            <p className="text-sm">
                              <span className="font-semibold">Risk Index:</span> {data.risk_index.toFixed(1)}/100
                            </p>
                            <p className="text-sm">
                              <span className="font-semibold">Risk Level:</span>{' '}
                              <span className={`font-bold ${
                                data.risk_level === 'High' ? 'text-red-600' :
                                data.risk_level === 'Medium' ? 'text-yellow-600' :
                                'text-green-600'
                              }`}>
                                {data.risk_level}
                              </span>
                            </p>
                            <p className="text-sm">
                              <span className="font-semibold">Reports (7d):</span> {data.total_predictions}
                            </p>
                          </div>
                          
                          <div className="border-t pt-2 mt-2">
                            <p className="text-xs font-semibold text-gray-700 mb-1">Trend Analysis:</p>
                            <div className={`text-sm p-2 rounded ${
                              data.trend === 'rising' ? 'bg-red-50 text-red-700' :
                              data.trend === 'falling' ? 'bg-green-50 text-green-700' :
                              'bg-gray-50 text-gray-700'
                            }`}>
                              {getTrendMessage(data.trend, data.trend_percentage)}
                            </div>
                          </div>
                          
                          <div className="border-t pt-2 mt-2 text-xs text-gray-600">
                            <p className="font-semibold mb-1">Additional Info:</p>
                            <p>• Base Risk: {data.base_risk.toFixed(1)}%</p>
                            <p>• Avg Fecal Coliform: {data.avg_fecal_coliform.toFixed(0)} per 100ml</p>
                          </div>
                          
                          {/* AI Risk Analysis Button - Available for all regions */}
                          <div className="border-t pt-2 mt-2">
                            <button
                              onClick={() => {
                                console.log("Opening AI Risk Analysis for:", data.region);
                                setSelectedRegionForDrivers(data.region);
                                setShowDriversModal(true);
                              }}
                              className="w-full px-3 py-2 bg-gradient-to-r from-blue-600 to-purple-600 text-white text-sm font-semibold rounded-lg hover:from-blue-700 hover:to-purple-700 transition-all shadow-md hover:shadow-lg flex items-center justify-center gap-2"
                            >
                              🔍 View AI Risk Analysis
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
            <div className="mt-4">
              <div className="flex items-center justify-center space-x-6 mb-3">
                <div className="flex items-center space-x-2">
                  <div className="w-4 h-4 rounded-full bg-green-500"></div>
                  <span className="text-sm text-gray-600">Low Risk (&lt;25)</span>
                </div>
                <div className="flex items-center space-x-2">
                  <div className="w-4 h-4 rounded-full bg-yellow-500"></div>
                  <span className="text-sm text-gray-600">Medium Risk (25-50)</span>
                </div>
                <div className="flex items-center space-x-2">
                  <div className="w-4 h-4 rounded-full bg-red-500"></div>
                  <span className="text-sm text-gray-600">High Risk (&gt;50)</span>
                </div>
              </div>
              <div className="flex items-center justify-center space-x-6">
                <div className="flex items-center space-x-2">
                  <div className="w-4 h-4 rounded-full border-2 border-red-500"></div>
                  <span className="text-sm text-gray-600">📈 Rising Trend</span>
                </div>
                <div className="flex items-center space-x-2">
                  <div className="w-4 h-4 rounded-full border-2 border-green-500"></div>
                  <span className="text-sm text-gray-600">📉 Falling Trend</span>
                </div>
                <div className="flex items-center space-x-2">
                  <div className="w-4 h-4 rounded-full border-2 border-gray-500"></div>
                  <span className="text-sm text-gray-600">➖ Stable Trend</span>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Weekly Reports Summary */}
        {weeklySummary && (
          <div className="bg-white rounded-lg shadow-sm border mb-6">
            <div className="p-6 border-b">
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-2">
                  <Calendar className="h-5 w-5 text-purple-500" />
                  <h2 className="text-lg font-semibold text-gray-900">📊 Weekly Report Summary</h2>
                </div>
                <button
                  onClick={handleExportReports}
                  className="flex items-center space-x-2 px-4 py-2 bg-green-600 text-white rounded-md hover:bg-green-700 transition-colors"
                >
                  <Download className="h-4 w-4" />
                  <span>Export CSV</span>
                </button>
              </div>
              <p className="text-sm text-gray-600 mt-1">
                Last 7 days • {new Date(weeklySummary.period.start).toLocaleDateString()} - {new Date(weeklySummary.period.end).toLocaleDateString()}
              </p>
            </div>
            
            <div className="p-6">
              <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-6">
                {/* Total Reports */}
                <div className="bg-gradient-to-br from-blue-50 to-blue-100 p-4 rounded-lg">
                  <div className="flex items-center justify-between">
                    <div>
                      <p className="text-sm text-blue-600 font-medium">Total Reports</p>
                      <p className="text-3xl font-bold text-blue-900 mt-1">{weeklySummary.total_reports}</p>
                    </div>
                    <Activity className="h-10 w-10 text-blue-500 opacity-50" />
                  </div>
                </div>
                
                {/* Top Region */}
                <div className="bg-gradient-to-br from-purple-50 to-purple-100 p-4 rounded-lg">
                  <div>
                    <p className="text-sm text-purple-600 font-medium">Top Region</p>
                    <p className="text-lg font-bold text-purple-900 mt-1">
                      {weeklySummary.by_region[0]?.region || 'N/A'}
                    </p>
                    <p className="text-sm text-purple-700 mt-1">
                      {weeklySummary.by_region[0]?.count || 0} reports
                    </p>
                  </div>
                </div>
                
                {/* Top Symptom */}
                <div className="bg-gradient-to-br from-orange-50 to-orange-100 p-4 rounded-lg">
                  <div>
                    <p className="text-sm text-orange-600 font-medium">Top Symptom</p>
                    <p className="text-lg font-bold text-orange-900 mt-1 capitalize">
                      {weeklySummary.by_symptom[0]?.symptom.replace('_', ' ') || 'N/A'}
                    </p>
                    <p className="text-sm text-orange-700 mt-1">
                      {weeklySummary.by_symptom[0]?.count || 0} cases
                    </p>
                  </div>
                </div>
              </div>
              
              <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                {/* Top 3 Affected Regions */}
                <div>
                  <h3 className="text-sm font-semibold text-gray-900 mb-3">Top 3 Affected Regions</h3>
                  <div className="space-y-3">
                    {weeklySummary.by_region.slice(0, 3).map((region, index) => (
                      <div key={region.region} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                        <div className="flex items-center space-x-3">
                          <div className={`w-8 h-8 rounded-full flex items-center justify-center font-bold text-white ${
                            index === 0 ? 'bg-yellow-500' : index === 1 ? 'bg-gray-400' : 'bg-orange-400'
                          }`}>
                            {index + 1}
                          </div>
                          <div>
                            <p className="font-medium text-gray-900">{region.region}</p>
                            <p className="text-xs text-gray-500">
                              {region.high_risk_count} high-risk cases
                            </p>
                          </div>
                        </div>
                        <div className="text-right">
                          <p className="text-lg font-bold text-gray-900">{region.count}</p>
                          <p className="text-xs text-gray-500">reports</p>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
                
                {/* Top 3 Common Symptoms */}
                <div>
                  <h3 className="text-sm font-semibold text-gray-900 mb-3">Top 3 Common Symptoms</h3>
                  <div className="space-y-3">
                    {weeklySummary.by_symptom.slice(0, 3).map((symptom, index) => {
                      const maxCount = weeklySummary.by_symptom[0]?.count || 1;
                      const percentage = (symptom.count / maxCount) * 100;
                      
                      return (
                        <div key={symptom.symptom} className="p-3 bg-gray-50 rounded-lg">
                          <div className="flex items-center justify-between mb-2">
                            <p className="font-medium text-gray-900 capitalize">
                              {symptom.symptom.replace('_', ' ')}
                            </p>
                            <p className="text-sm font-bold text-gray-900">{symptom.count}</p>
                          </div>
                          <div className="w-full bg-gray-200 rounded-full h-2">
                            <div
                              className={`h-2 rounded-full ${
                                index === 0 ? 'bg-red-500' : index === 1 ? 'bg-orange-500' : 'bg-yellow-500'
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
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
          {/* Disease Distribution Pie Chart */}
          <div className="bg-white rounded-lg shadow-sm border">
            <div className="p-6 border-b">
              <div className="flex items-center justify-between">
                <div>
                  <h2 className="text-lg font-semibold text-gray-900">Disease Distribution</h2>
                  <p className="text-sm text-gray-600">Breakdown of reported diseases (Last 7 days)</p>
                </div>
                <select
                  value={selectedRegion}
                  onChange={(e) => setSelectedRegion(e.target.value)}
                  className="px-3 py-2 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
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
            <div className="p-6">
              <DiseaseDistributionChart data={diseaseChartData} />
            </div>
          </div>

          {/* Feature Importance Bar Chart */}
          <div className="bg-white rounded-lg shadow-sm border">
            <div className="p-6 border-b">
              <div className="flex items-center space-x-2">
                <BarChart3 className="h-5 w-5 text-green-500" />
                <h2 className="text-lg font-semibold text-gray-900">Top Risk Drivers</h2>
              </div>
              <p className="text-sm text-gray-600">ML model feature importance</p>
            </div>
            <div className="p-6">
              <FeatureImportanceChart data={featureChartData} />
            </div>
          </div>
        </div>

        {/* Rainfall vs Disease Cases Line Chart */}
        <div className="bg-white rounded-lg shadow-sm border mb-6">
          <div className="p-6 border-b">
            <h2 className="text-lg font-semibold text-gray-900">Rainfall vs Disease Cases</h2>
            <p className="text-sm text-gray-600">Monthly correlation analysis</p>
          </div>
          <div className="p-6">
            <RainfallDiseaseChart data={rainfallDiseaseData} />
          </div>
        </div>

        {/* Alert Stats Cards */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-6">
          <div className="bg-gradient-to-br from-red-50 to-red-100 p-6 rounded-lg shadow-sm border border-red-200">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-red-600 font-medium">Active Alerts</p>
                <p className="text-3xl font-bold text-red-900 mt-1">
                  {alerts.filter(a => a.status === 'active' || !a.status).length}
                </p>
              </div>
              <div className="text-4xl">🚨</div>
            </div>
            <p className="text-xs text-red-600 mt-2">Requires immediate attention</p>
          </div>

          <div className="bg-gradient-to-br from-green-50 to-green-100 p-6 rounded-lg shadow-sm border border-green-200">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-green-600 font-medium">Resolved</p>
                <p className="text-3xl font-bold text-green-900 mt-1">
                  {alerts.filter(a => a.status === 'resolved').length}
                </p>
              </div>
              <div className="text-4xl">✅</div>
            </div>
            <p className="text-xs text-green-600 mt-2">Successfully addressed</p>
          </div>

          <div className="bg-gradient-to-br from-gray-50 to-gray-100 p-6 rounded-lg shadow-sm border border-gray-200">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-600 font-medium">Dismissed</p>
                <p className="text-3xl font-bold text-gray-900 mt-1">
                  {alerts.filter(a => a.status === 'dismissed').length}
                </p>
              </div>
              <div className="text-4xl">🗑️</div>
            </div>
            <p className="text-xs text-gray-600 mt-2">Marked as false positive</p>
          </div>
        </div>

        {/* Alert Table */}
        <div className="bg-white rounded-lg shadow-sm border">
          <div className="p-6 border-b">
            <div className="flex items-center justify-between">
              <div>
                <h2 className="text-lg font-semibold text-gray-900">Active Alerts</h2>
                <p className="text-sm text-gray-600">System-wide health alerts</p>
              </div>
              <button 
                onClick={() => setShowAlertModal(true)}
                className="bg-red-600 text-white px-4 py-2 rounded-md text-sm hover:bg-red-700 transition-colors"
              >
                Create Alert
              </button>
            </div>
          </div>
          <div className="overflow-x-auto">
            <table className="min-w-full divide-y divide-gray-200">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Region
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Risk Level
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Message
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Type
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Status
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Timestamp
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Actions
                  </th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                {alerts.length === 0 ? (
                  <tr>
                    <td colSpan={7} className="px-6 py-8 text-center text-gray-500">
                      No active alerts
                    </td>
                  </tr>
                ) : (
                  alerts.map((alert) => (
                    <tr key={alert.id} className="hover:bg-gray-50">
                      <td className="px-6 py-4 whitespace-nowrap">
                        <div className="flex items-center">
                          <MapPin className="h-4 w-4 text-gray-400 mr-2" />
                          <span className="text-sm font-medium text-gray-900">{alert.region}</span>
                        </div>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        {alert.risk_index && (
                          <span className="text-sm text-gray-900">{alert.risk_index}%</span>
                        )}
                      </td>
                      <td className="px-6 py-4">
                        <span className="text-sm text-gray-900">{alert.alert_message}</span>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        <span className={`px-2 py-1 text-xs font-medium rounded-full ${
                          alert.alert_type === 'critical' 
                            ? 'bg-red-100 text-red-800' 
                            : 'bg-yellow-100 text-yellow-800'
                        }`}>
                          {alert.alert_type}
                        </span>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        <span className={`px-2 py-1 text-xs font-medium rounded-full ${
                          alert.status === 'dismissed' 
                            ? 'bg-gray-100 text-gray-800'
                            : alert.status === 'resolved'
                            ? 'bg-green-100 text-green-800'
                            : alert.is_read 
                            ? 'bg-blue-100 text-blue-800' 
                            : 'bg-yellow-100 text-yellow-800'
                        }`}>
                          {alert.status === 'dismissed' ? 'Dismissed' : alert.status === 'resolved' ? 'Resolved' : alert.is_read ? 'Read' : 'Unread'}
                        </span>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                        {new Date(alert.timestamp).toLocaleString()}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm">
                        <div className="flex items-center space-x-2">
                          <button
                            onClick={() => handleResolveAlert(alert.id)}
                            className="text-green-600 hover:text-green-800 font-medium"
                            title="Mark as resolved"
                          >
                            Resolve
                          </button>
                          <span className="text-gray-300">|</span>
                          <button
                            onClick={() => handleDismissAlert(alert.id)}
                            className="text-red-600 hover:text-red-800 font-medium"
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
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
          <div className="bg-white rounded-lg shadow-xl max-w-md w-full">
            <div className="p-6 border-b flex items-center justify-between">
              <h3 className="text-lg font-semibold text-gray-900">Create New Alert</h3>
              <button
                onClick={() => setShowAlertModal(false)}
                className="text-gray-400 hover:text-gray-600"
              >
                <X className="h-5 w-5" />
              </button>
            </div>
            
            <form onSubmit={handleSubmitAlert} className="p-6 space-y-4">
              {/* Region */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Region <span className="text-red-500">*</span>
                </label>
                <select
                  value={alertForm.region}
                  onChange={(e) => setAlertForm({ ...alertForm, region: e.target.value })}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-red-500"
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
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Alert Type <span className="text-red-500">*</span>
                </label>
                <select
                  value={alertForm.alert_type}
                  onChange={(e) => setAlertForm({ ...alertForm, alert_type: e.target.value })}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-red-500"
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
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Priority
                </label>
                <select
                  value={alertForm.priority}
                  onChange={(e) => setAlertForm({ ...alertForm, priority: e.target.value })}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-red-500"
                >
                  <option value="low">Low</option>
                  <option value="medium">Medium</option>
                  <option value="high">High</option>
                </select>
              </div>

              {/* Message */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Alert Message <span className="text-red-500">*</span>
                </label>
                <textarea
                  value={alertForm.alert_message}
                  onChange={(e) => setAlertForm({ ...alertForm, alert_message: e.target.value })}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-red-500"
                  rows={4}
                  placeholder="Enter alert message..."
                  required
                />
                <p className="text-xs text-gray-500 mt-1">
                  {alertForm.alert_message.length} characters
                </p>
              </div>

              {/* Buttons */}
              <div className="flex space-x-3 pt-4">
                <button
                  type="button"
                  onClick={() => setShowAlertModal(false)}
                  className="flex-1 px-4 py-2 border border-gray-300 text-gray-700 rounded-md hover:bg-gray-50 transition-colors"
                  disabled={submittingAlert}
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="flex-1 px-4 py-2 bg-red-600 text-white rounded-md hover:bg-red-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
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
        days={7}
      />
    </div>
  );
};

export default AdminDashboard;