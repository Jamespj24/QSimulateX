"""
Sparse matrix utilities for efficient large-scale quantum simulation.
"""
import numpy as np
from scipy.sparse import csr_matrix, issparse
from typing import Union


def to_sparse(matrix: np.ndarray, threshold: float = 1e-10) -> csr_matrix:
    """
    Convert a dense matrix to sparse format.
    
    Args:
        matrix: Dense matrix
        threshold: Values below this are considered zero
    
    Returns:
        Sparse matrix in CSR format
    """
    matrix_copy = matrix.copy()
    matrix_copy[np.abs(matrix_copy) < threshold] = 0
    return csr_matrix(matrix_copy)


def sparse_state_vector_product(matrix: Union[np.ndarray, csr_matrix], 
                                 state: np.ndarray) -> np.ndarray:
    """
    Efficiently multiply a (potentially sparse) matrix with a state vector.
    
    Args:
        matrix: Gate matrix (dense or sparse)
        state: State vector
    
    Returns:
        Resulting state vector
    """
    if issparse(matrix):
        return matrix.dot(state)
    else:
        return np.dot(matrix, state)


def estimate_sparsity(matrix: Union[np.ndarray, csr_matrix], threshold: float = 1e-10) -> float:
    """
    Estimate the sparsity of a matrix.
    
    Args:
        matrix: Matrix to analyze
        threshold: Values below this are considered zero
    
    Returns:
        Sparsity ratio (0 = dense, 1 = completely sparse)
    """
    if issparse(matrix):
        return 1.0 - matrix.nnz / (matrix.shape[0] * matrix.shape[1])
    else:
        total_elements = matrix.size
        zero_elements = np.sum(np.abs(matrix) < threshold)
        return zero_elements / total_elements


def should_use_sparse(n_qubits: int, gate_sparsity: float = 0.5) -> bool:
    """
    Determine if sparse matrices should be used based on system size.
    
    Args:
        n_qubits: Number of qubits
        gate_sparsity: Expected sparsity of gates
    
    Returns:
        True if sparse representation is beneficial
    """
    # Use sparse for systems with >10 qubits or high sparsity
    return n_qubits > 10 or gate_sparsity > 0.7
