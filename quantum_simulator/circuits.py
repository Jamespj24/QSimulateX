"""
Quantum circuit class with tensor network simulation support.
"""
import numpy as np
from typing import List, Dict, Any, Optional, Tuple
from .gates import get_gate, apply_single_qubit_gate, apply_two_qubit_gate
from .qubit import create_multi_qubit_state
from .measure import get_probabilities, measure_counts
from .sparse_utils import sparse_state_vector_product, should_use_sparse
from .tensor_networks import tensor_network_simulator
from .optimizer import GateNode, CircuitOptimizer


class QuantumCircuit:
    """Quantum circuit simulator with optimization support."""
    
    def __init__(self, n_qubits: int, use_sparse: bool = None, use_tensor_network: bool = False):
        """
        Initialize a quantum circuit.
        
        Args:
            n_qubits: Number of qubits
            use_sparse: Whether to use sparse matrices (auto-detect if None)
            use_tensor_network: Whether to use tensor network simulation
        """
        self.n_qubits = n_qubits
        self.use_tensor_network = use_tensor_network
        
        # Auto-detect sparse usage
        if use_sparse is None:
            self.use_sparse = should_use_sparse(n_qubits)
        else:
            self.use_sparse = use_sparse
        
        # Initialize state to |0...0⟩
        self.state = create_multi_qubit_state(n_qubits, 0)
        
        # Gate history for optimization and visualization
        self.gates: List[GateNode] = []
        
        # Optimizer
        self.optimizer = CircuitOptimizer()
    
    def reset(self):
        """Reset the circuit to |0...0⟩."""
        self.state = create_multi_qubit_state(self.n_qubits, 0)
        self.gates = []
    
    def add_gate(self, gate_name: str, qubits: List[int], **params):
        """
        Add a gate to the circuit.
        
        Args:
            gate_name: Name of the gate
            qubits: List of qubit indices the gate acts on
            **params: Gate parameters (e.g., theta for rotations)
        """
        gate_node = GateNode(
            gate_name=gate_name,
            qubits=qubits,
            params=params
        )
        self.gates.append(gate_node)
    
    def x(self, qubit: int):
        """Apply Pauli-X gate."""
        self.add_gate('X', [qubit])
    
    def y(self, qubit: int):
        """Apply Pauli-Y gate."""
        self.add_gate('Y', [qubit])
    
    def z(self, qubit: int):
        """Apply Pauli-Z gate."""
        self.add_gate('Z', [qubit])
    
    def h(self, qubit: int):
        """Apply Hadamard gate."""
        self.add_gate('H', [qubit])
    
    def t(self, qubit: int):
        """Apply T gate."""
        self.add_gate('T', [qubit])
    
    def s(self, qubit: int):
        """Apply S gate."""
        self.add_gate('S', [qubit])
    
    def rx(self, qubit: int, theta: float):
        """Apply RX rotation."""
        self.add_gate('RX', [qubit], theta=theta)
    
    def ry(self, qubit: int, theta: float):
        """Apply RY rotation."""
        self.add_gate('RY', [qubit], theta=theta)
    
    def rz(self, qubit: int, theta: float):
        """Apply RZ rotation."""
        self.add_gate('RZ', [qubit], theta=theta)
    
    def cnot(self, control: int, target: int):
        """Apply CNOT gate."""
        self.add_gate('CNOT', [control, target])
    
    def cz(self, control: int, target: int):
        """Apply CZ gate."""
        self.add_gate('CZ', [control, target])
    
    def swap(self, qubit1: int, qubit2: int):
        """Apply SWAP gate."""
        self.add_gate('SWAP', [qubit1, qubit2])
    
    def run(self, optimize: bool = True) -> np.ndarray:
        """
        Run the circuit simulation.
        
        Args:
            optimize: Whether to optimize the circuit before running
        
        Returns:
            Final state vector
        """
        gates_to_run = self.gates
        
        if optimize:
            gates_to_run = self.optimizer.optimize(gates_to_run)
        
        if self.use_tensor_network:
            # Tensor network simulation
            gate_tuples = []
            for gate_node in gates_to_run:
                gate_matrix = get_gate(gate_node.gate_name, **gate_node.params)
                gate_tuples.append((gate_matrix, gate_node.qubits))
            
            self.state = tensor_network_simulator(self.n_qubits, gate_tuples)
        else:
            # Standard state vector simulation
            self.state = create_multi_qubit_state(self.n_qubits, 0)
            
            for gate_node in gates_to_run:
                gate_matrix = get_gate(gate_node.gate_name, **gate_node.params)
                
                if len(gate_node.qubits) == 1:
                    # Single-qubit gate
                    full_gate = apply_single_qubit_gate(
                        gate_matrix, gate_node.qubits[0], self.n_qubits, self.use_sparse
                    )
                elif len(gate_node.qubits) == 2:
                    # Two-qubit gate
                    full_gate = apply_two_qubit_gate(
                        gate_matrix, gate_node.qubits[0], gate_node.qubits[1], 
                        self.n_qubits, self.use_sparse
                    )
                else:
                    raise NotImplementedError(f"Gates with {len(gate_node.qubits)} qubits not yet supported")
                
                self.state = sparse_state_vector_product(full_gate, self.state)
        
        return self.state
    
    def get_statevector(self) -> np.ndarray:
        """Get the current state vector."""
        return self.state
    
    def get_probabilities(self) -> np.ndarray:
        """Get measurement probabilities."""
        return get_probabilities(self.state)
    
    def measure(self, shots: int = 1000) -> Dict[str, int]:
        """
        Measure the circuit.
        
        Args:
            shots: Number of measurements
        
        Returns:
            Dictionary of measurement counts
        """
        return measure_counts(self.state, shots)
    
    def get_circuit_info(self) -> Dict[str, Any]:
        """Get information about the circuit."""
        return {
            'n_qubits': self.n_qubits,
            'n_gates': len(self.gates),
            'depth': self.optimizer.calculate_circuit_depth(self.gates),
            'gate_counts': self.optimizer.estimate_gate_count(self.gates),
            'use_sparse': self.use_sparse,
            'use_tensor_network': self.use_tensor_network,
        }
    
    def to_json(self) -> Dict[str, Any]:
        """Export circuit to JSON format."""
        return {
            'n_qubits': self.n_qubits,
            'gates': [
                {
                    'gate': g.gate_name,
                    'qubits': g.qubits,
                    'params': g.params
                }
                for g in self.gates
            ]
        }
    
    @classmethod
    def from_json(cls, data: Dict[str, Any]) -> 'QuantumCircuit':
        """Create a circuit from JSON data."""
        circuit = cls(data['n_qubits'])
        
        for gate_data in data['gates']:
            circuit.add_gate(
                gate_data['gate'],
                gate_data['qubits'],
                **gate_data.get('params', {})
            )
        
        return circuit


def create_bell_state(qubit1: int = 0, qubit2: int = 1) -> QuantumCircuit:
    """
    Create a Bell state circuit.
    
    Returns:
        QuantumCircuit configured for Bell state
    """
    circuit = QuantumCircuit(2)
    circuit.h(qubit1)
    circuit.cnot(qubit1, qubit2)
    return circuit


def create_ghz_state(n_qubits: int) -> QuantumCircuit:
    """
    Create a GHZ state circuit.
    
    Args:
        n_qubits: Number of qubits
    
    Returns:
        QuantumCircuit configured for GHZ state
    """
    circuit = QuantumCircuit(n_qubits)
    circuit.h(0)
    for i in range(n_qubits - 1):
        circuit.cnot(i, i + 1)
    return circuit
