"""
Measurement utilities for quantum circuits.
"""
import numpy as np
from typing import Tuple, List, Dict


def get_probabilities(state: np.ndarray) -> np.ndarray:
    """
    Calculate measurement probabilities from a state vector.
    
    Args:
        state: Quantum state vector
    
    Returns:
        Array of probabilities for each basis state
    """
    return np.abs(state) ** 2


def measure(state: np.ndarray, shots: int = 1) -> List[int]:
    """
    Perform measurements on a quantum state.
    
    Args:
        state: Quantum state vector
        shots: Number of measurements
    
    Returns:
        List of measurement outcomes (basis state indices)
    """
    probs = get_probabilities(state)
    n_states = len(state)
    
    # Sample from probability distribution
    outcomes = np.random.choice(n_states, size=shots, p=probs)
    return outcomes.tolist()


def measure_counts(state: np.ndarray, shots: int = 1000) -> Dict[str, int]:
    """
    Perform measurements and return counts as binary strings.
    
    Args:
        state: Quantum state vector
        shots: Number of measurements
    
    Returns:
        Dictionary mapping binary strings to counts
    """
    outcomes = measure(state, shots)
    n_qubits = int(np.log2(len(state)))
    
    counts = {}
    for outcome in outcomes:
        binary_str = format(outcome, f'0{n_qubits}b')
        counts[binary_str] = counts.get(binary_str, 0) + 1
    
    return counts


def collapse_state(state: np.ndarray, outcome: int) -> np.ndarray:
    """
    Collapse the state to a specific measurement outcome.
    
    Args:
        state: Quantum state vector
        outcome: Measured basis state index
    
    Returns:
        Collapsed state vector
    """
    collapsed = np.zeros_like(state)
    collapsed[outcome] = 1.0
    return collapsed


def partial_measure(state: np.ndarray, qubit_indices: List[int], 
                    n_qubits: int) -> Tuple[int, np.ndarray]:
    """
    Measure specific qubits and return the outcome and post-measurement state.
    
    Args:
        state: Quantum state vector
        qubit_indices: Indices of qubits to measure
        n_qubits: Total number of qubits
    
    Returns:
        Tuple of (measurement outcome, post-measurement state)
    """
    probs = get_probabilities(state)
    
    # For simplicity, perform full measurement and extract relevant qubits
    outcome = np.random.choice(len(state), p=probs)
    
    # Extract measured qubit values
    measured_value = 0
    for i, qubit_idx in enumerate(sorted(qubit_indices)):
        bit = (outcome >> qubit_idx) & 1
        measured_value |= (bit << i)
    
    # Collapse to subspace consistent with measurement
    post_state = np.zeros_like(state)
    norm_sq = 0
    
    for i, amplitude in enumerate(state):
        # Check if this basis state is consistent with measurement
        consistent = True
        for qubit_idx in qubit_indices:
            measured_bit = (outcome >> qubit_idx) & 1
            state_bit = (i >> qubit_idx) & 1
            if measured_bit != state_bit:
                consistent = False
                break
        
        if consistent:
            post_state[i] = amplitude
            norm_sq += np.abs(amplitude) ** 2
    
    # Normalize
    if norm_sq > 0:
        post_state = post_state / np.sqrt(norm_sq)
    
    return measured_value, post_state


def expectation_value(state: np.ndarray, observable: np.ndarray) -> complex:
    """
    Calculate the expectation value of an observable.
    
    Args:
        state: Quantum state vector
        observable: Observable matrix (Hermitian)
    
    Returns:
        Expectation value ⟨ψ|O|ψ⟩
    """
    return np.dot(np.conj(state), np.dot(observable, state))
