"""
Comprehensive test suite to verify scientific correctness of quantum simulator.
Tests against known quantum mechanics results.
"""
import numpy as np
from quantum_simulator import QuantumCircuit, create_bell_state, create_ghz_state
from quantum_simulator.qubit import Qubit
from quantum_simulator.gates import (
    pauli_x, pauli_y, pauli_z, hadamard, cnot, 
    apply_single_qubit_gate
)


class TestResults:
    """Track test results."""
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.tests = []
    
    def assert_close(self, actual, expected, tolerance=1e-10, test_name="Test"):
        """Check if values are close within tolerance."""
        if isinstance(actual, np.ndarray):
            close = np.allclose(actual, expected, atol=tolerance)
        else:
            close = abs(actual - expected) < tolerance
        
        if close:
            self.passed += 1
            self.tests.append((test_name, "✓ PASS", None))
            print(f"  ✓ {test_name}")
        else:
            self.failed += 1
            self.tests.append((test_name, "✗ FAIL", f"Expected {expected}, got {actual}"))
            print(f"  ✗ {test_name}")
            print(f"    Expected: {expected}")
            print(f"    Got:      {actual}")
        
        return close
    
    def summary(self):
        """Print summary."""
        total = self.passed + self.failed
        print("\n" + "="*60)
        print("TEST SUMMARY")
        print("="*60)
        print(f"Total Tests: {total}")
        print(f"Passed:      {self.passed} ({100*self.passed/total:.1f}%)")
        print(f"Failed:      {self.failed} ({100*self.failed/total:.1f}%)")
        if self.failed == 0:
            print("\n✅ ALL TESTS PASSED - Quantum simulator is scientifically correct!")
        else:
            print(f"\n⚠️  {self.failed} test(s) failed - Review failures above")
        print("="*60)


def test_basic_gates(results):
    """Test basic quantum gates produce correct results."""
    print("\n[1] Testing Basic Quantum Gates...")
    
    # Test 1: Pauli-X on |0⟩ should give |1⟩
    circuit = QuantumCircuit(1)
    circuit.x(0)
    state = circuit.run()
    expected = np.array([0, 1], dtype=complex)
    results.assert_close(state, expected, test_name="Pauli-X: X|0⟩ = |1⟩")
    
    # Test 2: Pauli-X on |1⟩ should give |0⟩ (double application)
    circuit = QuantumCircuit(1)
    circuit.x(0)
    circuit.x(0)
    state = circuit.run()
    expected = np.array([1, 0], dtype=complex)
    results.assert_close(state, expected, test_name="Pauli-X: XX|0⟩ = |0⟩")
    
    # Test 3: Hadamard on |0⟩ should give (|0⟩+|1⟩)/√2
    circuit = QuantumCircuit(1)
    circuit.h(0)
    state = circuit.run()
    expected = np.array([1/np.sqrt(2), 1/np.sqrt(2)], dtype=complex)
    results.assert_close(state, expected, test_name="Hadamard: H|0⟩ = |+⟩")
    
    # Test 4: Hadamard twice should return to |0⟩
    circuit = QuantumCircuit(1)
    circuit.h(0)
    circuit.h(0)
    state = circuit.run()
    expected = np.array([1, 0], dtype=complex)
    results.assert_close(state, expected, test_name="Hadamard: HH|0⟩ = |0⟩")
    
    # Test 5: Pauli-Z on |0⟩ should give |0⟩
    circuit = QuantumCircuit(1)
    circuit.z(0)
    state = circuit.run()
    expected = np.array([1, 0], dtype=complex)
    results.assert_close(state, expected, test_name="Pauli-Z: Z|0⟩ = |0⟩")
    
    # Test 6: Pauli-Z on |1⟩ should give -|1⟩
    circuit = QuantumCircuit(1)
    circuit.x(0)  # Create |1⟩
    circuit.z(0)  # Apply Z
    state = circuit.run()
    expected = np.array([0, -1], dtype=complex)
    results.assert_close(state, expected, test_name="Pauli-Z: Z|1⟩ = -|1⟩")


def test_superposition(results):
    """Test superposition states."""
    print("\n[2] Testing Superposition States...")
    
    # Test 1: |+⟩ state should have equal probabilities
    circuit = QuantumCircuit(1)
    circuit.h(0)
    state = circuit.run()
    probs = circuit.get_probabilities()
    results.assert_close(probs[0], 0.5, test_name="|+⟩ state: P(0) = 0.5")
    results.assert_close(probs[1], 0.5, test_name="|+⟩ state: P(1) = 0.5")
    
    # Test 2: State normalization
    norm = np.sum(probs)
    results.assert_close(norm, 1.0, test_name="Probability normalization = 1")


def test_bell_state(results):
    """Test Bell state (entanglement)."""
    print("\n[3] Testing Bell State (Entanglement)...")
    
    circuit = create_bell_state()
    state = circuit.run()
    
    # Bell state should be (|00⟩ + |11⟩)/√2
    expected = np.array([1/np.sqrt(2), 0, 0, 1/np.sqrt(2)], dtype=complex)
    results.assert_close(state, expected, test_name="Bell state: (|00⟩+|11⟩)/√2")
    
    # Check probabilities
    probs = circuit.get_probabilities()
    results.assert_close(probs[0], 0.5, test_name="Bell: P(|00⟩) = 0.5")
    results.assert_close(probs[3], 0.5, test_name="Bell: P(|11⟩) = 0.5")
    results.assert_close(probs[1], 0.0, test_name="Bell: P(|01⟩) = 0.0")
    results.assert_close(probs[2], 0.0, test_name="Bell: P(|10⟩) = 0.0")


def test_ghz_state(results):
    """Test GHZ state (3-qubit entanglement)."""
    print("\n[4] Testing GHZ State (3-qubit)...")
    
    circuit = create_ghz_state(3)
    state = circuit.run()
    
    # GHZ state should be (|000⟩ + |111⟩)/√2
    expected = np.zeros(8, dtype=complex)
    expected[0] = 1/np.sqrt(2)  # |000⟩
    expected[7] = 1/np.sqrt(2)  # |111⟩
    results.assert_close(state, expected, test_name="GHZ: (|000⟩+|111⟩)/√2")
    
    probs = circuit.get_probabilities()
    results.assert_close(probs[0], 0.5, test_name="GHZ: P(|000⟩) = 0.5")
    results.assert_close(probs[7], 0.5, test_name="GHZ: P(|111⟩) = 0.5")


def test_bloch_sphere(results):
    """Test Bloch sphere coordinates."""
    print("\n[5] Testing Bloch Sphere Coordinates...")
    
    # Test 1: |0⟩ at north pole (0, 0, 1)
    qubit = Qubit.zero()
    x, y, z = qubit.get_bloch_vector()
    results.assert_close(x, 0.0, test_name="Bloch |0⟩: x = 0")
    results.assert_close(y, 0.0, test_name="Bloch |0⟩: y = 0")
    results.assert_close(z, 1.0, test_name="Bloch |0⟩: z = 1")
    
    # Test 2: |1⟩ at south pole (0, 0, -1)
    qubit = Qubit.one()
    x, y, z = qubit.get_bloch_vector()
    results.assert_close(x, 0.0, test_name="Bloch |1⟩: x = 0")
    results.assert_close(y, 0.0, test_name="Bloch |1⟩: y = 0")
    results.assert_close(z, -1.0, test_name="Bloch |1⟩: z = -1")
    
    # Test 3: |+⟩ at x-axis (1, 0, 0)
    qubit = Qubit.plus()
    x, y, z = qubit.get_bloch_vector()
    results.assert_close(x, 1.0, test_name="Bloch |+⟩: x = 1")
    results.assert_close(y, 0.0, test_name="Bloch |+⟩: y = 0")
    results.assert_close(z, 0.0, test_name="Bloch |+⟩: z = 0")
    
    # Test 4: |−⟩ at negative x-axis (-1, 0, 0)
    qubit = Qubit.minus()
    x, y, z = qubit.get_bloch_vector()
    results.assert_close(x, -1.0, test_name="Bloch |−⟩: x = -1")
    results.assert_close(y, 0.0, test_name="Bloch |−⟩: y = 0")
    results.assert_close(z, 0.0, test_name="Bloch |−⟩: z = 0")


def test_rotation_gates(results):
    """Test rotation gates."""
    print("\n[6] Testing Rotation Gates...")
    
    # Test 1: RY(π/2) on |0⟩ should give (|0⟩+|1⟩)/√2
    circuit = QuantumCircuit(1)
    circuit.ry(0, np.pi/2)
    state = circuit.run()
    expected = np.array([1/np.sqrt(2), 1/np.sqrt(2)], dtype=complex)
    results.assert_close(state, expected, test_name="RY(π/2)|0⟩ = (|0⟩+|1⟩)/√2")
    
    # Test 2: RX(π) should be equivalent to X
    circuit = QuantumCircuit(1)
    circuit.rx(0, np.pi)
    state = circuit.run()
    # RX(π) = -iX, so should have phase factor
    expected_magnitude = np.array([0, 1])
    results.assert_close(np.abs(state), expected_magnitude, 
                        test_name="RX(π) magnitude = X")
    
    # Test 3: RZ doesn't change |0⟩ magnitude
    circuit = QuantumCircuit(1)
    circuit.rz(0, np.pi/4)
    state = circuit.run()
    probs = np.abs(state)**2
    results.assert_close(probs[0], 1.0, test_name="RZ preserves |0⟩")


def test_unitarity(results):
    """Test that gates are unitary (preserve norm)."""
    print("\n[7] Testing Unitarity (Norm Preservation)...")
    
    # Test various gate sequences preserve normalization
    test_circuits = [
        ("H", lambda c: c.h(0)),
        ("X-Y-Z", lambda c: (c.x(0), c.y(0), c.z(0))),
        ("H-T-H", lambda c: (c.h(0), c.t(0), c.h(0))),
        ("RY(0.7)", lambda c: c.ry(0, 0.7)),
    ]
    
    for name, builder in test_circuits:
        circuit = QuantumCircuit(1)
        builder(circuit)
        state = circuit.run()
        norm = np.linalg.norm(state)
        results.assert_close(norm, 1.0, test_name=f"Unitarity: {name} preserves norm")


def test_quantum_interference(results):
    """Test quantum interference effects."""
    print("\n[8] Testing Quantum Interference...")
    
    # Test: H-Z-H should give |1⟩ (due to interference)
    circuit = QuantumCircuit(1)
    circuit.h(0)
    circuit.z(0)
    circuit.h(0)
    state = circuit.run()
    expected = np.array([0, 1], dtype=complex)
    results.assert_close(state, expected, test_name="H-Z-H interference = |1⟩")
    
    # Test: H-X-H should give |1⟩
    circuit = QuantumCircuit(1)
    circuit.h(0)
    circuit.x(0)
    circuit.h(0)
    state = circuit.run()
    expected = np.array([0, 1], dtype=complex)
    results.assert_close(state, expected, test_name="H-X-H = |1⟩")


def test_cnot_gate(results):
    """Test CNOT gate behavior."""
    print("\n[9] Testing CNOT Gate...")
    
    # Test 1: CNOT|00⟩ = |00⟩
    circuit = QuantumCircuit(2)
    circuit.cnot(0, 1)
    state = circuit.run()
    expected = np.array([1, 0, 0, 0], dtype=complex)
    results.assert_close(state, expected, test_name="CNOT|00⟩ = |00⟩")
    
    # Test 2: CNOT|10⟩ = |11⟩
    circuit = QuantumCircuit(2)
    circuit.x(0)  # Create |10⟩
    circuit.cnot(0, 1)
    state = circuit.run()
    expected = np.array([0, 0, 0, 1], dtype=complex)
    results.assert_close(state, expected, test_name="CNOT|10⟩ = |11⟩")
    
    # Test 3: CNOT|01⟩ = |01⟩
    circuit = QuantumCircuit(2)
    circuit.x(1)  # Create |01⟩
    circuit.cnot(0, 1)
    state = circuit.run()
    expected = np.array([0, 1, 0, 0], dtype=complex)
    results.assert_close(state, expected, test_name="CNOT|01⟩ = |01⟩")
    
    # Test 4: CNOT|11⟩ = |10⟩
    circuit = QuantumCircuit(2)
    circuit.x(0)
    circuit.x(1)  # Create |11⟩
    circuit.cnot(0, 1)
    state = circuit.run()
    expected = np.array([0, 0, 1, 0], dtype=complex)
    results.assert_close(state, expected, test_name="CNOT|11⟩ = |10⟩")


def test_measurement_statistics(results):
    """Test measurement statistics match probabilities."""
    print("\n[10] Testing Measurement Statistics...")
    
    # Create superposition
    circuit = QuantumCircuit(1)
    circuit.h(0)
    circuit.run()
    
    # Measure many times
    measurements = circuit.measure(shots=10000)
    
    # Count outcomes
    count_0 = measurements.get('0', 0)
    count_1 = measurements.get('1', 0)
    
    # Should be approximately 50/50 (within statistical tolerance)
    measured_prob_0 = count_0 / 10000
    measured_prob_1 = count_1 / 10000
    
    # Use larger tolerance for statistical variation
    results.assert_close(measured_prob_0, 0.5, tolerance=0.05,
                        test_name="Measurement: P(0) ≈ 0.5 (±5%)")
    results.assert_close(measured_prob_1, 0.5, tolerance=0.05,
                        test_name="Measurement: P(1) ≈ 0.5 (±5%)")


def test_commutation_relations(results):
    """Test quantum gate commutation relations."""
    print("\n[11] Testing Commutation Relations...")
    
    # Test: [X, Z] ≠ 0 (anti-commute)
    circuit1 = QuantumCircuit(1)
    circuit1.x(0)
    circuit1.z(0)
    state1 = circuit1.run()
    
    circuit2 = QuantumCircuit(1)
    circuit2.z(0)
    circuit2.x(0)
    state2 = circuit2.run()
    
    # These should be different (they anti-commute)
    different = not np.allclose(state1, state2)
    if different:
        results.passed += 1
        results.tests.append(("X and Z anti-commute", "✓ PASS", None))
        print("  ✓ X and Z anti-commute")
    else:
        results.failed += 1
        print("  ✗ X and Z should anti-commute")


def test_circuit_optimization(results):
    """Test that circuit optimization preserves results."""
    print("\n[12] Testing Circuit Optimization...")
    
    # Create circuit with canceling gates
    circuit = QuantumCircuit(1)
    circuit.h(0)
    circuit.x(0)
    circuit.x(0)  # Should cancel
    circuit.h(0)  # Should cancel with first H
    
    state_unoptimized = circuit.run(optimize=False)
    state_optimized = circuit.run(optimize=True)
    
    results.assert_close(state_optimized, state_unoptimized,
                        test_name="Optimization preserves circuit output")


def main():
    """Run all tests."""
    print("="*60)
    print("QUANTUM SIMULATOR CORRECTNESS TESTS")
    print("Testing against known quantum mechanics results")
    print("="*60)
    
    results = TestResults()
    
    try:
        test_basic_gates(results)
        test_superposition(results)
        test_bell_state(results)
        test_ghz_state(results)
        test_bloch_sphere(results)
        test_rotation_gates(results)
        test_unitarity(results)
        test_quantum_interference(results)
        test_cnot_gate(results)
        test_measurement_statistics(results)
        test_commutation_relations(results)
        test_circuit_optimization(results)
        
    except Exception as e:
        print(f"\n❌ Test execution error: {e}")
        import traceback
        traceback.print_exc()
    
    results.summary()
    
    return results.failed == 0


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
