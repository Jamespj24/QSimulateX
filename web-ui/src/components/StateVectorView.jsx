import React from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

const StateVectorView = ({ stateVector }) => {
  if (!stateVector || stateVector.length === 0) {
    return (
      <div className="bg-gray-900 rounded-lg p-6 shadow-xl">
        <h2 className="text-2xl font-bold text-white mb-4">State Vector</h2>
        <p className="text-gray-400">Run a simulation to see the state vector</p>
      </div>
    );
  }

  // Prepare data for visualization
  const chartData = stateVector.map((amplitude, index) => {
    const magnitude = Math.sqrt(amplitude.real ** 2 + amplitude.imag ** 2);
    const phase = Math.atan2(amplitude.imag, amplitude.real);
    const nQubits = Math.log2(stateVector.length);
    const binaryLabel = index.toString(2).padStart(nQubits, '0');

    return {
      state: `|${binaryLabel}⟩`,
      magnitude: magnitude,
      real: amplitude.real,
      imag: amplitude.imag,
      phase: phase,
    };
  });

  const CustomTooltip = ({ active, payload }) => {
    if (active && payload && payload.length) {
      const data = payload[0].payload;
      return (
        <div className="bg-gray-800 p-3 rounded-lg border border-gray-700">
          <p className="text-white font-semibold">{data.state}</p>
          <p className="text-blue-400">Magnitude: {data.magnitude.toFixed(4)}</p>
          <p className="text-green-400">Real: {data.real.toFixed(4)}</p>
          <p className="text-red-400">Imag: {data.imag.toFixed(4)}</p>
          <p className="text-purple-400">Phase: {data.phase.toFixed(4)} rad</p>
        </div>
      );
    }
    return null;
  };

  return (
    <div className="bg-gray-900 rounded-lg p-6 shadow-xl">
      <h2 className="text-2xl font-bold text-white mb-4">State Vector Amplitudes</h2>
      
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
            label={{ value: 'Amplitude', angle: -90, position: 'insideLeft', fill: '#9ca3af' }}
          />
          <Tooltip content={<CustomTooltip />} />
          <Legend wrapperStyle={{ color: '#9ca3af' }} />
          <Bar dataKey="magnitude" fill="#8b5cf6" name="Magnitude" />
        </BarChart>
      </ResponsiveContainer>

      <div className="mt-6 grid grid-cols-2 md:grid-cols-4 gap-4">
        {chartData.map((data, idx) => (
          <div key={idx} className="bg-gray-800 p-3 rounded-lg">
            <p className="text-white font-mono text-sm mb-1">{data.state}</p>
            <div className="text-xs text-gray-400">
              <p>|α| = {data.magnitude.toFixed(3)}</p>
              <p className="text-green-400">Re = {data.real.toFixed(3)}</p>
              <p className="text-red-400">Im = {data.imag.toFixed(3)}</p>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default StateVectorView;
