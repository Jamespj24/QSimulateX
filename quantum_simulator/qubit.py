"""
Qubit class and single-qubit state representations.
"""
import numpy as np
from typing import Union


class Qubit:
    """Represents a single qubit in quantum state."""
    
    def __init__(self, alpha: complex = 1.0, beta: complex = 0.0):
        """
        Initialize a qubit in state |ψ⟩ = α|0⟩ + β|1⟩
        
        Args:
            alpha: Amplitude of |0⟩ state
            beta: Amplitude of |1⟩ state
        """
        self.state = np.array([alpha, beta], dtype=complex)
        self.normalize()
    
    def normalize(self):
        """Normalize the quantum state to unit length."""
        norm = np.linalg.norm(self.state)
        if norm > 0:
            self.state = self.state / norm
    
    @classmethod
    def zero(cls):
        """Create |0⟩ state."""
        return cls(1.0, 0.0)
    
    @classmethod
    def one(cls):
        """Create |1⟩ state."""
        return cls(0.0, 1.0)
    
    @classmethod
    def plus(cls):
        """Create |+⟩ = (|0⟩ + |1⟩)/√2 state."""
        return cls(1/np.sqrt(2), 1/np.sqrt(2))
    
    @classmethod
    def minus(cls):
        """Create |−⟩ = (|0⟩ − |1⟩)/√2 state."""
        return cls(1/np.sqrt(2), -1/np.sqrt(2))
    
    def get_bloch_vector(self):
        """
        Get the Bloch sphere representation (x, y, z).
        
        Returns:
            tuple: (x, y, z) coordinates on Bloch sphere
        """
        alpha, beta = self.state
        
        # Bloch vector coordinates
        x = 2 * np.real(np.conj(alpha) * beta)
        y = 2 * np.imag(np.conj(alpha) * beta)
        z = np.abs(alpha)**2 - np.abs(beta)**2
        
        return (float(x), float(y), float(z))
    
    def probabilities(self):
        """
        Get measurement probabilities.
        
        Returns:
            tuple: (P(0), P(1))
        """
        return (np.abs(self.state[0])**2, np.abs(self.state[1])**2)
    
    def __repr__(self):
        return f"Qubit({self.state[0]:.4f}|0⟩ + {self.state[1]:.4f}|1⟩)"


def create_multi_qubit_state(n_qubits: int, state: Union[str, int] = 0) -> np.ndarray:
    """
    Create an n-qubit state.
    
    Args:
        n_qubits: Number of qubits
        state: Initial state (integer or binary string)
    
    Returns:
        np.ndarray: State vector of dimension 2^n_qubits
    """
    dim = 2**n_qubits
    state_vector = np.zeros(dim, dtype=complex)
    
    if isinstance(state, str):
        # Binary string like "101"
        state_index = int(state, 2)
    else:
        state_index = state
    
    state_vector[state_index] = 1.0
    return state_vector
