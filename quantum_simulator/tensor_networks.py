"""
Tensor network utilities for efficient quantum circuit simulation.
Uses MPS (Matrix Product State) representation and tensor contractions.
"""
import numpy as np
from typing import List, Tuple
import opt_einsum as oe


class MPS:
    """Matrix Product State representation."""
    
    def __init__(self, n_qubits: int, max_bond_dim: int = 100):
        """
        Initialize an MPS.
        
        Args:
            n_qubits: Number of qubits
            max_bond_dim: Maximum bond dimension for truncation
        """
        self.n_qubits = n_qubits
        self.max_bond_dim = max_bond_dim
        self.tensors: List[np.ndarray] = []
        
        # Initialize to |0...0⟩ state
        for i in range(n_qubits):
            if i == 0:
                # First tensor: shape (2, bond_dim)
                tensor = np.zeros((2, 1), dtype=complex)
                tensor[0, 0] = 1.0
            elif i == n_qubits - 1:
                # Last tensor: shape (bond_dim, 2)
                tensor = np.zeros((1, 2), dtype=complex)
                tensor[0, 0] = 1.0
            else:
                # Middle tensors: shape (bond_dim, 2, bond_dim)
                tensor = np.zeros((1, 2, 1), dtype=complex)
                tensor[0, 0, 0] = 1.0
            
            self.tensors.append(tensor)
    
    @classmethod
    def from_state_vector(cls, state: np.ndarray, max_bond_dim: int = 100):
        """
        Create an MPS from a state vector using SVD decomposition.
        
        Args:
            state: State vector
            max_bond_dim: Maximum bond dimension
        
        Returns:
            MPS object
        """
        n_qubits = int(np.log2(len(state)))
        mps = cls(n_qubits, max_bond_dim)
        
        # Reshape state into tensor and decompose
        remaining = state.reshape([2] * n_qubits)
        
        for i in range(n_qubits - 1):
            # Reshape for SVD
            shape = remaining.shape
            remaining = remaining.reshape(2 * (2 ** i), -1)
            
            # SVD
            U, S, Vh = np.linalg.svd(remaining, full_matrices=False)
            
            # Truncate
            bond_dim = min(max_bond_dim, len(S))
            U = U[:, :bond_dim]
            S = S[:bond_dim]
            Vh = Vh[:bond_dim, :]
            
            # Store tensor
            if i == 0:
                mps.tensors[i] = U.reshape(2, bond_dim)
            else:
                prev_bond = mps.tensors[i-1].shape[-1]
                mps.tensors[i] = U.reshape(prev_bond, 2, bond_dim)
            
            # Update remaining
            remaining = np.diag(S) @ Vh
            remaining = remaining.reshape([bond_dim] + [2] * (n_qubits - i - 1))
        
        # Last tensor
        mps.tensors[-1] = remaining.reshape(-1, 2)
        
        return mps
    
    def to_state_vector(self) -> np.ndarray:
        """
        Convert MPS back to a state vector.
        
        Returns:
            State vector
        """
        # Contract all tensors
        result = self.tensors[0]
        
        for i in range(1, self.n_qubits):
            if i == 1:
                # result: (2, bond), tensor: (bond, 2, bond) or (bond, 2)
                result = np.tensordot(result, self.tensors[i], axes=([-1], [0]))
            else:
                result = np.tensordot(result, self.tensors[i], axes=([-1], [0]))
        
        # Reshape to vector
        return result.flatten()


def apply_gate_tensor(state_tensor: np.ndarray, gate: np.ndarray, 
                     qubit_indices: List[int]) -> np.ndarray:
    """
    Apply a gate to specific qubits using tensor contraction.
    
    Args:
        state_tensor: State as a tensor of shape (2, 2, ..., 2)
        gate: Gate matrix (2^k × 2^k for k qubits)
        qubit_indices: Indices of qubits the gate acts on
    
    Returns:
        Updated state tensor
    """
    n_gate_qubits = len(qubit_indices)
    gate_shape = tuple([2] * n_gate_qubits + [2] * n_gate_qubits)
    gate_tensor = gate.reshape(gate_shape)
    
    # Build einsum string
    n_qubits = len(state_tensor.shape)
    
    # Input indices for state
    state_indices = list(range(n_qubits))
    
    # Gate input/output indices
    gate_in_indices = [n_qubits + i for i in range(n_gate_qubits)]
    gate_out_indices = [qubit_indices[i] for i in range(n_gate_qubits)]
    
    # Modify state indices for contracted qubits
    for i, q_idx in enumerate(qubit_indices):
        state_indices[q_idx] = gate_in_indices[i]
    
    # Output indices
    output_indices = list(range(n_qubits))
    
    # Perform contraction
    result = oe.contract(state_tensor, state_indices, gate_tensor, 
                        gate_out_indices + gate_in_indices, output_indices)
    
    return result


def tensor_network_simulator(n_qubits: int, gates: List[Tuple], 
                             use_mps: bool = False) -> np.ndarray:
    """
    Simulate a quantum circuit using tensor network methods.
    
    Args:
        n_qubits: Number of qubits
        gates: List of (gate_matrix, qubit_indices) tuples
        use_mps: Whether to use MPS representation
    
    Returns:
        Final state vector
    """
    if use_mps:
        mps = MPS(n_qubits)
        # MPS gate application would require more complex logic
        # For now, fall back to state vector
        state = mps.to_state_vector()
    else:
        # Start with |0...0⟩
        state_tensor = np.zeros([2] * n_qubits, dtype=complex)
        state_tensor[(0,) * n_qubits] = 1.0
    
    # Apply gates
    for gate, qubit_indices in gates:
        state_tensor = apply_gate_tensor(state_tensor, gate, qubit_indices)
    
    # Convert back to vector
    return state_tensor.flatten()
