"""
FastAPI backend for quantum circuit simulation.
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import numpy as np

from .circuits import QuantumCircuit
from .gates import GATE_MAP


app = FastAPI(title="Quantum Simulator API", version="1.0.0")

# Enable CORS for web frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ===== Request/Response Models =====

class GateOperation(BaseModel):
    gate: str
    qubits: List[int]
    params: Optional[Dict[str, float]] = {}


class CircuitRequest(BaseModel):
    n_qubits: int
    gates: List[GateOperation]
    shots: Optional[int] = 1000
    optimize: Optional[bool] = True


class CircuitResponse(BaseModel):
    state_vector: List[Dict[str, float]]  # [{"real": ..., "imag": ...}]
    probabilities: List[float]
    measurements: Dict[str, int]
    circuit_info: Dict[str, Any]


class OptimizeRequest(BaseModel):
    n_qubits: int
    gates: List[GateOperation]


class OptimizeResponse(BaseModel):
    original_gates: List[Dict[str, Any]]
    optimized_gates: List[Dict[str, Any]]
    original_depth: int
    optimized_depth: int
    gate_count_reduction: Dict[str, int]


# ===== Endpoints =====

@app.get("/")
async def root():
    """Health check endpoint."""
    return {
        "message": "Quantum Simulator API is running",
        "version": "1.0.0"
    }


@app.get("/gates")
async def get_available_gates():
    """Get list of available gates."""
    gate_info = {
        "single_qubit": ["X", "Y", "Z", "H", "T", "S"],
        "parameterized": ["RX", "RY", "RZ", "PHASE"],
        "two_qubit": ["CNOT", "CZ", "SWAP"],
        "three_qubit": ["TOFFOLI"],
    }
    
    gate_descriptions = {
        "X": "Pauli-X (NOT) gate",
        "Y": "Pauli-Y gate",
        "Z": "Pauli-Z gate",
        "H": "Hadamard gate",
        "T": "T gate (π/4 phase)",
        "S": "S gate (π/2 phase)",
        "RX": "Rotation around X-axis (requires theta parameter)",
        "RY": "Rotation around Y-axis (requires theta parameter)",
        "RZ": "Rotation around Z-axis (requires theta parameter)",
        "PHASE": "Phase gate (requires phi parameter)",
        "CNOT": "Controlled-NOT gate",
        "CZ": "Controlled-Z gate",
        "SWAP": "SWAP gate",
        "TOFFOLI": "Toffoli (CCNOT) gate",
    }
    
    return {
        "gates": gate_info,
        "descriptions": gate_descriptions
    }


@app.post("/run-circuit", response_model=CircuitResponse)
async def run_circuit(request: CircuitRequest):
    """
    Run a quantum circuit and return results.
    
    Args:
        request: Circuit specification
    
    Returns:
        Circuit results including state vector, probabilities, and measurements
    """
    try:
        # Create circuit
        circuit = QuantumCircuit(request.n_qubits)
        
        # Add gates
        for gate_op in request.gates:
            circuit.add_gate(gate_op.gate, gate_op.qubits, **gate_op.params)
        
        # Run simulation
        state = circuit.run(optimize=request.optimize)
        
        # Get probabilities
        probs = circuit.get_probabilities()
        
        # Perform measurements
        measurements = circuit.measure(shots=request.shots)
        
        # Get circuit info
        circuit_info = circuit.get_circuit_info()
        
        # Format state vector for JSON
        state_vector_json = [
            {"real": float(np.real(amplitude)), "imag": float(np.imag(amplitude))}
            for amplitude in state
        ]
        
        return CircuitResponse(
            state_vector=state_vector_json,
            probabilities=probs.tolist(),
            measurements=measurements,
            circuit_info=circuit_info
        )
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/optimize", response_model=OptimizeResponse)
async def optimize_circuit(request: OptimizeRequest):
    """
    Optimize a quantum circuit.
    
    Args:
        request: Circuit to optimize
    
    Returns:
        Original and optimized circuits with statistics
    """
    try:
        # Create circuit
        circuit = QuantumCircuit(request.n_qubits)
        
        # Add gates
        for gate_op in request.gates:
            circuit.add_gate(gate_op.gate, gate_op.qubits, **gate_op.params)
        
        # Get original stats
        original_depth = circuit.optimizer.calculate_circuit_depth(circuit.gates)
        original_counts = circuit.optimizer.estimate_gate_count(circuit.gates)
        
        # Optimize
        optimized_gates = circuit.optimizer.optimize(circuit.gates)
        optimized_depth = circuit.optimizer.calculate_circuit_depth(optimized_gates)
        optimized_counts = circuit.optimizer.estimate_gate_count(optimized_gates)
        
        # Calculate reductions
        gate_count_reduction = {}
        for gate_name in set(list(original_counts.keys()) + list(optimized_counts.keys())):
            original = original_counts.get(gate_name, 0)
            optimized = optimized_counts.get(gate_name, 0)
            gate_count_reduction[gate_name] = original - optimized
        
        # Format gates for JSON
        original_gates_json = [
            {
                "gate": g.gate_name,
                "qubits": g.qubits,
                "params": g.params,
                "depth": g.depth
            }
            for g in circuit.gates
        ]
        
        optimized_gates_json = [
            {
                "gate": g.gate_name,
                "qubits": g.qubits,
                "params": g.params,
                "depth": g.depth
            }
            for g in optimized_gates
        ]
        
        return OptimizeResponse(
            original_gates=original_gates_json,
            optimized_gates=optimized_gates_json,
            original_depth=original_depth,
            optimized_depth=optimized_depth,
            gate_count_reduction=gate_count_reduction
        )
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/bloch-sphere")
async def get_bloch_sphere_data(request: CircuitRequest):
    """
    Get Bloch sphere coordinates for a single-qubit state.
    
    Args:
        request: Circuit specification (must be 1 qubit)
    
    Returns:
        Bloch sphere coordinates (x, y, z)
    """
    try:
        if request.n_qubits != 1:
            raise ValueError("Bloch sphere visualization only supports single-qubit states")
        
        # Create and run circuit
        circuit = QuantumCircuit(request.n_qubits)
        
        for gate_op in request.gates:
            circuit.add_gate(gate_op.gate, gate_op.qubits, **gate_op.params)
        
        state = circuit.run(optimize=request.optimize)
        
        # Calculate Bloch vector
        alpha, beta = state[0], state[1]
        x = 2 * float(np.real(np.conj(alpha) * beta))
        y = 2 * float(np.imag(np.conj(alpha) * beta))
        z = float(np.abs(alpha)**2 - np.abs(beta)**2)
        
        return {
            "x": x,
            "y": y,
            "z": z,
            "state": {
                "alpha": {"real": float(np.real(alpha)), "imag": float(np.imag(alpha))},
                "beta": {"real": float(np.real(beta)), "imag": float(np.imag(beta))}
            }
        }
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
