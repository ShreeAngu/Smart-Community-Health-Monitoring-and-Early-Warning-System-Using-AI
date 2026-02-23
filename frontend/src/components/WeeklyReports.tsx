import React, { useState, useEffect } from 'react';
import { Download, RefreshCw, Filter, Calendar, MapPin, Activity, AlertCircle } from 'lucide-react';

interface Report {
 id: number;
 region: string;
 timestamp: string;
 symptoms: Record<string, boolean>;
 risk_score: number;
 risk_level: 'Low' | 'Medium' | 'High';
 predicted_disease: string;
 user_id: number;
}

interface WeeklyReportsProps {
 onReportClick?: (report: Report) => void;
}

const WeeklyReports: React.FC<WeeklyReportsProps> = ({ onReportClick }) => {
 const [reports, setReports] = useState<Report[]>([]);
 const [loading, setLoading] = useState(true);
 const [refreshing, setRefreshing] = useState(false);
 const [filter, setFilter] = useState({
 region: 'all',
 risk: 'all'
 });
 const [lastUpdated, setLastUpdated] = useState<Date>(new Date());
 const [showFilters, setShowFilters] = useState(false);

 const fetchReports = async (isRefresh = false) => {
 try {
 if (isRefresh) {
 setRefreshing(true);
 } else {
 setLoading(true);
 }

 // Build query parameters
 const params = new URLSearchParams();
 params.append('days', '');
 if (filter.region !== 'all') params.append('region', filter.region);
 if (filter.risk !== 'all') params.append('risk_level', filter.risk);

 const response = await fetch(`http://localhost:000/reports/list?${params.toString()}`, {
 headers: {
 'Authorization': `Bearer ${localStorage.getItem('token')}`
 }
 });

 if (!response.ok) throw new Error('Failed to fetch reports');

 const data = await response.json();
 setReports(data.reports || []);
 setLastUpdated(new Date());

 } catch (error) {
 console.error('Failed to fetch reports:', error);
 } finally {
 setLoading(false);
 setRefreshing(false);
 }
 };

 // Auto-refresh every seconds
 useEffect(() => {
 fetchReports();
 const interval = setInterval(() => fetchReports(true), 000);
 return () => clearInterval(interval);
 }, [filter]);

 const handleExport = async () => {
 try {
 const response = await fetch('http://localhost:000/reports/export?days=', {
 headers: {
 'Authorization': `Bearer ${localStorage.getItem('token')}`
 }
 });

 if (!response.ok) throw new Error('Export failed');

 const blob = await response.blob();
 const url = window.URL.createObjectURL(blob);
 const link = document.createElement('a');
 link.href = url;
 link.setAttribute('download', `weekly_reports_${new Date().toISOString().split('T')[0]}.csv`);
 document.body.appendChild(link);
 link.click();
 link.remove();
 window.URL.revokeObjectURL(url);
 } catch (error) {
 console.error('Export failed:', error);
 }
 };

 const getRiskBadgeColor = (level: string) => {
 switch (level) {
 case 'High': return 'bg-red-00 text-red-00 border-red-00';
 case 'Medium': return 'bg-yellow-00 text-yellow-00 border-yellow-00';
 case 'Low': return 'bg-green-00 text-green-00 border-green-00';
 default: return 'bg-gray-00 text-gray-00 border-gray-00';
 }
 };

 const getRiskIcon = (level: string) => {
 switch (level) {
 case 'High': return <AlertCircle className="h- w-" />;
 case 'Medium': return <Activity className="h- w-" />;
 default: return <Activity className="h- w-" />;
 }
 };

 const countSymptoms = (symptoms: Record<string, boolean>) => {
 return Object.values(symptoms).filter(Boolean).length;
 };

 const formatDate = (dateString: string) => {
 const date = new Date(dateString);
 return date.toLocaleDateString('en-US', {
 month: 'short',
 day: 'numeric',
 hour: '-digit',
 minute: '-digit'
 });
 };

 const filteredReports = reports
 .filter(report => {
 if (filter.region !== 'all' && report.region !== filter.region) return false;
 if (filter.risk !== 'all' && report.risk_level !== filter.risk) return false;
 return true;
 })
 .slice(0, 0); // Limit to last 0 reports

 // Get unique regions for filter
 const uniqueRegions = Array.from(new Set(reports.map(r => r.region)));

 return (
 <div className="bg-white rounded-lg shadow-sm border">
 {/* Header */}
 <div className="p- border-b">
 <div className="flex items-center justify-between mb-">
 <div>
 <div className="flex items-center space-x-">
 <Calendar className="h- w- text-blue-00" />
 <h className="text-lg font-semibold text-gray-00">Recent Reports (Last 0)</h>
 </div>
 <p className="text-sm text-gray-00 mt-">
 Last updated: {lastUpdated.toLocaleTimeString()}
 <span className="ml- inline-flex items-center">
 <span className="h- w- bg-green-00 rounded-full animate-pulse mr-"></span>
 <span className="text-green-00 text-xs font-medium">Live</span>
 </span>
 </p>
 </div>

 <div className="flex items-center space-x-">
 <button
 onClick={() => setShowFilters(!showFilters)}
 className="flex items-center space-x- px- py- text-sm border border-gray-00 rounded-lg hover:bg-gray-0 transition-colors"
 >
 <Filter className="h- w-" />
 <span>Filters</span>
 </button>

 <button
 onClick={() => fetchReports(true)}
 disabled={refreshing}
 className="flex items-center space-x- px- py- text-sm border border-gray-00 rounded-lg hover:bg-gray-0 transition-colors disabled:opacity-0"
 >
 <RefreshCw className={`h- w- ${refreshing ? 'animate-spin' : ''}`} />
 <span>Refresh</span>
 </button>

 <button
 onClick={handleExport}
 className="flex items-center space-x- px- py- text-sm bg-blue-00 text-white rounded-lg hover:bg-blue-00 transition-colors"
 >
 <Download className="h- w-" />
 <span>Export CSV</span>
 </button>
 </div>
 </div>

 {/* Filters */}
 {showFilters && (
 <div className="flex items-center space-x- p- bg-gray-0 rounded-lg">
 <div>
 <label className="block text-xs font-medium text-gray-00 mb-">Region</label>
 <select
 value={filter.region}
 onChange={(e) => setFilter({ ...filter, region: e.target.value })}
 className="px- py-. text-sm border border-gray-00 rounded-lg focus:ring- focus:ring-blue-00 focus:border-blue-00"
 >
 <option value="all">All Regions</option>
 {uniqueRegions.map(region => (
 <option key={region} value={region}>{region}</option>
 ))}
 </select>
 </div>

 <div>
 <label className="block text-xs font-medium text-gray-00 mb-">Risk Level</label>
 <select
 value={filter.risk}
 onChange={(e) => setFilter({ ...filter, risk: e.target.value })}
 className="px- py-. text-sm border border-gray-00 rounded-lg focus:ring- focus:ring-blue-00 focus:border-blue-00"
 >
 <option value="all">All Levels</option>
 <option value="High">High Risk</option>
 <option value="Medium">Medium Risk</option>
 <option value="Low">Low Risk</option>
 </select>
 </div>

 <button
 onClick={() => setFilter({ region: 'all', risk: 'all' })}
 className="mt- text-sm text-blue-00 hover:text-blue-00"
 >
 Clear Filters
 </button>
 </div>
 )}
 </div>

 {/* Table */}
 <div className="overflow-x-auto">
 {loading ? (
 <div className="flex items-center justify-center py-">
 <div className="animate-spin rounded-full h- w- border-b- border-blue-00"></div>
 <span className="ml- text-gray-00">Loading reports...</span>
 </div>
 ) : filteredReports.length === 0 ? (
 <div className="text-center py-">
 <Calendar className="h- w- text-gray-00 mx-auto mb-" />
 <p className="text-gray-00">No reports found for the selected filters</p>
 <p className="text-sm text-gray-00 mt-">Try adjusting your filters or check back later</p>
 </div>
 ) : (
 <table className="w-full">
 <thead className="bg-gray-0 border-b">
 <tr>
 <th className="px- py- text-left text-xs font-medium text-gray-00 uppercase tracking-wider">
 ID
 </th>
 <th className="px- py- text-left text-xs font-medium text-gray-00 uppercase tracking-wider">
 Region
 </th>
 <th className="px- py- text-left text-xs font-medium text-gray-00 uppercase tracking-wider">
 Timestamp
 </th>
 <th className="px- py- text-left text-xs font-medium text-gray-00 uppercase tracking-wider">
 Symptoms
 </th>
 <th className="px- py- text-left text-xs font-medium text-gray-00 uppercase tracking-wider">
 Disease
 </th>
 <th className="px- py- text-left text-xs font-medium text-gray-00 uppercase tracking-wider">
 Risk
 </th>
 <th className="px- py- text-left text-xs font-medium text-gray-00 uppercase tracking-wider">
 Score
 </th>
 </tr>
 </thead>
 <tbody className="bg-white divide-y divide-gray-00">
 {filteredReports.map((report) => (
 <tr
 key={report.id}
 onClick={() => onReportClick?.(report)}
 className="hover:bg-gray-0 cursor-pointer transition-colors"
 >
 <td className="px- py- whitespace-nowrap text-sm font-medium text-gray-00">
 #{report.id}
 </td>
 <td className="px- py- whitespace-nowrap">
 <div className="flex items-center space-x- text-sm text-gray-00">
 <MapPin className="h- w- text-gray-00" />
 <span>{report.region}</span>
 </div>
 </td>
 <td className="px- py- whitespace-nowrap text-sm text-gray-00">
 {formatDate(report.timestamp)}
 </td>
 <td className="px- py- whitespace-nowrap">
 <span className="inline-flex items-center px-. py-0. rounded-full text-xs font-medium bg-blue-00 text-blue-00">
 {countSymptoms(report.symptoms)} symptoms
 </span>
 </td>
 <td className="px- py- whitespace-nowrap text-sm text-gray-00">
 {report.predicted_disease.replace(/_/g, ' ')}
 </td>
 <td className="px- py- whitespace-nowrap">
 <span className={`inline-flex items-center space-x- px-. py-0. rounded-full text-xs font-medium border ${getRiskBadgeColor(report.risk_level)}`}>
 {getRiskIcon(report.risk_level)}
 <span>{report.risk_level}</span>
 </span>
 </td>
 <td className="px- py- whitespace-nowrap text-sm font-medium text-gray-00">
 {report.risk_score.toFixed()}%
 </td>
 </tr>
 ))}
 </tbody>
 </table>
 )}
 </div>

 {/* Footer with stats */}
 {!loading && filteredReports.length > 0 && (
 <div className="px- py- bg-gray-0 border-t">
 <div className="flex items-center justify-between text-sm">
 <div className="text-gray-00">
 Showing <span className="font-medium text-gray-00">{filteredReports.length}</span> of{' '}
 <span className="font-medium text-gray-00">
 {reports.filter(report => {
 if (filter.region !== 'all' && report.region !== filter.region) return false;
 if (filter.risk !== 'all' && report.risk_level !== filter.risk) return false;
 return true;
 }).length}
 </span> reports
 {filter.region !== 'all' || filter.risk !== 'all' ? (
 <span className="ml-">(filtered)</span>
 ) : null}
 </div>
 <div className="flex items-center space-x- text-xs">
 <div className="flex items-center space-x-">
 <span className="h- w- bg-red-00 rounded-full"></span>
 <span className="text-gray-00">
 {filteredReports.filter(r => r.risk_level === 'High').length} High Risk
 </span>
 </div>
 <div className="flex items-center space-x-">
 <span className="h- w- bg-yellow-00 rounded-full"></span>
 <span className="text-gray-00">
 {filteredReports.filter(r => r.risk_level === 'Medium').length} Medium Risk
 </span>
 </div>
 <div className="flex items-center space-x-">
 <span className="h- w- bg-green-00 rounded-full"></span>
 <span className="text-gray-00">
 {filteredReports.filter(r => r.risk_level === 'Low').length} Low Risk
 </span>
 </div>
 </div>
 </div>
 </div>
 )}
 </div>
 );
};

export default WeeklyReports;