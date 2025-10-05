"""
Tree-based circuit optimization.
"""
import numpy as np
from typing import List, Tuple, Dict, Any
from dataclasses import dataclass


@dataclass
class GateNode:
    """Represents a gate in the circuit tree."""
    gate_name: str
    qubits: List[int]
    params: Dict[str, Any]
    depth: int = 0


class CircuitOptimizer:
    """Optimizes quantum circuits using various techniques."""
    
    def __init__(self):
        self.optimization_rules = self._build_rules()
    
    def _build_rules(self) -> Dict[str, callable]:
        """Build optimization rules."""
        return {
            'cancel_inverse': self._cancel_inverse_gates,
            'merge_rotations': self._merge_rotation_gates,
            'commute_gates': self._commute_gates,
        }
    
    def optimize(self, gates: List[GateNode], rules: List[str] = None) -> List[GateNode]:
        """
        Optimize a circuit.
        
        Args:
            gates: List of gate nodes
            rules: List of optimization rule names to apply (None = all)
        
        Returns:
            Optimized gate list
        """
        if rules is None:
            rules = list(self.optimization_rules.keys())
        
        optimized = gates.copy()
        
        for rule_name in rules:
            if rule_name in self.optimization_rules:
                optimized = self.optimization_rules[rule_name](optimized)
        
        return optimized
    
    def _cancel_inverse_gates(self, gates: List[GateNode]) -> List[GateNode]:
        """Cancel pairs of inverse gates (e.g., X-X, H-H)."""
        inverse_pairs = {
            'X': 'X',
            'Y': 'Y',
            'Z': 'Z',
            'H': 'H',
            'CNOT': 'CNOT',
        }
        
        optimized = []
        i = 0
        
        while i < len(gates):
            gate = gates[i]
            
            # Check if next gate is inverse
            if (i + 1 < len(gates) and 
                gate.gate_name in inverse_pairs and
                gates[i + 1].gate_name == inverse_pairs[gate.gate_name] and
                gate.qubits == gates[i + 1].qubits):
                # Skip both gates
                i += 2
            else:
                optimized.append(gate)
                i += 1
        
        return optimized
    
    def _merge_rotation_gates(self, gates: List[GateNode]) -> List[GateNode]:
        """Merge consecutive rotation gates on the same qubit."""
        rotation_gates = {'RX', 'RY', 'RZ'}
        
        optimized = []
        i = 0
        
        while i < len(gates):
            gate = gates[i]
            
            # Check if this is a rotation gate
            if gate.gate_name in rotation_gates and len(gate.qubits) == 1:
                # Look for consecutive rotations on same qubit and axis
                total_angle = gate.params.get('theta', 0)
                j = i + 1
                
                while (j < len(gates) and 
                       gates[j].gate_name == gate.gate_name and
                       gates[j].qubits == gate.qubits):
                    total_angle += gates[j].params.get('theta', 0)
                    j += 1
                
                # Add merged gate
                if abs(total_angle % (2 * np.pi)) > 1e-10:  # Skip if trivial
                    merged_gate = GateNode(
                        gate_name=gate.gate_name,
                        qubits=gate.qubits,
                        params={'theta': total_angle % (2 * np.pi)},
                        depth=gate.depth
                    )
                    optimized.append(merged_gate)
                
                i = j
            else:
                optimized.append(gate)
                i += 1
        
        return optimized
    
    def _commute_gates(self, gates: List[GateNode]) -> List[GateNode]:
        """Commute gates to reduce circuit depth."""
        # This is a simplified version that checks if gates act on disjoint qubits
        optimized = gates.copy()
        
        # Sort gates by depth, then try to reduce depth where possible
        changed = True
        while changed:
            changed = False
            for i in range(len(optimized) - 1):
                gate1 = optimized[i]
                gate2 = optimized[i + 1]
                
                # Check if gates act on disjoint qubits
                if set(gate1.qubits).isdisjoint(set(gate2.qubits)):
                    # They can be parallelized
                    if gate2.depth > gate1.depth:
                        gate2.depth = gate1.depth
                        changed = True
        
        return optimized
    
    def calculate_circuit_depth(self, gates: List[GateNode]) -> int:
        """Calculate the depth of a circuit."""
        if not gates:
            return 0
        
        # Track the depth for each qubit
        qubit_depths = {}
        
        for gate in gates:
            # Find max depth of qubits this gate acts on
            max_depth = 0
            for qubit in gate.qubits:
                if qubit in qubit_depths:
                    max_depth = max(max_depth, qubit_depths[qubit])
            
            # Update depth for all qubits
            new_depth = max_depth + 1
            for qubit in gate.qubits:
                qubit_depths[qubit] = new_depth
        
        return max(qubit_depths.values())
    
    def estimate_gate_count(self, gates: List[GateNode]) -> Dict[str, int]:
        """Count gates by type."""
        counts = {}
        for gate in gates:
            counts[gate.gate_name] = counts.get(gate.gate_name, 0) + 1
        return counts
