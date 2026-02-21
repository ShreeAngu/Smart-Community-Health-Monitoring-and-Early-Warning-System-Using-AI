import React, { useState, useEffect } from 'react';
import { useAuth } from '../context/AuthContext';
import { reportsAPI, alertsAPI } from '../services/api';
import LoadingSpinner from '../components/LoadingSpinner';
import Toast, { type ToastType } from '../components/Toast';
import PredictionResultModal from '../components/PredictionResultModal';
import { 
  Droplets, 
  LogOut,
  Bell,
  MapPin,
  Shield,
  Heart,
  Thermometer,
  User,
  Send,
  BookOpen,
  Lightbulb
} from 'lucide-react';

interface Alert {
  id: number;
  region: string;
  alert_message: string;
  alert_type: string;
  risk_index?: number;
  timestamp: string;
  is_read: boolean;
}



interface SymptomFormData {
  // Location
  region: string;
  district: string;
  latitude: number | null;
  longitude: number | null;
  is_urban: boolean;
  population_density: number;
  
  // Personal
  age: number;
  gender: string;
  
  // Symptoms
  symptoms: {
    diarrhea: boolean;
    vomiting: boolean;
    fever: boolean;
    abdominal_pain: boolean;
    dehydration: boolean;
    jaundice: boolean;
    bloody_stool: boolean;
    skin_rash: boolean;
  };
  
  // Water
  water_source: string;
  water_treatment: string;
  water_metrics: {
    water_quality_index: number;
    ph: number;
    turbidity_ntu: number;
    dissolved_oxygen_mg_l: number;
    bod_mg_l: number;
    fecal_coliform_per_100ml: number;
    total_coliform_per_100ml: number;
    tds_mg_l: number;
    nitrate_mg_l: number;
    fluoride_mg_l: number;
    arsenic_ug_l: number;
  };
  
  // Sanitation
  toilet_access: number;
  handwashing_practice: string;
  open_defecation_rate: number;
  sewage_treatment_pct: number;
  
  // Environment
  month: number;
  season: string;
  avg_temperature_c: number;
  avg_rainfall_mm: number;
  avg_humidity_pct: number;
  flooding: boolean;
}

const CommunityDashboard: React.FC = () => {
  const { user, logout } = useAuth();
  const [alerts, setAlerts] = useState<Alert[]>([]);
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [toast, setToast] = useState<{ type: ToastType; message: string } | null>(null);
  const [showPredictionModal, setShowPredictionModal] = useState(false);
  const [predictionResult, setPredictionResult] = useState<any>(null);
  
  // Form state
  const [formData, setFormData] = useState<SymptomFormData>({
    // Location
    region: '',
    district: '',
    latitude: null,
    longitude: null,
    is_urban: true,
    population_density: 1000,
    
    // Personal
    age: 30,
    gender: 'Male',
    
    // Symptoms
    symptoms: {
      diarrhea: false,
      vomiting: false,
      fever: false,
      abdominal_pain: false,
      dehydration: false,
      jaundice: false,
      bloody_stool: false,
      skin_rash: false,
    },
    
    // Water
    water_source: 'Tap',
    water_treatment: 'None',
    water_metrics: {
      water_quality_index: 50,
      ph: 7.0,
      turbidity_ntu: 5.0,
      dissolved_oxygen_mg_l: 8.0,
      bod_mg_l: 3.0,
      fecal_coliform_per_100ml: 0,
      total_coliform_per_100ml: 0,
      tds_mg_l: 300,
      nitrate_mg_l: 5.0,
      fluoride_mg_l: 0.5,
      arsenic_ug_l: 5.0,
    },
    
    // Sanitation
    toilet_access: 1,
    handwashing_practice: 'Sometimes',
    open_defecation_rate: 0.1,
    sewage_treatment_pct: 50,
    
    // Environment
    month: new Date().getMonth() + 1,
    season: 'Summer',
    avg_temperature_c: 25,
    avg_rainfall_mm: 100,
    avg_humidity_pct: 60,
    flooding: false,
  });

  useEffect(() => {
    fetchDashboardData();
  }, []);

  const fetchDashboardData = async () => {
    try {
      setLoading(true);
      
      // Fetch alerts
      const alertsResponse = await alertsAPI.getAlerts();
      setAlerts(alertsResponse.data || []);
      
    } catch (error) {
      console.error('Error fetching dashboard data:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleSymptomChange = (symptom: keyof typeof formData.symptoms) => {
    setFormData(prev => ({
      ...prev,
      symptoms: {
        ...prev.symptoms,
        [symptom]: !prev.symptoms[symptom]
      }
    }));
  };

  const handleInputChange = (field: string, value: any) => {
    if (field.includes('.')) {
      const [parent, child] = field.split('.');
      setFormData(prev => {
        const parentObj = prev[parent as keyof SymptomFormData];
        if (typeof parentObj === 'object' && parentObj !== null && !Array.isArray(parentObj)) {
          return {
            ...prev,
            [parent]: {
              ...(parentObj as Record<string, any>),
              [child]: value
            }
          };
        }
        return prev;
      });
    } else {
      setFormData(prev => {
        const updates: any = { [field]: value };
        
        // Auto-fill district when region is selected
        if (field === 'region') {
          if (value === 'Coimbatore North' || value === 'Coimbatore South') {
            updates.district = 'Coimbatore';
          } else if (value === 'Chennai') {
            updates.district = 'Chennai';
          } else if (value === 'Madurai') {
            updates.district = 'Madurai';
          } else if (value === 'Tiruchirappalli') {
            updates.district = 'Tiruchirappalli';
          } else if (value === 'Salem') {
            updates.district = 'Salem';
          } else if (value === 'Tirunelveli') {
            updates.district = 'Tirunelveli';
          } else if (value === 'Vellore') {
            updates.district = 'Vellore';
          } else if (value === 'Erode') {
            updates.district = 'Erode';
          } else if (value === 'Thanjavur') {
            updates.district = 'Thanjavur';
          } else if (value === 'Dindigul') {
            updates.district = 'Dindigul';
          }
        }
        
        return {
          ...prev,
          ...updates
        };
      });
    }
  };

  const handleSubmitReport = async (e: React.FormEvent) => {
    e.preventDefault();
    
    // Validation: At least one symptom must be selected
    const hasSymptoms = Object.values(formData.symptoms).some(symptom => symptom);
    if (!hasSymptoms) {
      setToast({ 
        type: 'error', 
        message: 'Please select at least one symptom before submitting.' 
      });
      return;
    }
    
    setSubmitting(true);

    try {
      const response = await reportsAPI.submitReport(formData);
      
      // Show success toast
      setToast({ 
        type: 'success', 
        message: 'Report submitted successfully! Thank you for helping your community.' 
      });
      
      // Show prediction modal if prediction data is available
      if (response.data.prediction && !response.data.prediction.error) {
        setPredictionResult(response.data.prediction);
        setShowPredictionModal(true);
      }
      
      // Reset form
      setFormData({
        // Location
        region: formData.region, // Keep region
        district: formData.district, // Keep district
        latitude: null,
        longitude: null,
        is_urban: formData.is_urban,
        population_density: formData.population_density,
        
        // Personal
        age: formData.age, // Keep age
        gender: formData.gender, // Keep gender
        
        // Symptoms - Reset
        symptoms: {
          diarrhea: false,
          vomiting: false,
          fever: false,
          abdominal_pain: false,
          dehydration: false,
          jaundice: false,
          bloody_stool: false,
          skin_rash: false,
        },
        
        // Water - Keep defaults
        water_source: formData.water_source,
        water_treatment: formData.water_treatment,
        water_metrics: formData.water_metrics,
        
        // Sanitation - Keep defaults
        toilet_access: formData.toilet_access,
        handwashing_practice: formData.handwashing_practice,
        open_defecation_rate: formData.open_defecation_rate,
        sewage_treatment_pct: formData.sewage_treatment_pct,
        
        // Environment - Keep defaults
        month: new Date().getMonth() + 1,
        season: formData.season,
        avg_temperature_c: formData.avg_temperature_c,
        avg_rainfall_mm: formData.avg_rainfall_mm,
        avg_humidity_pct: formData.avg_humidity_pct,
        flooding: formData.flooding,
      });
      
      // Refresh data
      fetchDashboardData();
      
    } catch (error: any) {
      setToast({ 
        type: 'error', 
        message: error.response?.data?.detail || 'Failed to submit report. Please try again.' 
      });
    } finally {
      setSubmitting(false);
    }
  };

  if (loading) {
    return <LoadingSpinner fullScreen text="Loading your dashboard..." />;
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {toast && (
        <Toast
          type={toast.type}
          message={toast.message}
          onClose={() => setToast(null)}
        />
      )}

      {/* Header */}
      <header className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center py-4">
            <div className="flex items-center space-x-3">
              <Droplets className="h-8 w-8 text-blue-600" />
              <div>
                <h1 className="text-xl font-bold text-gray-900">Community Health Dashboard</h1>
                <p className="text-sm text-gray-500">Water-Borne Disease Prevention</p>
              </div>
            </div>
            <div className="flex items-center space-x-4">
              <div className="flex items-center space-x-2 text-sm">
                <User className="h-4 w-4 text-gray-400" />
                <span className="text-gray-700">{user?.email}</span>
                <span className="px-2 py-1 bg-blue-100 text-blue-800 rounded-full text-xs font-medium">
                  Community User
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
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Symptom Form */}
          <div className="bg-white rounded-lg shadow-sm border">
            <div className="p-6 border-b">
              <div className="flex items-center space-x-2">
                <Heart className="h-5 w-5 text-red-500" />
                <h2 className="text-lg font-semibold text-gray-900">Report Symptoms</h2>
              </div>
              <p className="text-sm text-gray-600 mt-1">
                Help us track health patterns in your community
              </p>
            </div>
            
            <form onSubmit={handleSubmitReport} className="p-6 space-y-6">
              {/* Location Info */}
              <div>
                <h3 className="text-sm font-semibold text-gray-900 mb-3 flex items-center">
                  <MapPin className="h-4 w-4 mr-2 text-blue-600" />
                  Location Information
                </h3>
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Region <span className="text-red-500">*</span>
                    </label>
                    <select
                      value={formData.region}
                      onChange={(e) => handleInputChange('region', e.target.value)}
                      className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                      required
                    >
                      <option value="">Select Region</option>
                      <option value="Coimbatore North">Coimbatore North</option>
                      <option value="Coimbatore South">Coimbatore South</option>
                      <option value="Chennai">Chennai</option>
                      <option value="Madurai">Madurai</option>
                      <option value="Tiruchirappalli">Tiruchirappalli</option>
                      <option value="Salem">Salem</option>
                      <option value="Tirunelveli">Tirunelveli</option>
                      <option value="Vellore">Vellore</option>
                      <option value="Erode">Erode</option>
                      <option value="Thanjavur">Thanjavur</option>
                      <option value="Dindigul">Dindigul</option>
                      <option value="TestRegion">TestRegion</option>
                    </select>
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      District
                    </label>
                    <select
                      value={formData.district}
                      onChange={(e) => handleInputChange('district', e.target.value)}
                      className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                    >
                      <option value="">Select District</option>
                      <option value="Coimbatore">Coimbatore</option>
                      <option value="Chennai">Chennai</option>
                      <option value="Madurai">Madurai</option>
                      <option value="Tiruchirappalli">Tiruchirappalli</option>
                      <option value="Salem">Salem</option>
                      <option value="Tirunelveli">Tirunelveli</option>
                      <option value="Vellore">Vellore</option>
                      <option value="Erode">Erode</option>
                      <option value="Thanjavur">Thanjavur</option>
                      <option value="Dindigul">Dindigul</option>
                      <option value="Kanyakumari">Kanyakumari</option>
                      <option value="Cuddalore">Cuddalore</option>
                      <option value="Karur">Karur</option>
                      <option value="Nagapattinam">Nagapattinam</option>
                      <option value="Namakkal">Namakkal</option>
                      <option value="Perambalur">Perambalur</option>
                      <option value="Pudukkottai">Pudukkottai</option>
                      <option value="Ramanathapuram">Ramanathapuram</option>
                      <option value="Sivaganga">Sivaganga</option>
                      <option value="Tenkasi">Tenkasi</option>
                      <option value="Theni">Theni</option>
                      <option value="Thoothukudi">Thoothukudi</option>
                      <option value="Tiruvallur">Tiruvallur</option>
                      <option value="Tiruvannamalai">Tiruvannamalai</option>
                      <option value="Tiruvarur">Tiruvarur</option>
                      <option value="Villupuram">Villupuram</option>
                      <option value="Virudhunagar">Virudhunagar</option>
                    </select>
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Area Type
                    </label>
                    <select
                      value={formData.is_urban ? 'urban' : 'rural'}
                      onChange={(e) => handleInputChange('is_urban', e.target.value === 'urban')}
                      className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                    >
                      <option value="urban">Urban</option>
                      <option value="rural">Rural</option>
                    </select>
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Population Density (per km²)
                    </label>
                    <input
                      type="number"
                      value={formData.population_density}
                      onChange={(e) => handleInputChange('population_density', parseInt(e.target.value) || 1000)}
                      className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                      min="100"
                      max="50000"
                    />
                  </div>
                </div>
              </div>

              {/* Personal Info */}
              <div>
                <h3 className="text-sm font-semibold text-gray-900 mb-3 flex items-center">
                  <User className="h-4 w-4 mr-2 text-blue-600" />
                  Personal Information
                </h3>
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Age <span className="text-red-500">*</span>
                    </label>
                    <input
                      type="number"
                      value={formData.age}
                      onChange={(e) => handleInputChange('age', parseInt(e.target.value) || 30)}
                      className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                      min="1"
                      max="120"
                      required
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Gender <span className="text-red-500">*</span>
                    </label>
                    <select
                      value={formData.gender}
                      onChange={(e) => handleInputChange('gender', e.target.value)}
                      className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                      required
                    >
                      <option value="Male">Male</option>
                      <option value="Female">Female</option>
                      <option value="Other">Other</option>
                    </select>
                  </div>
                </div>
              </div>

              {/* Symptoms */}
              <div>
                <h3 className="text-sm font-semibold text-gray-900 mb-3 flex items-center">
                  <Heart className="h-4 w-4 mr-2 text-red-600" />
                  Current Symptoms <span className="text-red-500 ml-1">* (Select at least one)</span>
                </h3>
                <div className="grid grid-cols-2 gap-3">
                  {Object.entries(formData.symptoms).map(([symptom, checked]) => (
                    <label key={symptom} className="flex items-center space-x-2 cursor-pointer p-2 rounded hover:bg-gray-50">
                      <input
                        type="checkbox"
                        checked={checked}
                        onChange={() => handleSymptomChange(symptom as keyof typeof formData.symptoms)}
                        className="rounded border-gray-300 text-blue-600 focus:ring-blue-500"
                      />
                      <span className="text-sm text-gray-700 capitalize">
                        {symptom.replace(/_/g, ' ')}
                      </span>
                    </label>
                  ))}
                </div>
              </div>

              {/* Water Information */}
              <div>
                <h3 className="text-sm font-semibold text-gray-900 mb-3 flex items-center">
                  <Droplets className="h-4 w-4 mr-2 text-blue-600" />
                  Water Information
                </h3>
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                  <div>
                    <label className="block text-xs text-gray-600 mb-1">Water Source</label>
                    <select
                      value={formData.water_source}
                      onChange={(e) => handleInputChange('water_source', e.target.value)}
                      className="w-full px-3 py-2 text-sm border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                    >
                      <option value="Tap">Tap Water</option>
                      <option value="Well">Well Water</option>
                      <option value="Borehole">Borehole</option>
                      <option value="River">River/Stream</option>
                      <option value="Pond">Pond</option>
                      <option value="Rainwater">Rainwater</option>
                      <option value="Tanker">Tanker</option>
                      <option value="Piped">Piped Water</option>
                      <option value="Open Well">Open Well</option>
                    </select>
                  </div>
                  <div>
                    <label className="block text-xs text-gray-600 mb-1">Water Treatment</label>
                    <select
                      value={formData.water_treatment}
                      onChange={(e) => handleInputChange('water_treatment', e.target.value)}
                      className="w-full px-3 py-2 text-sm border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                    >
                      <option value="None">None</option>
                      <option value="Boiling">Boiling</option>
                      <option value="Chlorination">Chlorination</option>
                      <option value="Chlorinated">Chlorinated</option>
                      <option value="Filtration">Filtration</option>
                      <option value="Filtered">Filtered</option>
                      <option value="UV">UV Treatment</option>
                      <option value="Untreated">Untreated</option>
                    </select>
                  </div>
                  <div>
                    <label className="block text-xs text-gray-600 mb-1">Water Quality Index (0-100)</label>
                    <input
                      type="number"
                      value={formData.water_metrics.water_quality_index}
                      onChange={(e) => handleInputChange('water_metrics.water_quality_index', parseFloat(e.target.value) || 50)}
                      className="w-full px-3 py-2 text-sm border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                      min="0"
                      max="100"
                      step="0.1"
                    />
                  </div>
                  <div>
                    <label className="block text-xs text-gray-600 mb-1">pH Level</label>
                    <input
                      type="number"
                      value={formData.water_metrics.ph}
                      onChange={(e) => handleInputChange('water_metrics.ph', parseFloat(e.target.value) || 7.0)}
                      className="w-full px-3 py-2 text-sm border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                      min="0"
                      max="14"
                      step="0.1"
                    />
                  </div>
                  <div>
                    <label className="block text-xs text-gray-600 mb-1">Turbidity (NTU)</label>
                    <input
                      type="number"
                      value={formData.water_metrics.turbidity_ntu}
                      onChange={(e) => handleInputChange('water_metrics.turbidity_ntu', parseFloat(e.target.value) || 5.0)}
                      className="w-full px-3 py-2 text-sm border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                      min="0"
                      step="0.1"
                    />
                  </div>
                  <div>
                    <label className="block text-xs text-gray-600 mb-1">Fecal Coliform (per 100ml)</label>
                    <input
                      type="number"
                      value={formData.water_metrics.fecal_coliform_per_100ml}
                      onChange={(e) => handleInputChange('water_metrics.fecal_coliform_per_100ml', parseInt(e.target.value) || 0)}
                      className="w-full px-3 py-2 text-sm border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                      min="0"
                    />
                  </div>
                </div>
              </div>

              {/* Sanitation */}
              <div>
                <h3 className="text-sm font-semibold text-gray-900 mb-3 flex items-center">
                  <Shield className="h-4 w-4 mr-2 text-green-600" />
                  Sanitation & Hygiene
                </h3>
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                  <div>
                    <label className="block text-xs text-gray-600 mb-1">Toilet Access</label>
                    <select
                      value={formData.toilet_access}
                      onChange={(e) => handleInputChange('toilet_access', parseInt(e.target.value))}
                      className="w-full px-3 py-2 text-sm border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                    >
                      <option value="1">Yes - Have Access</option>
                      <option value="0">No - No Access</option>
                    </select>
                  </div>
                  <div>
                    <label className="block text-xs text-gray-600 mb-1">Handwashing Practice</label>
                    <select
                      value={formData.handwashing_practice}
                      onChange={(e) => handleInputChange('handwashing_practice', e.target.value)}
                      className="w-full px-3 py-2 text-sm border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                    >
                      <option value="Always">Always</option>
                      <option value="Sometimes">Sometimes</option>
                      <option value="Rarely">Rarely</option>
                      <option value="Never">Never</option>
                    </select>
                  </div>
                  <div>
                    <label className="block text-xs text-gray-600 mb-1">Open Defecation Nearby (%)</label>
                    <input
                      type="number"
                      value={formData.open_defecation_rate * 100}
                      onChange={(e) => handleInputChange('open_defecation_rate', (parseFloat(e.target.value) || 0) / 100)}
                      className="w-full px-3 py-2 text-sm border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                      min="0"
                      max="100"
                      step="1"
                    />
                  </div>
                  <div>
                    <label className="block text-xs text-gray-600 mb-1">Sewage Treatment (%)</label>
                    <input
                      type="number"
                      value={formData.sewage_treatment_pct}
                      onChange={(e) => handleInputChange('sewage_treatment_pct', parseFloat(e.target.value) || 50)}
                      className="w-full px-3 py-2 text-sm border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                      min="0"
                      max="100"
                      step="1"
                    />
                  </div>
                </div>
              </div>

              {/* Environment */}
              <div>
                <h3 className="text-sm font-semibold text-gray-900 mb-3 flex items-center">
                  <Thermometer className="h-4 w-4 mr-2 text-orange-600" />
                  Environmental Conditions
                </h3>
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                  <div>
                    <label className="block text-xs text-gray-600 mb-1">Season</label>
                    <select
                      value={formData.season}
                      onChange={(e) => handleInputChange('season', e.target.value)}
                      className="w-full px-3 py-2 text-sm border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                    >
                      <option value="Summer">Summer</option>
                      <option value="Monsoon">Monsoon</option>
                      <option value="Winter">Winter</option>
                      <option value="Post-Monsoon">Post-Monsoon</option>
                    </select>
                  </div>
                  <div>
                    <label className="block text-xs text-gray-600 mb-1">Flooding</label>
                    <select
                      value={formData.flooding ? 'yes' : 'no'}
                      onChange={(e) => handleInputChange('flooding', e.target.value === 'yes')}
                      className="w-full px-3 py-2 text-sm border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                    >
                      <option value="no">No Flooding</option>
                      <option value="yes">Flooding Present</option>
                    </select>
                  </div>
                  <div>
                    <label className="block text-xs text-gray-600 mb-1">Avg Temperature (°C)</label>
                    <input
                      type="number"
                      value={formData.avg_temperature_c}
                      onChange={(e) => handleInputChange('avg_temperature_c', parseFloat(e.target.value) || 25)}
                      className="w-full px-3 py-2 text-sm border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                      min="-10"
                      max="50"
                      step="0.1"
                    />
                  </div>
                  <div>
                    <label className="block text-xs text-gray-600 mb-1">Avg Rainfall (mm)</label>
                    <input
                      type="number"
                      value={formData.avg_rainfall_mm}
                      onChange={(e) => handleInputChange('avg_rainfall_mm', parseFloat(e.target.value) || 100)}
                      className="w-full px-3 py-2 text-sm border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                      min="0"
                      max="1000"
                      step="1"
                    />
                  </div>
                </div>
              </div>

              {/* Submit Button */}
              <div className="flex items-center justify-between pt-4 border-t">
                <p className="text-xs text-gray-500">
                  <span className="text-red-500">*</span> Required fields
                </p>
                <button
                  type="submit"
                  disabled={submitting}
                  className="flex items-center space-x-2 bg-blue-600 text-white px-6 py-2 rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
                >
                  {submitting ? (
                    <>
                      <LoadingSpinner size="sm" />
                      <span>Submitting...</span>
                    </>
                  ) : (
                    <>
                      <Send className="h-4 w-4" />
                      <span>Submit Report</span>
                    </>
                  )}
                </button>
              </div>
            </form>
          </div>

          {/* Education Module & Alerts */}
          <div className="space-y-6">
            {/* Education Module */}
            <div className="bg-white rounded-lg shadow-sm border">
              <div className="p-6 border-b">
                <div className="flex items-center space-x-2">
                  <BookOpen className="h-5 w-5 text-green-500" />
                  <h2 className="text-lg font-semibold text-gray-900">Health & Hygiene Tips</h2>
                </div>
              </div>
              <div className="p-6">
                <div className="space-y-4">
                  <div className="flex items-start space-x-3">
                    <Lightbulb className="h-5 w-5 text-yellow-500 mt-0.5" />
                    <div>
                      <h3 className="font-medium text-gray-900">Boil Your Water</h3>
                      <p className="text-sm text-gray-600">
                        Boil water for at least 1 minute to kill harmful bacteria and viruses.
                      </p>
                    </div>
                  </div>
                  <div className="flex items-start space-x-3">
                    <Lightbulb className="h-5 w-5 text-yellow-500 mt-0.5" />
                    <div>
                      <h3 className="font-medium text-gray-900">Wash Your Hands</h3>
                      <p className="text-sm text-gray-600">
                        Wash hands with soap for 20 seconds, especially before eating and after using the toilet.
                      </p>
                    </div>
                  </div>
                  <div className="flex items-start space-x-3">
                    <Lightbulb className="h-5 w-5 text-yellow-500 mt-0.5" />
                    <div>
                      <h3 className="font-medium text-gray-900">Safe Food Practices</h3>
                      <p className="text-sm text-gray-600">
                        Cook food thoroughly and avoid raw or undercooked foods, especially seafood.
                      </p>
                    </div>
                  </div>
                  <div className="flex items-start space-x-3">
                    <Lightbulb className="h-5 w-5 text-yellow-500 mt-0.5" />
                    <div>
                      <h3 className="font-medium text-gray-900">Proper Sanitation</h3>
                      <p className="text-sm text-gray-600">
                        Use proper toilet facilities and ensure waste is disposed of safely.
                      </p>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            {/* Alerts Panel */}
            <div className="bg-white rounded-lg shadow-sm border">
              <div className="p-6 border-b">
                <div className="flex items-center justify-between">
                  <div className="flex items-center space-x-2">
                    <Bell className="h-5 w-5 text-orange-500" />
                    <h2 className="text-lg font-semibold text-gray-900">Recent Alerts</h2>
                  </div>
                  <span className="bg-red-100 text-red-800 text-xs font-medium px-2 py-1 rounded-full">
                    {alerts.filter(alert => !alert.is_read).length} New
                  </span>
                </div>
              </div>
              <div className="max-h-96 overflow-y-auto">
                {alerts.length === 0 ? (
                  <div className="p-6 text-center text-gray-500">
                    <Shield className="h-12 w-12 text-gray-300 mx-auto mb-3" />
                    <p>No active alerts at this time.</p>
                    <p className="text-sm">Your area is currently safe.</p>
                  </div>
                ) : (
                  <div className="divide-y divide-gray-200">
                    {alerts.slice(0, 5).map((alert) => (
                      <div key={alert.id} className="p-4 hover:bg-gray-50 transition-colors">
                        <div className="flex items-start space-x-3">
                          <div className={`flex-shrink-0 w-2 h-2 rounded-full mt-2 ${
                            alert.alert_type === 'critical' ? 'bg-red-500' : 'bg-yellow-500'
                          }`} />
                          <div className="flex-1 min-w-0">
                            <div className="flex items-center space-x-2">
                              <MapPin className="h-4 w-4 text-gray-400" />
                              <p className="text-sm font-medium text-gray-900">{alert.region}</p>
                              <span className={`px-2 py-1 text-xs font-medium rounded-full ${
                                alert.alert_type === 'critical' 
                                  ? 'bg-red-100 text-red-800' 
                                  : 'bg-yellow-100 text-yellow-800'
                              }`}>
                                {alert.alert_type}
                              </span>
                            </div>
                            <p className="text-sm text-gray-700 mt-1">{alert.alert_message}</p>
                            {alert.risk_index && (
                              <p className="text-xs text-gray-500 mt-1">
                                Risk Index: {alert.risk_index}%
                              </p>
                            )}
                            <p className="text-xs text-gray-500 mt-1">
                              {new Date(alert.timestamp).toLocaleString()}
                            </p>
                          </div>
                        </div>
                      </div>
                    ))}
                  </div>
                )}
              </div>
            </div>
          </div>
        </div>
      </div>
      
      {/* Prediction Result Modal */}
      {predictionResult && (
        <PredictionResultModal
          isOpen={showPredictionModal}
          onClose={() => setShowPredictionModal(false)}
          prediction={predictionResult}
        />
      )}
    </div>
  );
};

export default CommunityDashboard;