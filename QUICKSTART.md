# QSimulateX - Quick Start Guide

## 🚀 Get Started in 3 Steps

### Step 1: Install Python Dependencies
```bash
pip install -r requirements.txt
```

### Step 2A: Try the Python Demo (No Web UI Required)
```bash
python main.py
```
This will show you examples of:
- Bell states
- GHZ states  
- Circuit optimization
- Quantum interference
- And more!

### Step 2B: Run the Full Web Application

**Terminal 1 - Start Backend:**
```bash
# Option 1: Using the batch script
start_backend.bat

# Option 2: Manual
python -m quantum_simulator.api
```

**Terminal 2 - Start Frontend:**
```bash
cd web-ui
npm install
npm run dev
```

Then open http://localhost:3000 in your browser!

---

## 🎯 Quick Examples

### Example 1: Create a Bell State (Python)
```python
from quantum_simulator import create_bell_state

circuit = create_bell_state()
state = circuit.run()
measurements = circuit.measure(shots=1000)
print(measurements)
# Output: {'00': ~500, '11': ~500}
```

### Example 2: Single Qubit Superposition
```python
from quantum_simulator import QuantumCircuit

circuit = QuantumCircuit(1)
circuit.h(0)  # Apply Hadamard
state = circuit.run()
print(circuit.get_probabilities())
# Output: [0.5, 0.5] - equal superposition
```

### Example 3: Rotation Gates
```python
import numpy as np
from quantum_simulator import QuantumCircuit

circuit = QuantumCircuit(1)
circuit.ry(0, np.pi/4)  # Rotate π/4 around Y-axis
state = circuit.run()

from quantum_simulator.qubit import Qubit
q = Qubit(state[0], state[1])
print(q.get_bloch_vector())  # See coordinates on Bloch sphere
```

---

## 🌐 Using the Web UI

1. **Set Number of Qubits**: Choose 1-10 qubits
2. **Build Circuit**: Drag gates from the palette onto wires
3. **Run Simulation**: Click "Run Simulation" button
4. **View Results**: 
   - State vector amplitudes
   - Measurement histogram
   - Bloch sphere (for 1 qubit)

### Creating a Bell State in Web UI:
1. Set qubits to 2
2. Drag H gate onto qubit 0
3. Click CNOT (will apply to qubits 0 and 1)
4. Click "Run Simulation"
5. See 50/50 split between |00⟩ and |11⟩!

---

## 📊 Available Gates

**Single-Qubit Gates:**
- **H**: Hadamard (superposition)
- **X**: Pauli-X (NOT gate)
- **Y**: Pauli-Y
- **Z**: Pauli-Z (phase flip)
- **T**: T gate (π/4 phase)
- **S**: S gate (π/2 phase)

**Parameterized Gates:**
- **RX(θ)**: Rotation around X-axis
- **RY(θ)**: Rotation around Y-axis
- **RZ(θ)**: Rotation around Z-axis

**Two-Qubit Gates:**
- **CNOT**: Controlled-NOT (entanglement)
- **CZ**: Controlled-Z
- **SWAP**: Swap qubits

---

## 🔍 API Endpoints (when backend is running)

**Base URL**: http://localhost:8000

- `GET /` - Health check
- `GET /gates` - List available gates
- `POST /run-circuit` - Run a circuit
- `POST /optimize` - Optimize a circuit
- `POST /bloch-sphere` - Get Bloch coordinates

**Interactive Docs**: http://localhost:8000/docs

---

## 🐛 Troubleshooting

**Problem**: Backend won't start
```bash
# Make sure dependencies are installed
pip install -r requirements.txt

# Try running manually
python -m quantum_simulator.api
```

**Problem**: Frontend won't start
```bash
cd web-ui
npm install
npm run dev
```

**Problem**: "Module not found" errors
```bash
# Reinstall Python packages
pip install -r requirements.txt --force-reinstall
```

---

## 💡 Tips

1. **Start Small**: Begin with 1-2 qubits to understand behavior
2. **Use Optimization**: Enable circuit optimization for better performance
3. **More Shots = Better Statistics**: Use 1000+ shots for accurate probabilities
4. **Bloch Sphere**: Only works with single-qubit circuits
5. **Circuit Depth**: Keep depth reasonable for faster simulation

---

## 📚 Next Steps

- Read the full [README.md](README.md) for detailed documentation
- Explore `main.py` for more Python examples
- Check API docs at http://localhost:8000/docs
- Experiment with different quantum circuits!

---

**Ready to simulate quantum circuits! 🚀⚛️**
