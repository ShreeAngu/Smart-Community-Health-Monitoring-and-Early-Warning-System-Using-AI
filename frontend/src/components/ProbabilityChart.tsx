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
    disease: p.disease.length > 10 ? p.disease.substring(0, 10) + '...' : p.disease,
    fullDisease: p.disease, // Keep full name for tooltip
    probability: Math.round(p.probability * 100)
  }));

  // Custom tooltip to show full disease name
  const CustomTooltip = ({ active, payload, label }: any) => {
    if (active && payload && payload.length) {
      const data = payload[0].payload;
      return (
        <div className="bg-white p-3 border border-gray-200 rounded-lg shadow-lg">
          <p className="font-medium text-gray-900">{data.fullDisease}</p>
          <p className="text-blue-600">
            <span className="font-medium">{payload[0].value}%</span> probability
          </p>
        </div>
      );
    }
    return null;
  };

  return (
    <div className="w-full">
      <ResponsiveContainer width="100%" height={200}>
        <BarChart data={chartData} layout="vertical" margin={{ top: 5, right: 30, left: 5, bottom: 5 }}>
          <XAxis 
            type="number" 
            domain={[0, 100]} 
            hide 
          />
          <YAxis 
            dataKey="disease" 
            type="category" 
            width={100} 
            tick={{ fontSize: 11, fill: '#6B7280' }}
            axisLine={false}
            tickLine={false}
          />
          <Tooltip content={<CustomTooltip />} />
          <Bar 
            dataKey="probability" 
            fill="#3B82F6"
            radius={[0, 4, 4, 0]}
          />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
};

export default ProbabilityChart;