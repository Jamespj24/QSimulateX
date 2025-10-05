"""
Quantum gate definitions (dense and sparse).
"""
import numpy as np
from scipy.sparse import csr_matrix, kron as sparse_kron, identity as sparse_identity
from typing import Union


# ===== Single-Qubit Gates (Dense) =====

def pauli_x():
    """Pauli-X gate (NOT gate)."""
    return np.array([[0, 1], [1, 0]], dtype=complex)


def pauli_y():
    """Pauli-Y gate."""
    return np.array([[0, -1j], [1j, 0]], dtype=complex)


def pauli_z():
    """Pauli-Z gate."""
    return np.array([[1, 0], [0, -1]], dtype=complex)


def hadamard():
    """Hadamard gate."""
    return np.array([[1, 1], [1, -1]], dtype=complex) / np.sqrt(2)


def t_gate():
    """T gate (π/4 phase gate)."""
    return np.array([[1, 0], [0, np.exp(1j * np.pi / 4)]], dtype=complex)


def s_gate():
    """S gate (phase gate)."""
    return np.array([[1, 0], [0, 1j]], dtype=complex)


def rx(theta: float):
    """Rotation around X-axis."""
    return np.array([
        [np.cos(theta/2), -1j*np.sin(theta/2)],
        [-1j*np.sin(theta/2), np.cos(theta/2)]
    ], dtype=complex)


def ry(theta: float):
    """Rotation around Y-axis."""
    return np.array([
        [np.cos(theta/2), -np.sin(theta/2)],
        [np.sin(theta/2), np.cos(theta/2)]
    ], dtype=complex)


def rz(theta: float):
    """Rotation around Z-axis."""
    return np.array([
        [np.exp(-1j*theta/2), 0],
        [0, np.exp(1j*theta/2)]
    ], dtype=complex)


def phase(phi: float):
    """Phase gate with arbitrary angle."""
    return np.array([[1, 0], [0, np.exp(1j*phi)]], dtype=complex)


# ===== Two-Qubit Gates =====

def cnot():
    """Controlled-NOT (CNOT) gate."""
    return np.array([
        [1, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, 0, 1],
        [0, 0, 1, 0]
    ], dtype=complex)


def cz():
    """Controlled-Z gate."""
    return np.array([
        [1, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, -1]
    ], dtype=complex)


def swap():
    """SWAP gate."""
    return np.array([
        [1, 0, 0, 0],
        [0, 0, 1, 0],
        [0, 1, 0, 0],
        [0, 0, 0, 1]
    ], dtype=complex)


# ===== Three-Qubit Gates =====

def toffoli():
    """Toffoli (CCNOT) gate."""
    gate = np.eye(8, dtype=complex)
    gate[6, 6] = 0
    gate[7, 7] = 0
    gate[6, 7] = 1
    gate[7, 6] = 1
    return gate


# ===== Gate Application =====

def apply_single_qubit_gate(gate: np.ndarray, qubit_index: int, n_qubits: int, 
                           use_sparse: bool = False) -> Union[np.ndarray, csr_matrix]:
    """
    Create the full matrix for applying a single-qubit gate to a specific qubit.
    
    Args:
        gate: 2x2 gate matrix
        qubit_index: Index of the qubit to apply the gate to (0-indexed)
        n_qubits: Total number of qubits
        use_sparse: Whether to use sparse matrices
    
    Returns:
        Full gate matrix of size 2^n_qubits × 2^n_qubits
    """
    if use_sparse:
        identity = sparse_identity(2, dtype=complex, format='csr')
        gate_sparse = csr_matrix(gate)
        
        # Build tensor product
        if qubit_index == 0:
            result = gate_sparse
        else:
            result = identity
        
        for i in range(1, n_qubits):
            if i == qubit_index:
                result = sparse_kron(result, gate_sparse)
            else:
                result = sparse_kron(result, identity)
        
        return result
    else:
        # Dense version
        identity = np.eye(2, dtype=complex)
        
        if qubit_index == 0:
            result = gate
        else:
            result = identity
        
        for i in range(1, n_qubits):
            if i == qubit_index:
                result = np.kron(result, gate)
            else:
                result = np.kron(result, identity)
        
        return result


def apply_two_qubit_gate(gate: np.ndarray, control: int, target: int, n_qubits: int,
                         use_sparse: bool = False) -> Union[np.ndarray, csr_matrix]:
    """
    Create the full matrix for applying a two-qubit gate.
    
    Args:
        gate: 4x4 gate matrix
        control: Control qubit index
        target: Target qubit index
        n_qubits: Total number of qubits
        use_sparse: Whether to use sparse matrices
    
    Returns:
        Full gate matrix of size 2^n_qubits × 2^n_qubits
    """
    # For simplicity, this implementation assumes adjacent qubits
    # A full implementation would handle arbitrary qubit positions with SWAP gates
    
    if abs(control - target) != 1:
        raise NotImplementedError("Non-adjacent qubit gates require SWAP decomposition")
    
    if use_sparse:
        identity = sparse_identity(2, dtype=complex, format='csr')
        gate_sparse = csr_matrix(gate)
        
        min_idx = min(control, target)
        result = sparse_identity(1, dtype=complex, format='csr')
        
        for i in range(0, n_qubits, 2):
            if i == min_idx:
                result = sparse_kron(result, gate_sparse)
                break
            else:
                result = sparse_kron(result, identity)
        
        for i in range(min_idx + 2, n_qubits):
            result = sparse_kron(result, identity)
        
        return result
    else:
        # Dense version
        identity = np.eye(2, dtype=complex)
        min_idx = min(control, target)
        
        result = np.eye(1, dtype=complex)
        
        for i in range(0, min_idx):
            result = np.kron(result, identity)
        
        result = np.kron(result, gate)
        
        for i in range(min_idx + 2, n_qubits):
            result = np.kron(result, identity)
        
        return result


# ===== Gate Dictionary =====

GATE_MAP = {
    'X': pauli_x,
    'Y': pauli_y,
    'Z': pauli_z,
    'H': hadamard,
    'T': t_gate,
    'S': s_gate,
    'CNOT': cnot,
    'CZ': cz,
    'SWAP': swap,
    'TOFFOLI': toffoli,
}


def get_gate(gate_name: str, **params):
    """
    Get a gate by name with optional parameters.
    
    Args:
        gate_name: Name of the gate
        **params: Additional parameters (e.g., theta for rotation gates)
    
    Returns:
        Gate matrix
    """
    if gate_name in GATE_MAP:
        gate_func = GATE_MAP[gate_name]
        if callable(gate_func):
            return gate_func()
        return gate_func
    
    # Parameterized gates
    if gate_name == 'RX':
        return rx(params.get('theta', 0))
    elif gate_name == 'RY':
        return ry(params.get('theta', 0))
    elif gate_name == 'RZ':
        return rz(params.get('theta', 0))
    elif gate_name == 'PHASE':
        return phase(params.get('phi', 0))
    
    raise ValueError(f"Unknown gate: {gate_name}")
