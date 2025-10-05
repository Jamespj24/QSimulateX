import React, { useState, useRef } from 'react';
import { Plus, Trash2, Play, Download, Upload } from 'lucide-react';

const AVAILABLE_GATES = {
  'Single Qubit': ['H', 'X', 'Y', 'Z', 'T', 'S'],
  'Rotations': ['RX', 'RY', 'RZ'],
  'Two Qubit': ['CNOT', 'CZ', 'SWAP'],
};

const GATE_COLORS = {
  H: 'bg-blue-500',
  X: 'bg-red-500',
  Y: 'bg-green-500',
  Z: 'bg-purple-500',
  T: 'bg-pink-500',
  S: 'bg-indigo-500',
  RX: 'bg-orange-500',
  RY: 'bg-yellow-500',
  RZ: 'bg-teal-500',
  CNOT: 'bg-cyan-500',
  CZ: 'bg-violet-500',
  SWAP: 'bg-fuchsia-500',
};

const CircuitBuilder = ({ nQubits, gates, setGates, onRun }) => {
  const [selectedGate, setSelectedGate] = useState(null);
  const [draggedGate, setDraggedGate] = useState(null);
  const [showParamModal, setShowParamModal] = useState(false);
  const [paramValue, setParamValue] = useState(0);
  const [pendingGate, setPendingGate] = useState(null);

  const handleDragStart = (gateName) => {
    setDraggedGate(gateName);
  };

  const handleDrop = (qubitIndex) => {
    if (!draggedGate) return;

    const needsParam = ['RX', 'RY', 'RZ'].includes(draggedGate);
    
    if (needsParam) {
      setPendingGate({ gate: draggedGate, qubits: [qubitIndex] });
      setShowParamModal(true);
    } else {
      addGate(draggedGate, [qubitIndex], {});
    }
    
    setDraggedGate(null);
  };

  const handleTwoQubitGate = (gateName) => {
    // For two-qubit gates, we need to select both qubits
    // Simplified: use first two qubits for demo
    if (nQubits < 2) {
      alert('Need at least 2 qubits for this gate');
      return;
    }
    addGate(gateName, [0, 1], {});
  };

  const addGate = (gateName, qubits, params) => {
    const newGate = {
      gate: gateName,
      qubits: qubits,
      params: params,
    };
    setGates([...gates, newGate]);
  };

  const handleParamSubmit = () => {
    if (pendingGate) {
      const theta = parseFloat(paramValue);
      if (isNaN(theta)) {
        alert('Please enter a valid number');
        return;
      }
      addGate(pendingGate.gate, pendingGate.qubits, { theta });
      setPendingGate(null);
      setParamValue(0);
      setShowParamModal(false);
    }
  };

  const removeGate = (index) => {
    setGates(gates.filter((_, i) => i !== index));
  };

  const clearCircuit = () => {
    setGates([]);
  };

  const exportCircuit = () => {
    const circuitData = {
      n_qubits: nQubits,
      gates: gates,
    };
    const blob = new Blob([JSON.stringify(circuitData, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'quantum_circuit.json';
    a.click();
  };

  return (
    <div className="bg-gray-900 rounded-lg p-6 shadow-xl">
      <div className="flex justify-between items-center mb-4">
        <h2 className="text-2xl font-bold text-white">Circuit Builder</h2>
        <div className="flex gap-2">
          <button
            onClick={clearCircuit}
            className="px-4 py-2 bg-red-600 hover:bg-red-700 text-white rounded-lg flex items-center gap-2 transition"
          >
            <Trash2 size={16} />
            Clear
          </button>
          <button
            onClick={exportCircuit}
            className="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg flex items-center gap-2 transition"
          >
            <Download size={16} />
            Export
          </button>
          <button
            onClick={onRun}
            className="px-6 py-2 bg-gradient-to-r from-quantum-purple to-quantum-pink hover:opacity-90 text-white rounded-lg flex items-center gap-2 transition font-semibold"
          >
            <Play size={16} />
            Run Simulation
          </button>
        </div>
      </div>

      {/* Gate Palette */}
      <div className="mb-6">
        <h3 className="text-lg font-semibold text-white mb-3">Available Gates</h3>
        <div className="space-y-3">
          {Object.entries(AVAILABLE_GATES).map(([category, gateList]) => (
            <div key={category}>
              <p className="text-sm text-gray-400 mb-2">{category}</p>
              <div className="flex flex-wrap gap-2">
                {gateList.map((gateName) => (
                  <div
                    key={gateName}
                    draggable
                    onDragStart={() => handleDragStart(gateName)}
                    onClick={() => {
                      if (gateName === 'CNOT' || gateName === 'CZ' || gateName === 'SWAP') {
                        handleTwoQubitGate(gateName);
                      }
                    }}
                    className={`${GATE_COLORS[gateName]} quantum-gate px-4 py-2 text-white font-bold rounded-lg cursor-move`}
                  >
                    {gateName}
                  </div>
                ))}
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Circuit Canvas */}
      <div className="bg-gray-800 rounded-lg p-6">
        <h3 className="text-lg font-semibold text-white mb-4">Quantum Circuit</h3>
        <svg width="100%" height={nQubits * 80 + 40} className="bg-gray-850 rounded">
          {/* Draw qubit wires */}
          {Array.from({ length: nQubits }).map((_, qubitIdx) => (
            <g key={`qubit-${qubitIdx}`}>
              <line
                x1="40"
                y1={60 + qubitIdx * 80}
                x2="95%"
                y2={60 + qubitIdx * 80}
                className="quantum-wire"
              />
              <text
                x="10"
                y={60 + qubitIdx * 80}
                fill="white"
                dominantBaseline="middle"
                fontSize="14"
              >
                q{qubitIdx}
              </text>
              
              {/* Drop zone */}
              <rect
                x="40"
                y={30 + qubitIdx * 80}
                width="90%"
                height="60"
                fill="transparent"
                onDragOver={(e) => e.preventDefault()}
                onDrop={() => handleDrop(qubitIdx)}
                className="cursor-pointer"
              />
            </g>
          ))}

          {/* Draw gates */}
          {gates.map((gate, idx) => {
            const xPos = 100 + idx * 80;
            const yPos = 60 + gate.qubits[0] * 80;

            if (gate.gate === 'CNOT' && gate.qubits.length === 2) {
              const controlY = 60 + gate.qubits[0] * 80;
              const targetY = 60 + gate.qubits[1] * 80;
              return (
                <g key={`gate-${idx}`}>
                  {/* Control-target line */}
                  <line
                    x1={xPos}
                    y1={controlY}
                    x2={xPos}
                    y2={targetY}
                    stroke="#0066ff"
                    strokeWidth="2"
                  />
                  {/* Control dot */}
                  <circle cx={xPos} cy={controlY} r="6" fill="#0066ff" />
                  {/* Target circle with cross */}
                  <circle cx={xPos} cy={targetY} r="15" fill="none" stroke="#0066ff" strokeWidth="2" />
                  <line x1={xPos - 10} y1={targetY} x2={xPos + 10} y2={targetY} stroke="#0066ff" strokeWidth="2" />
                  <line x1={xPos} y1={targetY - 10} x2={xPos} y2={targetY + 10} stroke="#0066ff" strokeWidth="2" />
                </g>
              );
            }

            return (
              <g key={`gate-${idx}`}>
                <rect
                  x={xPos - 25}
                  y={yPos - 20}
                  width="50"
                  height="40"
                  className={GATE_COLORS[gate.gate]}
                  rx="5"
                />
                <text
                  x={xPos}
                  y={yPos}
                  fill="white"
                  textAnchor="middle"
                  dominantBaseline="middle"
                  fontSize="12"
                  fontWeight="bold"
                >
                  {gate.gate}
                </text>
                {/* Delete button */}
                <circle
                  cx={xPos + 20}
                  cy={yPos - 25}
                  r="8"
                  fill="#ef4444"
                  className="cursor-pointer"
                  onClick={() => removeGate(idx)}
                />
                <text
                  x={xPos + 20}
                  y={yPos - 25}
                  fill="white"
                  textAnchor="middle"
                  dominantBaseline="middle"
                  fontSize="10"
                  className="cursor-pointer pointer-events-none"
                >
                  ×
                </text>
              </g>
            );
          })}
        </svg>

        <div className="mt-4 text-sm text-gray-400">
          <p>Drag gates from the palette above and drop them on qubit wires</p>
          <p>Gates applied: {gates.length} | Circuit depth: {gates.length}</p>
        </div>
      </div>

      {/* Parameter Modal */}
      {showParamModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-gray-800 p-6 rounded-lg shadow-xl max-w-md w-full">
            <h3 className="text-xl font-bold text-white mb-4">
              Enter Rotation Angle
            </h3>
            <p className="text-gray-400 mb-4">
              Enter the rotation angle θ (in radians) for {pendingGate?.gate}
            </p>
            <input
              type="number"
              step="0.01"
              value={paramValue}
              onChange={(e) => setParamValue(e.target.value)}
              className="w-full px-4 py-2 bg-gray-700 text-white rounded-lg mb-4 focus:outline-none focus:ring-2 focus:ring-quantum-purple"
              placeholder="e.g., 1.5708 for π/2"
            />
            <div className="flex gap-2">
              <button
                onClick={() => {
                  setShowParamModal(false);
                  setPendingGate(null);
                  setParamValue(0);
                }}
                className="flex-1 px-4 py-2 bg-gray-600 hover:bg-gray-700 text-white rounded-lg transition"
              >
                Cancel
              </button>
              <button
                onClick={handleParamSubmit}
                className="flex-1 px-4 py-2 bg-quantum-purple hover:bg-purple-600 text-white rounded-lg transition"
              >
                Add Gate
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default CircuitBuilder;
