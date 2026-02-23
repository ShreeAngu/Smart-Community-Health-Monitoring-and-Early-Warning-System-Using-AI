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
 fecal_coliform_per_00ml: number;
 total_coliform_per_00ml: number;
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
 population_density: 000,

 // Personal
 age: 0,
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
 water_quality_index: 0,
 ph: .0,
 turbidity_ntu: .0,
 dissolved_oxygen_mg_l: .0,
 bod_mg_l: .0,
 fecal_coliform_per_00ml: 0,
 total_coliform_per_00ml: 0,
 tds_mg_l: 00,
 nitrate_mg_l: .0,
 fluoride_mg_l: 0.,
 arsenic_ug_l: .0,
 },

 // Sanitation
 toilet_access: ,
 handwashing_practice: 'Sometimes',
 open_defecation_rate: 0.,
 sewage_treatment_pct: 0,

 // Environment
 month: new Date().getMonth() + ,
 season: 'Summer',
 avg_temperature_c: ,
 avg_rainfall_mm: 00,
 avg_humidity_pct: 0,
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
 month: new Date().getMonth() + ,
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
 <div className="min-h-screen bg-gray-0">
 {toast && (
 <Toast
 type={toast.type}
 message={toast.message}
 onClose={() => setToast(null)}
 />
 )}

 {/* Header */}
 <header className="bg-white shadow-sm border-b">
 <div className="max-w-xl mx-auto px- sm:px- lg:px-">
 <div className="flex justify-between items-center py-">
 <div className="flex items-center space-x-">
 <Droplets className="h- w- text-blue-00" />
 <div>
 <h className="text-xl font-bold text-gray-00">Community Health Dashboard</h>
 <p className="text-sm text-gray-00">Water-Borne Disease Prevention</p>
 </div>
 </div>
 <div className="flex items-center space-x-">
 <div className="flex items-center space-x- text-sm">
 <User className="h- w- text-gray-00" />
 <span className="text-gray-00">{user?.email}</span>
 <span className="px- py- bg-blue-00 text-blue-00 rounded-full text-xs font-medium">
 Community User
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
 <div className="grid grid-cols- lg:grid-cols- gap-">
 {/* Symptom Form */}
 <div className="bg-white rounded-lg shadow-sm border">
 <div className="p- border-b">
 <div className="flex items-center space-x-">
 <Heart className="h- w- text-red-00" />
 <h className="text-lg font-semibold text-gray-00">Report Symptoms</h>
 </div>
 <p className="text-sm text-gray-00 mt-">
 Help us track health patterns in your community
 </p>
 </div>

 <form onSubmit={handleSubmitReport} className="p- space-y-">
 {/* Location Info */}
 <div>
 <h className="text-sm font-semibold text-gray-00 mb- flex items-center">
 <MapPin className="h- w- mr- text-blue-00" />
 Location Information
 </h>
 <div className="grid grid-cols- sm:grid-cols- gap-">
 <div>
 <label className="block text-sm font-medium text-gray-00 mb-">
 Region <span className="text-red-00">*</span>
 </label>
 <select
 value={formData.region}
 onChange={(e) => handleInputChange('region', e.target.value)}
 className="w-full px- py- border border-gray-00 rounded-md focus:outline-none focus:ring- focus:ring-blue-00"
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
 <label className="block text-sm font-medium text-gray-00 mb-">
 District
 </label>
 <select
 value={formData.district}
 onChange={(e) => handleInputChange('district', e.target.value)}
 className="w-full px- py- border border-gray-00 rounded-md focus:outline-none focus:ring- focus:ring-blue-00"
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
 <label className="block text-sm font-medium text-gray-00 mb-">
 Area Type
 </label>
 <select
 value={formData.is_urban ? 'urban' : 'rural'}
 onChange={(e) => handleInputChange('is_urban', e.target.value === 'urban')}
 className="w-full px- py- border border-gray-00 rounded-md focus:outline-none focus:ring- focus:ring-blue-00"
 >
 <option value="urban">Urban</option>
 <option value="rural">Rural</option>
 </select>
 </div>
 <div>
 <label className="block text-sm font-medium text-gray-00 mb-">
 Population Density (per km²)
 </label>
 <input
 type="number"
 value={formData.population_density}
 onChange={(e) => handleInputChange('population_density', parseInt(e.target.value) || 000)}
 className="w-full px- py- border border-gray-00 rounded-md focus:outline-none focus:ring- focus:ring-blue-00"
 min="00"
 max="0000"
 />
 </div>
 </div>
 </div>

 {/* Personal Info */}
 <div>
 <h className="text-sm font-semibold text-gray-00 mb- flex items-center">
 <User className="h- w- mr- text-blue-00" />
 Personal Information
 </h>
 <div className="grid grid-cols- sm:grid-cols- gap-">
 <div>
 <label className="block text-sm font-medium text-gray-00 mb-">
 Age <span className="text-red-00">*</span>
 </label>
 <input
 type="number"
 value={formData.age}
 onChange={(e) => handleInputChange('age', parseInt(e.target.value) || 0)}
 className="w-full px- py- border border-gray-00 rounded-md focus:outline-none focus:ring- focus:ring-blue-00"
 min=""
 max="0"
 required
 />
 </div>
 <div>
 <label className="block text-sm font-medium text-gray-00 mb-">
 Gender <span className="text-red-00">*</span>
 </label>
 <select
 value={formData.gender}
 onChange={(e) => handleInputChange('gender', e.target.value)}
 className="w-full px- py- border border-gray-00 rounded-md focus:outline-none focus:ring- focus:ring-blue-00"
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
 <h className="text-sm font-semibold text-gray-00 mb- flex items-center">
 <Heart className="h- w- mr- text-red-00" />
 Current Symptoms <span className="text-red-00 ml-">* (Select at least one)</span>
 </h>
 <div className="grid grid-cols- gap-">
 {Object.entries(formData.symptoms).map(([symptom, checked]) => (
 <label key={symptom} className="flex items-center space-x- cursor-pointer p- rounded hover:bg-gray-0">
 <input
 type="checkbox"
 checked={checked}
 onChange={() => handleSymptomChange(symptom as keyof typeof formData.symptoms)}
 className="rounded border-gray-00 text-blue-00 focus:ring-blue-00"
 />
 <span className="text-sm text-gray-00 capitalize">
 {symptom.replace(/_/g, ' ')}
 </span>
 </label>
 ))}
 </div>
 </div>

 {/* Water Information */}
 <div>
 <h className="text-sm font-semibold text-gray-00 mb- flex items-center">
 <Droplets className="h- w- mr- text-blue-00" />
 Water Information
 </h>
 <div className="grid grid-cols- sm:grid-cols- gap-">
 <div>
 <label className="block text-xs text-gray-00 mb-">Water Source</label>
 <select
 value={formData.water_source}
 onChange={(e) => handleInputChange('water_source', e.target.value)}
 className="w-full px- py- text-sm border border-gray-00 rounded-md focus:outline-none focus:ring- focus:ring-blue-00"
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
 <label className="block text-xs text-gray-00 mb-">Water Treatment</label>
 <select
 value={formData.water_treatment}
 onChange={(e) => handleInputChange('water_treatment', e.target.value)}
 className="w-full px- py- text-sm border border-gray-00 rounded-md focus:outline-none focus:ring- focus:ring-blue-00"
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
 <label className="block text-xs text-gray-00 mb-">Water Quality Index (0-00)</label>
 <input
 type="number"
 value={formData.water_metrics.water_quality_index}
 onChange={(e) => handleInputChange('water_metrics.water_quality_index', parseFloat(e.target.value) || 0)}
 className="w-full px- py- text-sm border border-gray-00 rounded-md focus:outline-none focus:ring- focus:ring-blue-00"
 min="0"
 max="00"
 step="0."
 />
 </div>
 <div>
 <label className="block text-xs text-gray-00 mb-">pH Level</label>
 <input
 type="number"
 value={formData.water_metrics.ph}
 onChange={(e) => handleInputChange('water_metrics.ph', parseFloat(e.target.value) || .0)}
 className="w-full px- py- text-sm border border-gray-00 rounded-md focus:outline-none focus:ring- focus:ring-blue-00"
 min="0"
 max=""
 step="0."
 />
 </div>
 <div>
 <label className="block text-xs text-gray-00 mb-">Turbidity (NTU)</label>
 <input
 type="number"
 value={formData.water_metrics.turbidity_ntu}
 onChange={(e) => handleInputChange('water_metrics.turbidity_ntu', parseFloat(e.target.value) || .0)}
 className="w-full px- py- text-sm border border-gray-00 rounded-md focus:outline-none focus:ring- focus:ring-blue-00"
 min="0"
 step="0."
 />
 </div>
 <div>
 <label className="block text-xs text-gray-00 mb-">Fecal Coliform (per 00ml)</label>
 <input
 type="number"
 value={formData.water_metrics.fecal_coliform_per_00ml}
 onChange={(e) => handleInputChange('water_metrics.fecal_coliform_per_00ml', parseInt(e.target.value) || 0)}
 className="w-full px- py- text-sm border border-gray-00 rounded-md focus:outline-none focus:ring- focus:ring-blue-00"
 min="0"
 />
 </div>
 </div>
 </div>

 {/* Sanitation */}
 <div>
 <h className="text-sm font-semibold text-gray-00 mb- flex items-center">
 <Shield className="h- w- mr- text-green-00" />
 Sanitation & Hygiene
 </h>
 <div className="grid grid-cols- sm:grid-cols- gap-">
 <div>
 <label className="block text-xs text-gray-00 mb-">Toilet Access</label>
 <select
 value={formData.toilet_access}
 onChange={(e) => handleInputChange('toilet_access', parseInt(e.target.value))}
 className="w-full px- py- text-sm border border-gray-00 rounded-md focus:outline-none focus:ring- focus:ring-blue-00"
 >
 <option value="">Yes - Have Access</option>
 <option value="0">No - No Access</option>
 </select>
 </div>
 <div>
 <label className="block text-xs text-gray-00 mb-">Handwashing Practice</label>
 <select
 value={formData.handwashing_practice}
 onChange={(e) => handleInputChange('handwashing_practice', e.target.value)}
 className="w-full px- py- text-sm border border-gray-00 rounded-md focus:outline-none focus:ring- focus:ring-blue-00"
 >
 <option value="Always">Always</option>
 <option value="Sometimes">Sometimes</option>
 <option value="Rarely">Rarely</option>
 <option value="Never">Never</option>
 </select>
 </div>
 <div>
 <label className="block text-xs text-gray-00 mb-">Open Defecation Nearby (%)</label>
 <input
 type="number"
 value={formData.open_defecation_rate * 00}
 onChange={(e) => handleInputChange('open_defecation_rate', (parseFloat(e.target.value) || 0) / 00)}
 className="w-full px- py- text-sm border border-gray-00 rounded-md focus:outline-none focus:ring- focus:ring-blue-00"
 min="0"
 max="00"
 step=""
 />
 </div>
 <div>
 <label className="block text-xs text-gray-00 mb-">Sewage Treatment (%)</label>
 <input
 type="number"
 value={formData.sewage_treatment_pct}
 onChange={(e) => handleInputChange('sewage_treatment_pct', parseFloat(e.target.value) || 0)}
 className="w-full px- py- text-sm border border-gray-00 rounded-md focus:outline-none focus:ring- focus:ring-blue-00"
 min="0"
 max="00"
 step=""
 />
 </div>
 </div>
 </div>

 {/* Environment */}
 <div>
 <h className="text-sm font-semibold text-gray-00 mb- flex items-center">
 <Thermometer className="h- w- mr- text-orange-00" />
 Environmental Conditions
 </h>
 <div className="grid grid-cols- sm:grid-cols- gap-">
 <div>
 <label className="block text-xs text-gray-00 mb-">Season</label>
 <select
 value={formData.season}
 onChange={(e) => handleInputChange('season', e.target.value)}
 className="w-full px- py- text-sm border border-gray-00 rounded-md focus:outline-none focus:ring- focus:ring-blue-00"
 >
 <option value="Summer">Summer</option>
 <option value="Monsoon">Monsoon</option>
 <option value="Winter">Winter</option>
 <option value="Post-Monsoon">Post-Monsoon</option>
 </select>
 </div>
 <div>
 <label className="block text-xs text-gray-00 mb-">Flooding</label>
 <select
 value={formData.flooding ? 'yes' : 'no'}
 onChange={(e) => handleInputChange('flooding', e.target.value === 'yes')}
 className="w-full px- py- text-sm border border-gray-00 rounded-md focus:outline-none focus:ring- focus:ring-blue-00"
 >
 <option value="no">No Flooding</option>
 <option value="yes">Flooding Present</option>
 </select>
 </div>
 <div>
 <label className="block text-xs text-gray-00 mb-">Avg Temperature (°C)</label>
 <input
 type="number"
 value={formData.avg_temperature_c}
 onChange={(e) => handleInputChange('avg_temperature_c', parseFloat(e.target.value) || )}
 className="w-full px- py- text-sm border border-gray-00 rounded-md focus:outline-none focus:ring- focus:ring-blue-00"
 min="-0"
 max="0"
 step="0."
 />
 </div>
 <div>
 <label className="block text-xs text-gray-00 mb-">Avg Rainfall (mm)</label>
 <input
 type="number"
 value={formData.avg_rainfall_mm}
 onChange={(e) => handleInputChange('avg_rainfall_mm', parseFloat(e.target.value) || 00)}
 className="w-full px- py- text-sm border border-gray-00 rounded-md focus:outline-none focus:ring- focus:ring-blue-00"
 min="0"
 max="000"
 step=""
 />
 </div>
 </div>
 </div>

 {/* Submit Button */}
 <div className="flex items-center justify-between pt- border-t">
 <p className="text-xs text-gray-00">
 <span className="text-red-00">*</span> Required fields
 </p>
 <button
 type="submit"
 disabled={submitting}
 className="flex items-center space-x- bg-blue-00 text-white px- py- rounded-md hover:bg-blue-00 focus:outline-none focus:ring- focus:ring-blue-00 disabled:opacity-0 disabled:cursor-not-allowed transition-colors"
 >
 {submitting ? (
 <>
 <LoadingSpinner size="sm" />
 <span>Submitting...</span>
 </>
 ) : (
 <>
 <Send className="h- w-" />
 <span>Submit Report</span>
 </>
 )}
 </button>
 </div>
 </form>
 </div>

 {/* Education Module & Alerts */}
 <div className="space-y-">
 {/* Education Module */}
 <div className="bg-white rounded-lg shadow-sm border">
 <div className="p- border-b">
 <div className="flex items-center space-x-">
 <BookOpen className="h- w- text-green-00" />
 <h className="text-lg font-semibold text-gray-00">Health & Hygiene Tips</h>
 </div>
 </div>
 <div className="p-">
 <div className="space-y-">
 <div className="flex items-start space-x-">
 <Lightbulb className="h- w- text-yellow-00 mt-0." />
 <div>
 <h className="font-medium text-gray-00">Boil Your Water</h>
 <p className="text-sm text-gray-00">
 Boil water for at least minute to kill harmful bacteria and viruses.
 </p>
 </div>
 </div>
 <div className="flex items-start space-x-">
 <Lightbulb className="h- w- text-yellow-00 mt-0." />
 <div>
 <h className="font-medium text-gray-00">Wash Your Hands</h>
 <p className="text-sm text-gray-00">
 Wash hands with soap for 0 seconds, especially before eating and after using the toilet.
 </p>
 </div>
 </div>
 <div className="flex items-start space-x-">
 <Lightbulb className="h- w- text-yellow-00 mt-0." />
 <div>
 <h className="font-medium text-gray-00">Safe Food Practices</h>
 <p className="text-sm text-gray-00">
 Cook food thoroughly and avoid raw or undercooked foods, especially seafood.
 </p>
 </div>
 </div>
 <div className="flex items-start space-x-">
 <Lightbulb className="h- w- text-yellow-00 mt-0." />
 <div>
 <h className="font-medium text-gray-00">Proper Sanitation</h>
 <p className="text-sm text-gray-00">
 Use proper toilet facilities and ensure waste is disposed of safely.
 </p>
 </div>
 </div>
 </div>
 </div>
 </div>

 {/* Alerts Panel */}
 <div className="bg-white rounded-lg shadow-sm border">
 <div className="p- border-b">
 <div className="flex items-center justify-between">
 <div className="flex items-center space-x-">
 <Bell className="h- w- text-orange-00" />
 <h className="text-lg font-semibold text-gray-00">Recent Alerts</h>
 </div>
 <span className="bg-red-00 text-red-00 text-xs font-medium px- py- rounded-full">
 {alerts.filter(alert => !alert.is_read).length} New
 </span>
 </div>
 </div>
 <div className="max-h- overflow-y-auto">
 {alerts.length === 0 ? (
 <div className="p- text-center text-gray-00">
 <Shield className="h- w- text-gray-00 mx-auto mb-" />
 <p>No active alerts at this time.</p>
 <p className="text-sm">Your area is currently safe.</p>
 </div>
 ) : (
 <div className="divide-y divide-gray-00">
 {alerts.slice(0, ).map((alert) => (
 <div key={alert.id} className="p- hover:bg-gray-0 transition-colors">
 <div className="flex items-start space-x-">
 <div className={`flex-shrink-0 w- h- rounded-full mt- ${
 alert.alert_type === 'critical' ? 'bg-red-00' : 'bg-yellow-00'
 }`} />
 <div className="flex- min-w-0">
 <div className="flex items-center space-x-">
 <MapPin className="h- w- text-gray-00" />
 <p className="text-sm font-medium text-gray-00">{alert.region}</p>
 <span className={`px- py- text-xs font-medium rounded-full ${
 alert.alert_type === 'critical'
 ? 'bg-red-00 text-red-00'
 : 'bg-yellow-00 text-yellow-00'
 }`}>
 {alert.alert_type}
 </span>
 </div>
 <p className="text-sm text-gray-00 mt-">{alert.alert_message}</p>
 {alert.risk_index && (
 <p className="text-xs text-gray-00 mt-">
 Risk Index: {alert.risk_index}%
 </p>
 )}
 <p className="text-xs text-gray-00 mt-">
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