import React, { useRef, useState } from 'react';
import { useFrame } from '@react-three/fiber';
import { Html } from '@react-three/drei';
import { buttonStyle } from './styles';

const Echo = ({ agent, position, color = 'cyan', isSelected, onSelect, onCommand }) => {
  const meshRef = useRef();
  const [isHovered, setIsHovered] = useState(false);

  // Add a subtle bobbing animation
  useFrame((state) => {
    if (meshRef.current) {
      const t = state.clock.getElapsedTime();
      meshRef.current.position.y = position[1] + Math.sin(t * 2) * 0.1;
      meshRef.current.scale.setScalar(isHovered ? 1.5 : 1);
    }
  });

  return (
    <mesh
      ref={meshRef}
      position={position}
      onPointerOver={(e) => { e.stopPropagation(); setIsHovered(true); }}
      onPointerOut={(e) => setIsHovered(false)}
      onClick={(e) => { e.stopPropagation(); onSelect(agent.id); }}
    >
      <sphereGeometry args={[0.3, 32, 32]} />
      <meshStandardMaterial
        color={isSelected ? 'white' : color}
        emissive={isSelected ? 'white' : color}
        emissiveIntensity={isHovered ? 1.2 : 0.8}
        toneMapped={false}
      />
      {isSelected && (
        <Html distanceFactor={10}>
          <div style={{
            padding: '8px 12px',
            background: 'rgba(0, 0, 0, 0.7)',
            color: 'white',
            borderRadius: '4px',
            border: '1px solid white',
            whiteSpace: 'nowrap',
            transform: 'translate(-50%, -150%)', // Position it above the echo
          }}>
                        <div><strong>{agent.name}</strong></div>
            <div>Status: {agent.status}</div>
            <div style={{ marginTop: '8px', display: 'flex', gap: '8px' }}>
              <button 
                onClick={(e) => { e.stopPropagation(); onCommand(agent.id, 'stop'); }} 
                style={buttonStyle}
              >
                Stop
              </button>
              <button 
                onClick={(e) => { e.stopPropagation(); onCommand(agent.id, 'restart'); }} 
                style={buttonStyle}
              >
                Restart
              </button>
            </div>
          </div>
        </Html>
      )}
    </mesh>
  );
};

export default Echo;
