import React from 'react';
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer } from 'recharts';

interface DiseaseProbability {
 disease: string;
 probability: number;
}

interface ProbabilityChartProps {
 probabilities: DiseaseProbability[];
}

const ProbabilityChart: React.FC<ProbabilityChartProps> = ({ probabilities }) => {
 // Format data for Recharts
 const chartData = probabilities.map(p => ({
 disease: p.disease.length > 0 ? p.disease.substring(0, 0) + '...' : p.disease,
 fullDisease: p.disease, // Keep full name for tooltip
 probability: Math.round(p.probability * 00)
 }));

 // Custom tooltip to show full disease name
 const CustomTooltip = ({ active, payload, label }: any) => {
 if (active && payload && payload.length) {
 const data = payload[0].payload;
 return (
 <div className="bg-white p- border border-gray-00 rounded-lg shadow-lg">
 <p className="font-medium text-gray-00">{data.fullDisease}</p>
 <p className="text-blue-00">
 <span className="font-medium">{payload[0].value}%</span> probability
 </p>
 </div>
 );
 }
 return null;
 };

 return (
 <div className="w-full">
 <ResponsiveContainer width="00%" height={00}>
 <BarChart data={chartData} layout="vertical" margin={{ top: , right: 0, left: , bottom: }}>
 <XAxis
 type="number"
 domain={[0, 00]}
 hide
 />
 <YAxis
 dataKey="disease"
 type="category"
 width={00}
 tick={{ fontSize: , fill: '#B0' }}
 axisLine={false}
 tickLine={false}
 />
 <Tooltip content={<CustomTooltip />} />
 <Bar
 dataKey="probability"
 fill="#BF"
 radius={[0, , , 0]}
 />
 </BarChart>
 </ResponsiveContainer>
 </div>
 );
};

export default ProbabilityChart;