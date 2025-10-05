"""Quick verification of key quantum simulator results."""
import numpy as np
from quantum_simulator import QuantumCircuit, create_bell_state, create_ghz_state
from quantum_simulator.qubit import Qubit

print("="*70)
print("QUANTUM SIMULATOR VERIFICATION - Key Tests")
print("="*70)

def test_result(name, actual, expected, tolerance=1e-10):
    """Test and print result."""
    if isinstance(actual, np.ndarray):
        match = np.allclose(actual, expected, atol=tolerance)
    elif isinstance(actual, tuple) or isinstance(expected, tuple):
        # Convert tuples to arrays for comparison
        actual_arr = np.array(actual)
        expected_arr = np.array(expected)
        match = np.allclose(actual_arr, expected_arr, atol=tolerance)
    else:
        match = abs(actual - expected) < tolerance
    
    status = "✓ PASS" if match else "✗ FAIL"
    print(f"{status} | {name}")
    if not match:
        print(f"       Expected: {expected}")
        print(f"       Got:      {actual}")
    return match

passed = 0
failed = 0

# Test 1: Hadamard creates superposition
print("\n[Test 1] Hadamard Gate H|0⟩ = (|0⟩+|1⟩)/√2")
circuit = QuantumCircuit(1)
circuit.h(0)
state = circuit.run()
expected = np.array([1/np.sqrt(2), 1/np.sqrt(2)])
if test_result("  State vector", state, expected):
    passed += 1
else:
    failed += 1

probs = circuit.get_probabilities()
if test_result("  P(0) = 0.5", probs[0], 0.5):
    passed += 1
else:
    failed += 1
if test_result("  P(1) = 0.5", probs[1], 0.5):
    passed += 1
else:
    failed += 1

# Test 2: Pauli-X flips state
print("\n[Test 2] Pauli-X (NOT) Gate X|0⟩ = |1⟩")
circuit = QuantumCircuit(1)
circuit.x(0)
state = circuit.run()
expected = np.array([0, 1])
if test_result("  State vector", state, expected):
    passed += 1
else:
    failed += 1

# Test 3: Bell State (Entanglement)
print("\n[Test 3] Bell State: (|00⟩+|11⟩)/√2")
circuit = create_bell_state()
state = circuit.run()
expected = np.array([1/np.sqrt(2), 0, 0, 1/np.sqrt(2)])
if test_result("  State vector", state, expected):
    passed += 1
else:
    failed += 1

probs = circuit.get_probabilities()
if test_result("  P(|00⟩) = 0.5", probs[0], 0.5):
    passed += 1
else:
    failed += 1
if test_result("  P(|11⟩) = 0.5", probs[3], 0.5):
    passed += 1
else:
    failed += 1
if test_result("  P(|01⟩) = 0", probs[1], 0.0):
    passed += 1
else:
    failed += 1

# Test 4: GHZ State (3-qubit entanglement)
print("\n[Test 4] GHZ State: (|000⟩+|111⟩)/√2")
circuit = create_ghz_state(3)
state = circuit.run()
expected = np.zeros(8)
expected[0] = 1/np.sqrt(2)
expected[7] = 1/np.sqrt(2)
if test_result("  State vector", state, expected):
    passed += 1
else:
    failed += 1

# Test 5: Bloch Sphere Coordinates
print("\n[Test 5] Bloch Sphere Coordinates")
qubit_zero = Qubit.zero()
x, y, z = qubit_zero.get_bloch_vector()
if test_result("  |0⟩ at north pole: (0,0,1)", (x, y, z), (0, 0, 1)):
    passed += 1
else:
    failed += 1

qubit_one = Qubit.one()
x, y, z = qubit_one.get_bloch_vector()
if test_result("  |1⟩ at south pole: (0,0,-1)", (x, y, z), (0, 0, -1)):
    passed += 1
else:
    failed += 1

qubit_plus = Qubit.plus()
x, y, z = qubit_plus.get_bloch_vector()
if test_result("  |+⟩ on x-axis: (1,0,0)", (x, y, z), (1, 0, 0)):
    passed += 1
else:
    failed += 1

# Test 6: Quantum Interference H-Z-H = |1⟩
print("\n[Test 6] Quantum Interference: H-Z-H|0⟩ = |1⟩")
circuit = QuantumCircuit(1)
circuit.h(0)
circuit.z(0)
circuit.h(0)
state = circuit.run()
expected = np.array([0, 1])
if test_result("  State vector", state, expected):
    passed += 1
else:
    failed += 1

# Test 7: CNOT Gate Truth Table
print("\n[Test 7] CNOT Gate Truth Table")
# CNOT|00⟩ = |00⟩
circuit = QuantumCircuit(2)
circuit.cnot(0, 1)
state = circuit.run()
if test_result("  CNOT|00⟩ = |00⟩", state, np.array([1, 0, 0, 0])):
    passed += 1
else:
    failed += 1

# CNOT|10⟩ = |11⟩
circuit = QuantumCircuit(2)
circuit.x(0)
circuit.cnot(0, 1)
state = circuit.run()
if test_result("  CNOT|10⟩ = |11⟩", state, np.array([0, 0, 0, 1])):
    passed += 1
else:
    failed += 1

# Test 8: Unitarity (norm preservation)
print("\n[Test 8] Unitarity - Gates Preserve Norm")
circuit = QuantumCircuit(1)
circuit.h(0)
circuit.t(0)
circuit.s(0)
state = circuit.run()
norm = np.linalg.norm(state)
if test_result("  ||ψ|| = 1", norm, 1.0):
    passed += 1
else:
    failed += 1

# Test 9: Rotation Gate RY(π/2)
print("\n[Test 9] Rotation Gate RY(π/2)|0⟩ = (|0⟩+|1⟩)/√2")
circuit = QuantumCircuit(1)
circuit.ry(0, np.pi/2)
state = circuit.run()
expected = np.array([1/np.sqrt(2), 1/np.sqrt(2)])
if test_result("  State vector", state, expected):
    passed += 1
else:
    failed += 1

# Test 10: Measurement Statistics
print("\n[Test 10] Measurement Statistics (10000 shots)")
circuit = QuantumCircuit(1)
circuit.h(0)
circuit.run()
measurements = circuit.measure(shots=10000)
count_0 = measurements.get('0', 0)
count_1 = measurements.get('1', 0)
prob_0 = count_0 / 10000
prob_1 = count_1 / 10000
print(f"       Measured: P(0)={prob_0:.3f}, P(1)={prob_1:.3f}")
if test_result("  P(0) ≈ 0.5 (±5%)", prob_0, 0.5, tolerance=0.05):
    passed += 1
else:
    failed += 1
if test_result("  P(1) ≈ 0.5 (±5%)", prob_1, 0.5, tolerance=0.05):
    passed += 1
else:
    failed += 1

# Summary
print("\n" + "="*70)
print("SUMMARY")
print("="*70)
total = passed + failed
print(f"Total Tests:  {total}")
print(f"Passed:       {passed} ({100*passed/total:.1f}%)")
print(f"Failed:       {failed}")

if failed == 0:
    print("\n✅ ALL TESTS PASSED!")
    print("The quantum simulator produces scientifically correct results!")
    print("\nVerified Properties:")
    print("  ✓ Correct quantum gate operations")
    print("  ✓ Proper superposition states")
    print("  ✓ Accurate entanglement (Bell & GHZ states)")
    print("  ✓ Correct Bloch sphere coordinates")
    print("  ✓ Quantum interference effects")
    print("  ✓ Proper CNOT gate behavior")
    print("  ✓ Unitarity (norm preservation)")
    print("  ✓ Accurate rotation gates")
    print("  ✓ Correct measurement statistics")
else:
    print(f"\n⚠️  {failed} test(s) failed - review above")

print("="*70)
