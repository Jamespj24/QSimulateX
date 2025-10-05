# QSimulateX - Intelligent Quantum Computing Simulator

A full-stack quantum computing simulator with Python backend and modern React frontend, featuring real-time circuit visualization, state vector analysis, and interactive Bloch sphere rendering.

![Quantum Computing](https://img.shields.io/badge/quantum-computing-blue)
![Python](https://img.shields.io/badge/python-3.10+-blue)
![React](https://img.shields.io/badge/react-18.2-blue)
![FastAPI](https://img.shields.io/badge/fastapi-0.109-green)

## 🌟 Features

### Python Quantum Simulator
- **Complex State Vectors**: Full support for multi-qubit quantum states using complex number matrices
- **Tensor Networks**: Efficient simulation using MPS (Matrix Product State) representation and tensor contractions with `opt_einsum`
- **Sparse Matrices**: Scalable simulation for large quantum systems (10+ qubits)
- **Circuit Optimization**: Tree-based gate optimization to reduce circuit depth and gate count
- **Comprehensive Gate Library**: 
  - Single-qubit: X, Y, Z, H, T, S
  - Parameterized: RX, RY, RZ, Phase
  - Multi-qubit: CNOT, CZ, SWAP, Toffoli

### Web Frontend
- **Interactive Circuit Builder**: Drag-and-drop interface for building quantum circuits
- **Real-time Visualization**:
  - State vector amplitude display
  - Measurement probability histograms
  - 3D Bloch sphere rendering (for single qubits)
- **Modern UI**: Built with React, TailwindCSS, and Recharts
- **Responsive Design**: Works on desktop and tablet devices

### FastAPI Backend
- RESTful API for quantum circuit simulation
- Circuit optimization endpoint
- Bloch sphere data generation
- CORS-enabled for web frontend

---

## 📁 Project Structure

```
QSimulateX/
├── quantum_simulator/          # Python backend
│   ├── __init__.py            # Package initialization
│   ├── qubit.py               # Qubit class and states
│   ├── gates.py               # Quantum gate definitions
│   ├── circuits.py            # QuantumCircuit class
│   ├── measure.py             # Measurement utilities
│   ├── optimizer.py           # Circuit optimization
│   ├── tensor_networks.py     # Tensor network simulation
│   ├── sparse_utils.py        # Sparse matrix utilities
│   └── api.py                 # FastAPI backend
│
├── web-ui/                    # React frontend
│   ├── src/
│   │   ├── components/
│   │   │   ├── CircuitBuilder.jsx
│   │   │   ├── StateVectorView.jsx
│   │   │   ├── ProbabilityHistogram.jsx
│   │   │   └── BlochSphere.jsx
│   │   ├── App.jsx            # Main app component
│   │   ├── api.js             # API client
│   │   ├── main.jsx           # Entry point
│   │   └── index.css          # Styles
│   ├── package.json
│   ├── vite.config.js
│   └── tailwind.config.js
│
├── main.py                    # Demo script (no web UI)
├── requirements.txt           # Python dependencies
├── README.md                  # This file
└── todo.txt                   # Project specifications
```

---

## 🚀 Installation & Setup

### Prerequisites
- Python 3.10 or higher
- Node.js 18+ and npm
- Git (optional)

### 1. Install Python Backend

```bash
# Navigate to project directory
cd QSimulateX

# Create virtual environment (recommended)
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install Python dependencies
pip install -r requirements.txt
```

### 2. Install Frontend Dependencies

```bash
# Navigate to web-ui directory
cd web-ui

# Install npm packages
npm install
```

---

## 🎮 Usage

### Option 1: Full Stack (Backend + Frontend)

#### Start the Backend Server
```bash
# From project root directory
python -m quantum_simulator.api
```
The API will be available at `http://localhost:8000`

#### Start the Frontend Development Server
```bash
# In a new terminal, from web-ui directory
cd web-ui
npm run dev
```
The web app will be available at `http://localhost:3000`

### Option 2: Python Demo (No Web UI)

```bash
# From project root directory
python main.py
```

This will run a comprehensive demonstration of:
- Single-qubit gates
- Bell state creation (entanglement)
- GHZ state (3-qubit entanglement)
- Quantum interference
- Circuit optimization
- Custom circuits

---

## 📚 API Documentation

Once the backend is running, visit:
- **Interactive API Docs**: http://localhost:8000/docs
- **Alternative Docs**: http://localhost:8000/redoc

### Key Endpoints

#### `POST /run-circuit`
Run a quantum circuit simulation.

**Request Body:**
```json
{
  "n_qubits": 2,
  "gates": [
    {"gate": "H", "qubits": [0], "params": {}},
    {"gate": "CNOT", "qubits": [0, 1], "params": {}}
  ],
  "shots": 1000,
  "optimize": true
}
```

**Response:**
```json
{
  "state_vector": [...],
  "probabilities": [...],
  "measurements": {"00": 502, "11": 498},
  "circuit_info": {...}
}
```

#### `GET /gates`
Get available quantum gates and their descriptions.

#### `POST /optimize`
Optimize a quantum circuit to reduce depth and gate count.

#### `POST /bloch-sphere`
Get Bloch sphere coordinates for single-qubit states.

---

## 🧪 Example Circuits

### Bell State (Entanglement)
```python
from quantum_simulator import create_bell_state

circuit = create_bell_state()
state = circuit.run()
measurements = circuit.measure(shots=1000)
print(measurements)  # ~50% |00⟩, ~50% |11⟩
```

### Quantum Superposition
```python
from quantum_simulator import QuantumCircuit

circuit = QuantumCircuit(1)
circuit.h(0)  # Hadamard gate
state = circuit.run()
# State: (|0⟩ + |1⟩) / √2
```

### GHZ State (3-qubit Entanglement)
```python
from quantum_simulator import create_ghz_state

circuit = create_ghz_state(3)
state = circuit.run()
measurements = circuit.measure(shots=1000)
# ~50% |000⟩, ~50% |111⟩
```

### Rotation Gates
```python
import numpy as np
from quantum_simulator import QuantumCircuit

circuit = QuantumCircuit(1)
circuit.ry(0, np.pi / 4)  # Rotate around Y-axis
state = circuit.run()
```

---

## 🎨 Web UI Features

### Circuit Builder
- **Drag & Drop**: Drag gates from the palette onto qubit wires
- **Interactive**: Click to add two-qubit gates
- **Parameterized Gates**: Enter rotation angles for RX, RY, RZ gates
- **Visual Feedback**: Color-coded gates and real-time circuit display

### Visualizations

#### State Vector View
- Bar chart showing amplitude magnitudes
- Detailed breakdown of complex amplitudes (real and imaginary parts)
- Phase information

#### Probability Histogram
- Measurement outcome distribution
- Comparison between measured and theoretical probabilities
- Color-coded state labels

#### Bloch Sphere (Single Qubit)
- Interactive 3D visualization using Three.js
- Real-time rotation and zoom
- Coordinate display (X, Y, Z)
- State component breakdown

---

## 🔧 Configuration

### Backend Configuration
Edit `quantum_simulator/api.py`:
- Change host/port in the `if __name__ == "__main__"` block
- Modify CORS settings for production deployment

### Frontend Configuration
Create `web-ui/.env` file:
```env
VITE_API_URL=http://localhost:8000
```

---

## 🧠 Technical Details

### Quantum Simulation Methods

1. **State Vector Simulation**: Full state vector representation for exact results (up to ~15 qubits)
2. **Tensor Network Simulation**: MPS representation for efficient simulation of certain circuit types
3. **Sparse Matrix Optimization**: Automatically used for systems with >10 qubits

### Circuit Optimization

The optimizer applies several techniques:
- **Inverse Gate Cancellation**: Removes pairs of inverse gates (e.g., X-X, H-H)
- **Rotation Merging**: Combines consecutive rotation gates
- **Gate Commutation**: Reorders gates to reduce circuit depth

### Bloch Sphere Coordinates

For a single qubit in state α|0⟩ + β|1⟩:
- X = 2 × Re(α*β)
- Y = 2 × Im(α*β)
- Z = |α|² - |β|²

---

## 📊 Performance

- **Small circuits** (1-5 qubits): Near-instantaneous
- **Medium circuits** (6-10 qubits): < 1 second
- **Large circuits** (11-15 qubits): 1-10 seconds (with sparse matrices)

*Note: Performance depends on circuit depth and gate count*

---

## 🤝 Contributing

Contributions are welcome! Areas for improvement:
- Additional quantum gates (controlled-U, phase estimation)
- Noise models for realistic simulation
- GPU acceleration
- Quantum algorithm library
- Mobile-responsive UI enhancements

---

## 📝 License

This project is open source and available under the MIT License.

---

## 🙏 Acknowledgments

Built with:
- **NumPy** & **SciPy**: Numerical computation
- **FastAPI**: High-performance Python web framework
- **React**: Frontend framework
- **Three.js**: 3D visualization
- **Recharts**: Chart library
- **TailwindCSS**: Utility-first CSS framework
- **opt_einsum**: Optimized tensor contractions

---

## 📞 Support

For issues, questions, or suggestions:
1. Check the [API documentation](http://localhost:8000/docs) when backend is running
2. Run `python main.py` to see example usage
3. Review the code in `quantum_simulator/` directory

---

## 🎓 Learning Resources

To learn more about quantum computing:
- [Qiskit Textbook](https://qiskit.org/textbook/)
- [Quantum Computing for the Very Curious](https://quantum.country/)
- [Nielsen & Chuang: Quantum Computation and Quantum Information](http://mmrc.amss.cas.cn/tlb/201702/W020170224608149940643.pdf)

---

**Happy Quantum Computing! 🚀⚛️**