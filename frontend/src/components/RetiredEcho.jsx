import React, { useRef, useState } from 'react';
import { useFrame } from '@react-three/fiber';
import { Html } from '@react-three/drei';

const RetiredEcho = ({ agent, position }) => {
  const meshRef = useRef();
  const [isHovered, setIsHovered] = useState(false);

  useFrame(() => {
    if (meshRef.current) {
      meshRef.current.scale.setScalar(isHovered ? 1.2 : 1);
    }
  });

  return (
    <mesh
      ref={meshRef}
      position={position}
      onPointerOver={(e) => { e.stopPropagation(); setIsHovered(true); }}
      onPointerOut={(e) => setIsHovered(false)}
    >
      <sphereGeometry args={[0.25, 16, 16]} />
      <meshStandardMaterial
        color="#4b5563" // A muted grey
        emissive="#1f2937"
        emissiveIntensity={0.5}
        roughness={0.8}
        metalness={0.2}
        transparent
        opacity={0.6}
      />
      {isHovered && (
        <Html distanceFactor={8}>
          <div style={{
            padding: '4px 8px',
            background: 'rgba(0, 0, 0, 0.8)',
            color: '#9ca3af', // Lighter grey text
            borderRadius: '4px',
            whiteSpace: 'nowrap',
            transform: 'translate(-50%, -150%)',
            fontSize: '12px',
          }}>
            {agent.name} (Retired)
          </div>
        </Html>
      )}
    </mesh>
  );
};

export default RetiredEcho;
