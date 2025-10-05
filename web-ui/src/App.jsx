import React, { useState } from 'react';
import { Cpu, Zap, Info } from 'lucide-react';
import CircuitBuilder from './components/CircuitBuilder';
import StateVectorView from './components/StateVectorView';
import ProbabilityHistogram from './components/ProbabilityHistogram';
import BlochSphere from './components/BlochSphere';
import { runCircuit } from './api';

function App() {
  const [nQubits, setNQubits] = useState(2);
  const [gates, setGates] = useState([]);
  const [simulationResult, setSimulationResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [shots, setShots] = useState(1000);

  const handleRunSimulation = async () => {
    setLoading(true);
    setError(null);

    try {
      const circuitData = {
        n_qubits: nQubits,
        gates: gates,
        shots: shots,
        optimize: true,
      };

      const result = await runCircuit(circuitData);
      setSimulationResult(result);
    } catch (err) {
      setError(err.response?.data?.detail || err.message || 'Simulation failed');
      console.error('Simulation error:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleQubitChange = (value) => {
    const newQubits = parseInt(value);
    if (newQubits > 0 && newQubits <= 10) {
      setNQubits(newQubits);
      setGates([]); // Clear gates when changing qubit count
      setSimulationResult(null);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-950 via-gray-900 to-purple-950">
      {/* Header */}
      <header className="bg-gray-900 bg-opacity-80 backdrop-blur-sm border-b border-gray-800 sticky top-0 z-10">
        <div className="container mx-auto px-6 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="bg-gradient-to-br from-quantum-purple to-quantum-pink p-2 rounded-lg">
                <Cpu size={32} className="text-white" />
              </div>
              <div>
                <h1 className="text-3xl font-bold text-white">QSimulateX</h1>
                <p className="text-sm text-gray-400">Intelligent Quantum Computing Simulator</p>
              </div>
            </div>

            <div className="flex items-center gap-4">
              <div className="bg-gray-800 px-4 py-2 rounded-lg flex items-center gap-2">
                <Zap size={16} className="text-quantum-purple" />
                <span className="text-white text-sm">
                  {loading ? 'Simulating...' : 'Ready'}
                </span>
              </div>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="container mx-auto px-6 py-8">
        {/* Control Panel */}
        <div className="bg-gray-900 rounded-lg p-6 shadow-xl mb-8">
          <h2 className="text-xl font-bold text-white mb-4">Circuit Configuration</h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div>
              <label className="block text-sm font-medium text-gray-400 mb-2">
                Number of Qubits
              </label>
              <input
                type="number"
                min="1"
                max="10"
                value={nQubits}
                onChange={(e) => handleQubitChange(e.target.value)}
                className="w-full px-4 py-2 bg-gray-800 text-white rounded-lg focus:outline-none focus:ring-2 focus:ring-quantum-purple"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-400 mb-2">
                Number of Shots
              </label>
              <input
                type="number"
                min="100"
                max="10000"
                step="100"
                value={shots}
                onChange={(e) => setShots(parseInt(e.target.value))}
                className="w-full px-4 py-2 bg-gray-800 text-white rounded-lg focus:outline-none focus:ring-2 focus:ring-quantum-purple"
              />
            </div>

            <div className="flex items-end">
              <div className="bg-gray-800 p-4 rounded-lg w-full">
                <div className="flex items-center gap-2 text-gray-400">
                  <Info size={16} />
                  <span className="text-sm">
                    Gates: {gates.length} | Qubits: {nQubits}
                  </span>
                </div>
              </div>
            </div>
          </div>

          {error && (
            <div className="mt-4 bg-red-900 bg-opacity-20 border border-red-500 text-red-300 px-4 py-3 rounded-lg">
              <strong className="font-bold">Error: </strong>
              <span>{error}</span>
            </div>
          )}
        </div>

        {/* Circuit Builder */}
        <div className="mb-8">
          <CircuitBuilder
            nQubits={nQubits}
            gates={gates}
            setGates={setGates}
            onRun={handleRunSimulation}
          />
        </div>

        {/* Results */}
        {loading && (
          <div className="bg-gray-900 rounded-lg p-12 shadow-xl text-center">
            <div className="inline-block animate-spin rounded-full h-16 w-16 border-t-4 border-b-4 border-quantum-purple mb-4"></div>
            <p className="text-white text-lg">Running quantum simulation...</p>
          </div>
        )}

        {simulationResult && !loading && (
          <div className="space-y-8">
            {/* Circuit Info */}
            <div className="bg-gray-900 rounded-lg p-6 shadow-xl">
              <h2 className="text-2xl font-bold text-white mb-4">Circuit Information</h2>
              <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                <div className="bg-gray-800 p-4 rounded-lg">
                  <p className="text-sm text-gray-400">Total Gates</p>
                  <p className="text-2xl font-bold text-white">
                    {simulationResult.circuit_info.n_gates}
                  </p>
                </div>
                <div className="bg-gray-800 p-4 rounded-lg">
                  <p className="text-sm text-gray-400">Circuit Depth</p>
                  <p className="text-2xl font-bold text-quantum-purple">
                    {simulationResult.circuit_info.depth}
                  </p>
                </div>
                <div className="bg-gray-800 p-4 rounded-lg">
                  <p className="text-sm text-gray-400">Qubits</p>
                  <p className="text-2xl font-bold text-quantum-blue">
                    {simulationResult.circuit_info.n_qubits}
                  </p>
                </div>
                <div className="bg-gray-800 p-4 rounded-lg">
                  <p className="text-sm text-gray-400">Mode</p>
                  <p className="text-sm font-semibold text-green-400">
                    {simulationResult.circuit_info.use_sparse ? 'Sparse' : 'Dense'}
                  </p>
                </div>
              </div>
            </div>

            {/* Visualizations Grid */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
              <StateVectorView stateVector={simulationResult.state_vector} />
              <ProbabilityHistogram
                measurements={simulationResult.measurements}
                probabilities={simulationResult.probabilities}
              />
            </div>

            {/* Bloch Sphere (only for single qubit) */}
            {nQubits === 1 && (
              <BlochSphere stateVector={simulationResult.state_vector} />
            )}
          </div>
        )}

        {/* Getting Started Info */}
        {gates.length === 0 && !simulationResult && (
          <div className="bg-gradient-to-br from-purple-900 to-blue-900 bg-opacity-20 rounded-lg p-8 shadow-xl border border-purple-700 border-opacity-30">
            <h2 className="text-2xl font-bold text-white mb-4 flex items-center gap-2">
              <Info size={24} />
              Getting Started
            </h2>
            <div className="space-y-3 text-gray-300">
              <p>👋 Welcome to QSimulateX! Here's how to create your first quantum circuit:</p>
              <ol className="list-decimal list-inside space-y-2 ml-4">
                <li>Choose the number of qubits for your circuit (1-10)</li>
                <li>Drag gates from the palette and drop them onto qubit wires</li>
                <li>For rotation gates (RX, RY, RZ), you'll be prompted to enter an angle</li>
                <li>Click "Run Simulation" to execute your circuit</li>
                <li>Explore the state vector, probabilities, and measurement results!</li>
              </ol>
              <div className="mt-6 bg-gray-900 bg-opacity-50 p-4 rounded-lg">
                <p className="font-semibold text-quantum-purple mb-2">Quick Examples:</p>
                <ul className="list-disc list-inside space-y-1 text-sm">
                  <li>Create a superposition: Apply H gate to qubit 0</li>
                  <li>Bell State: H on qubit 0, then CNOT with control=0, target=1</li>
                  <li>Rotation: Apply RX, RY, or RZ with angle π/2 (≈1.5708)</li>
                </ul>
              </div>
            </div>
          </div>
        )}
      </main>

      {/* Footer */}
      <footer className="bg-gray-900 border-t border-gray-800 mt-12">
        <div className="container mx-auto px-6 py-6 text-center text-gray-400">
          <p>QSimulateX - Intelligent Quantum Computing Simulator</p>
          <p className="text-sm mt-2">Built with React, FastAPI, and NumPy</p>
        </div>
      </footer>
    </div>
  );
}

export default App;
