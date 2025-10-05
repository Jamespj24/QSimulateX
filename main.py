"""
Main demonstration of the Quantum Simulator without the web interface.
Creates various quantum circuits and displays results.
"""
import numpy as np
from quantum_simulator import QuantumCircuit, create_bell_state, create_ghz_state
from quantum_simulator.qubit import Qubit


def print_section(title):
    """Print a formatted section header."""
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60 + "\n")


def demonstrate_single_qubit_gates():
    """Demonstrate single-qubit gates."""
    print_section("Single-Qubit Gates Demo")
    
    # Hadamard gate - creates superposition
    print("1. Hadamard Gate (creates superposition)")
    circuit = QuantumCircuit(1)
    circuit.h(0)
    circuit.run()
    
    qubit = Qubit(circuit.state[0], circuit.state[1])
    print(f"   State: {qubit}")
    print(f"   Probabilities: P(0) = {qubit.probabilities()[0]:.4f}, P(1) = {qubit.probabilities()[1]:.4f}")
    print(f"   Bloch vector: {qubit.get_bloch_vector()}")
    
    # Pauli-X gate (NOT gate)
    print("\n2. Pauli-X Gate (NOT gate)")
    circuit = QuantumCircuit(1)
    circuit.x(0)
    circuit.run()
    
    qubit = Qubit(circuit.state[0], circuit.state[1])
    print(f"   State: {qubit}")
    print(f"   Probabilities: P(0) = {qubit.probabilities()[0]:.4f}, P(1) = {qubit.probabilities()[1]:.4f}")
    
    # Rotation gates
    print("\n3. RY Rotation (π/4)")
    circuit = QuantumCircuit(1)
    circuit.ry(0, np.pi / 4)
    circuit.run()
    
    qubit = Qubit(circuit.state[0], circuit.state[1])
    print(f"   State: {qubit}")
    print(f"   Probabilities: P(0) = {qubit.probabilities()[0]:.4f}, P(1) = {qubit.probabilities()[1]:.4f}")
    print(f"   Bloch vector: {qubit.get_bloch_vector()}")


def demonstrate_bell_state():
    """Demonstrate Bell state creation."""
    print_section("Bell State (Entanglement) Demo")
    
    circuit = create_bell_state()
    state = circuit.run()
    
    print("Circuit: H(0) → CNOT(0,1)")
    print(f"Final state vector: {state}")
    print(f"\nState decomposition:")
    for i, amplitude in enumerate(state):
        if np.abs(amplitude) > 1e-10:
            binary = format(i, '02b')
            print(f"   |{binary}⟩: {amplitude:.4f} (prob: {np.abs(amplitude)**2:.4f})")
    
    # Measure the circuit
    measurements = circuit.measure(shots=1000)
    print(f"\nMeasurement results (1000 shots):")
    for state_str, count in sorted(measurements.items(), key=lambda x: -x[1]):
        percentage = (count / 1000) * 100
        print(f"   |{state_str}⟩: {count:4d} times ({percentage:5.2f}%)")


def demonstrate_ghz_state():
    """Demonstrate GHZ state creation."""
    print_section("GHZ State (3-Qubit Entanglement) Demo")
    
    circuit = create_ghz_state(3)
    state = circuit.run()
    
    print("Circuit: H(0) → CNOT(0,1) → CNOT(1,2)")
    print(f"Final state vector: {state}")
    print(f"\nState decomposition:")
    for i, amplitude in enumerate(state):
        if np.abs(amplitude) > 1e-10:
            binary = format(i, '03b')
            print(f"   |{binary}⟩: {amplitude:.4f} (prob: {np.abs(amplitude)**2:.4f})")
    
    measurements = circuit.measure(shots=1000)
    print(f"\nMeasurement results (1000 shots):")
    for state_str, count in sorted(measurements.items(), key=lambda x: -x[1]):
        percentage = (count / 1000) * 100
        print(f"   |{state_str}⟩: {count:4d} times ({percentage:5.2f}%)")


def demonstrate_quantum_interference():
    """Demonstrate quantum interference."""
    print_section("Quantum Interference Demo")
    
    print("Circuit: H(0) → Z(0) → H(0)")
    circuit = QuantumCircuit(1)
    circuit.h(0)
    circuit.z(0)
    circuit.h(0)
    state = circuit.run()
    
    qubit = Qubit(state[0], state[1])
    print(f"State: {qubit}")
    print(f"Probabilities: P(0) = {qubit.probabilities()[0]:.4f}, P(1) = {qubit.probabilities()[1]:.4f}")
    print("\nResult: The qubit is in state |1⟩ due to interference!")


def demonstrate_circuit_optimization():
    """Demonstrate circuit optimization."""
    print_section("Circuit Optimization Demo")
    
    print("Original circuit: X → X → H → H → Y → Y")
    circuit = QuantumCircuit(1)
    circuit.x(0)
    circuit.x(0)  # These cancel
    circuit.h(0)
    circuit.h(0)  # These cancel
    circuit.y(0)
    circuit.y(0)  # These cancel
    
    print(f"Original gate count: {len(circuit.gates)}")
    print(f"Original depth: {circuit.optimizer.calculate_circuit_depth(circuit.gates)}")
    
    # Run with optimization
    state = circuit.run(optimize=True)
    
    print(f"\nAfter optimization:")
    print(f"All gates canceled - final state: {state}")
    print(f"State should be |0⟩: {np.allclose(state, [1, 0])}")


def demonstrate_custom_circuit():
    """Demonstrate a custom quantum circuit."""
    print_section("Custom Circuit Demo: Quantum Fourier Transform (2 qubits)")
    
    circuit = QuantumCircuit(2)
    
    # Simplified 2-qubit QFT
    circuit.h(0)
    circuit.rz(0, np.pi / 2)
    circuit.cnot(1, 0)
    circuit.rz(0, -np.pi / 2)
    circuit.cnot(1, 0)
    circuit.h(1)
    
    state = circuit.run()
    
    print("State decomposition:")
    for i, amplitude in enumerate(state):
        binary = format(i, '02b')
        prob = np.abs(amplitude)**2
        if prob > 1e-10:
            print(f"   |{binary}⟩: {amplitude:.4f} (prob: {prob:.4f})")
    
    measurements = circuit.measure(shots=1000)
    print(f"\nMeasurement results (1000 shots):")
    for state_str, count in sorted(measurements.items(), key=lambda x: -x[1]):
        percentage = (count / 1000) * 100
        print(f"   |{state_str}⟩: {count:4d} times ({percentage:5.2f}%)")
    
    # Circuit info
    info = circuit.get_circuit_info()
    print(f"\nCircuit Info:")
    print(f"   Qubits: {info['n_qubits']}")
    print(f"   Gates: {info['n_gates']}")
    print(f"   Depth: {info['depth']}")
    print(f"   Using sparse matrices: {info['use_sparse']}")


def main():
    """Run all demonstrations."""
    print("\n" + "█" * 60)
    print("█" + " " * 58 + "█")
    print("█" + "  QSimulateX - Quantum Computing Simulator Demo".center(58) + "█")
    print("█" + " " * 58 + "█")
    print("█" * 60)
    
    try:
        demonstrate_single_qubit_gates()
        demonstrate_bell_state()
        demonstrate_ghz_state()
        demonstrate_quantum_interference()
        demonstrate_circuit_optimization()
        demonstrate_custom_circuit()
        
        print_section("Demo Complete!")
        print("✓ All demonstrations completed successfully!")
        print("\nNext steps:")
        print("  1. Start the FastAPI backend: python -m quantum_simulator.api")
        print("  2. Start the web UI: cd web-ui && npm install && npm run dev")
        print("  3. Open http://localhost:3000 in your browser")
        
    except Exception as e:
        print(f"\n❌ Error during demo: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
