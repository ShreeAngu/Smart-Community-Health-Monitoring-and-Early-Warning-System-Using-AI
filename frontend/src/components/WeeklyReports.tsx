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
      params.append('days', '7');
      if (filter.region !== 'all') params.append('region', filter.region);
      if (filter.risk !== 'all') params.append('risk_level', filter.risk);

      const response = await fetch(`http://localhost:8000/reports/list?${params.toString()}`, {
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

  // Auto-refresh every 15 seconds
  useEffect(() => {
    fetchReports();
    const interval = setInterval(() => fetchReports(true), 15000);
    return () => clearInterval(interval);
  }, [filter]);

  const handleExport = async () => {
    try {
      const response = await fetch('http://localhost:8000/reports/export?days=7', {
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
      case 'High': return 'bg-red-100 text-red-800 border-red-200';
      case 'Medium': return 'bg-yellow-100 text-yellow-800 border-yellow-200';
      case 'Low': return 'bg-green-100 text-green-800 border-green-200';
      default: return 'bg-gray-100 text-gray-800 border-gray-200';
    }
  };

  const getRiskIcon = (level: string) => {
    switch (level) {
      case 'High': return <AlertCircle className="h-3 w-3" />;
      case 'Medium': return <Activity className="h-3 w-3" />;
      default: return <Activity className="h-3 w-3" />;
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
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  const filteredReports = reports
    .filter(report => {
      if (filter.region !== 'all' && report.region !== filter.region) return false;
      if (filter.risk !== 'all' && report.risk_level !== filter.risk) return false;
      return true;
    })
    .slice(0, 10); // Limit to last 10 reports

  // Get unique regions for filter
  const uniqueRegions = Array.from(new Set(reports.map(r => r.region)));

  return (
    <div className="bg-white rounded-lg shadow-sm border">
      {/* Header */}
      <div className="p-6 border-b">
        <div className="flex items-center justify-between mb-4">
          <div>
            <div className="flex items-center space-x-2">
              <Calendar className="h-5 w-5 text-blue-500" />
              <h3 className="text-lg font-semibold text-gray-900">Recent Reports (Last 10)</h3>
            </div>
            <p className="text-sm text-gray-500 mt-1">
              Last updated: {lastUpdated.toLocaleTimeString()}
              <span className="ml-2 inline-flex items-center">
                <span className="h-2 w-2 bg-green-500 rounded-full animate-pulse mr-1"></span>
                <span className="text-green-600 text-xs font-medium">Live</span>
              </span>
            </p>
          </div>

          <div className="flex items-center space-x-2">
            <button
              onClick={() => setShowFilters(!showFilters)}
              className="flex items-center space-x-1 px-3 py-2 text-sm border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors"
            >
              <Filter className="h-4 w-4" />
              <span>Filters</span>
            </button>

            <button
              onClick={() => fetchReports(true)}
              disabled={refreshing}
              className="flex items-center space-x-1 px-3 py-2 text-sm border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors disabled:opacity-50"
            >
              <RefreshCw className={`h-4 w-4 ${refreshing ? 'animate-spin' : ''}`} />
              <span>Refresh</span>
            </button>

            <button
              onClick={handleExport}
              className="flex items-center space-x-1 px-3 py-2 text-sm bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
            >
              <Download className="h-4 w-4" />
              <span>Export CSV</span>
            </button>
          </div>
        </div>

        {/* Filters */}
        {showFilters && (
          <div className="flex items-center space-x-4 p-4 bg-gray-50 rounded-lg">
            <div>
              <label className="block text-xs font-medium text-gray-700 mb-1">Region</label>
              <select
                value={filter.region}
                onChange={(e) => setFilter({ ...filter, region: e.target.value })}
                className="px-3 py-1.5 text-sm border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              >
                <option value="all">All Regions</option>
                {uniqueRegions.map(region => (
                  <option key={region} value={region}>{region}</option>
                ))}
              </select>
            </div>

            <div>
              <label className="block text-xs font-medium text-gray-700 mb-1">Risk Level</label>
              <select
                value={filter.risk}
                onChange={(e) => setFilter({ ...filter, risk: e.target.value })}
                className="px-3 py-1.5 text-sm border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              >
                <option value="all">All Levels</option>
                <option value="High">High Risk</option>
                <option value="Medium">Medium Risk</option>
                <option value="Low">Low Risk</option>
              </select>
            </div>

            <button
              onClick={() => setFilter({ region: 'all', risk: 'all' })}
              className="mt-5 text-sm text-blue-600 hover:text-blue-700"
            >
              Clear Filters
            </button>
          </div>
        )}
      </div>

      {/* Table */}
      <div className="overflow-x-auto">
        {loading ? (
          <div className="flex items-center justify-center py-12">
            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
            <span className="ml-3 text-gray-600">Loading reports...</span>
          </div>
        ) : filteredReports.length === 0 ? (
          <div className="text-center py-12">
            <Calendar className="h-12 w-12 text-gray-400 mx-auto mb-3" />
            <p className="text-gray-600">No reports found for the selected filters</p>
            <p className="text-sm text-gray-500 mt-1">Try adjusting your filters or check back later</p>
          </div>
        ) : (
          <table className="w-full">
            <thead className="bg-gray-50 border-b">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  ID
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Region
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Timestamp
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Symptoms
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Disease
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Risk
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Score
                </th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {filteredReports.map((report) => (
                <tr
                  key={report.id}
                  onClick={() => onReportClick?.(report)}
                  className="hover:bg-gray-50 cursor-pointer transition-colors"
                >
                  <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                    #{report.id}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <div className="flex items-center space-x-1 text-sm text-gray-900">
                      <MapPin className="h-3 w-3 text-gray-400" />
                      <span>{report.region}</span>
                    </div>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                    {formatDate(report.timestamp)}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800">
                      {countSymptoms(report.symptoms)} symptoms
                    </span>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                    {report.predicted_disease.replace(/_/g, ' ')}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <span className={`inline-flex items-center space-x-1 px-2.5 py-0.5 rounded-full text-xs font-medium border ${getRiskBadgeColor(report.risk_level)}`}>
                      {getRiskIcon(report.risk_level)}
                      <span>{report.risk_level}</span>
                    </span>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                    {report.risk_score.toFixed(1)}%
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>

      {/* Footer with stats */}
      {!loading && filteredReports.length > 0 && (
        <div className="px-6 py-4 bg-gray-50 border-t">
          <div className="flex items-center justify-between text-sm">
            <div className="text-gray-600">
              Showing <span className="font-medium text-gray-900">{filteredReports.length}</span> of{' '}
              <span className="font-medium text-gray-900">
                {reports.filter(report => {
                  if (filter.region !== 'all' && report.region !== filter.region) return false;
                  if (filter.risk !== 'all' && report.risk_level !== filter.risk) return false;
                  return true;
                }).length}
              </span> reports
              {filter.region !== 'all' || filter.risk !== 'all' ? (
                <span className="ml-1">(filtered)</span>
              ) : null}
            </div>
            <div className="flex items-center space-x-4 text-xs">
              <div className="flex items-center space-x-1">
                <span className="h-2 w-2 bg-red-500 rounded-full"></span>
                <span className="text-gray-600">
                  {filteredReports.filter(r => r.risk_level === 'High').length} High Risk
                </span>
              </div>
              <div className="flex items-center space-x-1">
                <span className="h-2 w-2 bg-yellow-500 rounded-full"></span>
                <span className="text-gray-600">
                  {filteredReports.filter(r => r.risk_level === 'Medium').length} Medium Risk
                </span>
              </div>
              <div className="flex items-center space-x-1">
                <span className="h-2 w-2 bg-green-500 rounded-full"></span>
                <span className="text-gray-600">
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