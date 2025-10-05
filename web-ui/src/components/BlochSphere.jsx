import React, { useRef, useEffect } from 'react';
import { Canvas, useFrame } from '@react-three/fiber';
import { OrbitControls, Sphere, Line, Text } from '@react-three/drei';
import * as THREE from 'three';

const BlochSphereVisualization = ({ x = 0, y = 0, z = 1 }) => {
  const stateVectorRef = useRef();

  // Normalize the vector
  const magnitude = Math.sqrt(x * x + y * y + z * z);
  const nx = magnitude > 0 ? x / magnitude : 0;
  const ny = magnitude > 0 ? y / magnitude : 0;
  const nz = magnitude > 0 ? z / magnitude : 1;

  return (
    <>
      {/* Main sphere */}
      <Sphere args={[1, 32, 32]}>
        <meshStandardMaterial
          color="#1e293b"
          transparent
          opacity={0.3}
          side={THREE.DoubleSide}
        />
      </Sphere>

      {/* Equator circle */}
      <Line
        points={Array.from({ length: 65 }, (_, i) => {
          const angle = (i / 64) * Math.PI * 2;
          return [Math.cos(angle), Math.sin(angle), 0];
        })}
        color="#4b5563"
        lineWidth={1}
      />

      {/* Meridian circles */}
      <Line
        points={Array.from({ length: 65 }, (_, i) => {
          const angle = (i / 64) * Math.PI * 2;
          return [Math.cos(angle), 0, Math.sin(angle)];
        })}
        color="#4b5563"
        lineWidth={1}
      />
      <Line
        points={Array.from({ length: 65 }, (_, i) => {
          const angle = (i / 64) * Math.PI * 2;
          return [0, Math.cos(angle), Math.sin(angle)];
        })}
        color="#4b5563"
        lineWidth={1}
      />

      {/* Axes */}
      {/* X-axis */}
      <Line points={[[-1.3, 0, 0], [1.3, 0, 0]]} color="#ef4444" lineWidth={2} />
      <Text position={[1.5, 0, 0]} fontSize={0.15} color="#ef4444">
        X
      </Text>

      {/* Y-axis */}
      <Line points={[[0, -1.3, 0], [0, 1.3, 0]]} color="#10b981" lineWidth={2} />
      <Text position={[0, 1.5, 0]} fontSize={0.15} color="#10b981">
        Y
      </Text>

      {/* Z-axis */}
      <Line points={[[0, 0, -1.3], [0, 0, 1.3]]} color="#3b82f6" lineWidth={2} />
      <Text position={[0, 0, 1.5]} fontSize={0.15} color="#3b82f6">
        |0⟩
      </Text>
      <Text position={[0, 0, -1.5]} fontSize={0.15} color="#3b82f6">
        |1⟩
      </Text>

      {/* State vector */}
      <Line
        points={[[0, 0, 0], [nx, ny, nz]]}
        color="#8b5cf6"
        lineWidth={4}
        ref={stateVectorRef}
      />

      {/* State vector endpoint */}
      <mesh position={[nx, ny, nz]}>
        <sphereGeometry args={[0.08, 16, 16]} />
        <meshStandardMaterial color="#8b5cf6" emissive="#8b5cf6" emissiveIntensity={0.5} />
      </mesh>

      {/* Projection onto XY plane */}
      <Line
        points={[[nx, ny, 0], [nx, ny, nz]]}
        color="#8b5cf6"
        lineWidth={1}
        opacity={0.3}
        transparent
        dashed
        dashSize={0.05}
        gapSize={0.05}
      />

      {/* Ambient light */}
      <ambientLight intensity={0.5} />
      <pointLight position={[10, 10, 10]} intensity={1} />
    </>
  );
};

const BlochSphere = ({ stateVector }) => {
  // Calculate Bloch vector from state vector
  let x = 0, y = 0, z = 1;

  if (stateVector && stateVector.length >= 2) {
    const alpha = stateVector[0];
    const beta = stateVector[1];

    // Bloch sphere coordinates
    x = 2 * (alpha.real * beta.real + alpha.imag * beta.imag);
    y = 2 * (alpha.real * beta.imag - alpha.imag * beta.real);
    z = alpha.real * alpha.real + alpha.imag * alpha.imag - 
        beta.real * beta.real - beta.imag * beta.imag;
  }

  return (
    <div className="bg-gray-900 rounded-lg p-6 shadow-xl">
      <h2 className="text-2xl font-bold text-white mb-4">Bloch Sphere</h2>
      
      {stateVector && stateVector.length >= 2 ? (
        <>
          <div style={{ height: '400px' }}>
            <Canvas camera={{ position: [2, 2, 2], fov: 50 }}>
              <BlochSphereVisualization x={x} y={y} z={z} />
              <OrbitControls enableDamping dampingFactor={0.05} />
            </Canvas>
          </div>

          <div className="mt-4 grid grid-cols-3 gap-4">
            <div className="bg-gray-800 p-3 rounded-lg">
              <p className="text-sm text-gray-400">X (Re⟨σx⟩)</p>
              <p className="text-xl font-bold text-red-400">{x.toFixed(4)}</p>
            </div>
            <div className="bg-gray-800 p-3 rounded-lg">
              <p className="text-sm text-gray-400">Y (Re⟨σy⟩)</p>
              <p className="text-xl font-bold text-green-400">{y.toFixed(4)}</p>
            </div>
            <div className="bg-gray-800 p-3 rounded-lg">
              <p className="text-sm text-gray-400">Z (Re⟨σz⟩)</p>
              <p className="text-xl font-bold text-blue-400">{z.toFixed(4)}</p>
            </div>
          </div>

          <div className="mt-4 bg-gray-800 p-4 rounded-lg">
            <p className="text-sm text-gray-400 mb-2">State Components</p>
            <div className="space-y-1 font-mono text-sm">
              <p className="text-white">
                α = {stateVector[0].real.toFixed(4)} + {stateVector[0].imag.toFixed(4)}i
              </p>
              <p className="text-white">
                β = {stateVector[1].real.toFixed(4)} + {stateVector[1].imag.toFixed(4)}i
              </p>
            </div>
          </div>
        </>
      ) : (
        <div className="h-64 flex items-center justify-center text-gray-400">
          <p>Run a single-qubit circuit to visualize the Bloch sphere</p>
        </div>
      )}
    </div>
  );
};

export default BlochSphere;
