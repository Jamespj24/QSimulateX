import React from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, Cell } from 'recharts';

const ProbabilityHistogram = ({ measurements, probabilities }) => {
  if (!measurements || Object.keys(measurements).length === 0) {
    return (
      <div className="bg-gray-900 rounded-lg p-6 shadow-xl">
        <h2 className="text-2xl font-bold text-white mb-4">Measurement Results</h2>
        <p className="text-gray-400">Run a simulation to see measurement results</p>
      </div>
    );
  }

  // Calculate total shots
  const totalShots = Object.values(measurements).reduce((sum, count) => sum + count, 0);

  // Prepare data for chart
  const chartData = Object.entries(measurements)
    .map(([state, count]) => ({
      state: `|${state}⟩`,
      count: count,
      probability: count / totalShots,
      theoreticalProb: probabilities ? probabilities[parseInt(state, 2)] : null,
    }))
    .sort((a, b) => b.count - a.count);

  const CustomTooltip = ({ active, payload }) => {
    if (active && payload && payload.length) {
      const data = payload[0].payload;
      return (
        <div className="bg-gray-800 p-3 rounded-lg border border-gray-700">
          <p className="text-white font-semibold mb-2">{data.state}</p>
          <p className="text-blue-400">Measured: {data.count} times</p>
          <p className="text-green-400">Probability: {(data.probability * 100).toFixed(2)}%</p>
          {data.theoreticalProb !== null && (
            <p className="text-purple-400">
              Theoretical: {(data.theoreticalProb * 100).toFixed(2)}%
            </p>
          )}
        </div>
      );
    }
    return null;
  };

  // Color palette
  const COLORS = ['#8b5cf6', '#ec4899', '#0066ff', '#10b981', '#f59e0b', '#ef4444', '#06b6d4', '#84cc16'];

  return (
    <div className="bg-gray-900 rounded-lg p-6 shadow-xl">
      <div className="flex justify-between items-center mb-4">
        <h2 className="text-2xl font-bold text-white">Measurement Results</h2>
        <div className="text-sm text-gray-400">
          Total shots: <span className="text-white font-semibold">{totalShots}</span>
        </div>
      </div>

      <ResponsiveContainer width="100%" height={300}>
        <BarChart data={chartData}>
          <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
          <XAxis 
            dataKey="state" 
            stroke="#9ca3af"
            tick={{ fill: '#9ca3af', fontSize: 12 }}
          />
          <YAxis 
            stroke="#9ca3af"
            tick={{ fill: '#9ca3af', fontSize: 12 }}
            label={{ value: 'Count', angle: -90, position: 'insideLeft', fill: '#9ca3af' }}
          />
          <Tooltip content={<CustomTooltip />} />
          <Legend wrapperStyle={{ color: '#9ca3af' }} />
          <Bar dataKey="count" name="Measurement Count">
            {chartData.map((entry, index) => (
              <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
            ))}
          </Bar>
        </BarChart>
      </ResponsiveContainer>

      {/* Statistics */}
      <div className="mt-6 grid grid-cols-2 md:grid-cols-3 gap-4">
        {chartData.slice(0, 6).map((data, idx) => (
          <div 
            key={idx} 
            className="bg-gray-800 p-4 rounded-lg border-l-4"
            style={{ borderColor: COLORS[idx % COLORS.length] }}
          >
            <p className="text-white font-mono text-lg font-bold mb-1">{data.state}</p>
            <div className="space-y-1">
              <p className="text-sm text-gray-400">
                Count: <span className="text-white">{data.count}</span>
              </p>
              <p className="text-sm text-gray-400">
                Measured: <span className="text-green-400">{(data.probability * 100).toFixed(2)}%</span>
              </p>
              {data.theoreticalProb !== null && (
                <p className="text-sm text-gray-400">
                  Expected: <span className="text-purple-400">{(data.theoreticalProb * 100).toFixed(2)}%</span>
                </p>
              )}
            </div>
          </div>
        ))}
      </div>

      {/* Shannon Entropy */}
      {probabilities && (
        <div className="mt-6 bg-gray-800 p-4 rounded-lg">
          <h3 className="text-lg font-semibold text-white mb-2">Quantum Information</h3>
          <div className="grid grid-cols-2 gap-4">
            <div>
              <p className="text-sm text-gray-400">Distinct States</p>
              <p className="text-2xl font-bold text-white">{chartData.length}</p>
            </div>
            <div>
              <p className="text-sm text-gray-400">Most Probable</p>
              <p className="text-2xl font-bold text-quantum-purple">{chartData[0].state}</p>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default ProbabilityHistogram;
