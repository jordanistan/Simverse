import React, { useState } from 'react';
import { Html } from '@react-three/drei';
import { buttonStyle, inputStyle } from './styles';

const AlphaNode = ({ position, onCreateAgent }) => {
  const [name, setName] = useState('');
  const [image, setImage] = useState('hello-world'); // Default image

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!name.trim()) {
      alert('Agent name is required.');
      return;
    }
    onCreateAgent(name, image);
    setName(''); // Reset form after submission
  };

  return (
    <group position={position}>
      <mesh>
        <octahedronGeometry args={[0.5, 0]} />
        <meshStandardMaterial 
          color="#4f46e5" 
          emissive="#6366f1"
          emissiveIntensity={1.5}
          toneMapped={false}
        />
      </mesh>
      <Html distanceFactor={10} center>
        <div style={{
          width: '250px',
          padding: '16px',
          background: 'rgba(17, 24, 39, 0.9)',
          color: 'white',
          borderRadius: '8px',
          border: '1px solid #4f46e5',
        }}>
          <h3 style={{ marginTop: 0, textAlign: 'center', color: '#a5b4fc' }}>Alpha Node</h3>
          <p style={{ fontSize: '12px', textAlign: 'center', color: '#9ca3af' }}>Create a new Echo</p>
          <form onSubmit={handleSubmit}>
            <input
              type="text"
              placeholder="Agent Name"
              value={name}
              onChange={(e) => setName(e.target.value)}
              style={inputStyle}
            />
            <input
              type="text"
              placeholder="Docker Image (e.g., alpine)"
              value={image}
              onChange={(e) => setImage(e.target.value)}
              style={inputStyle}
            />
            <button type="submit" style={{ ...buttonStyle, width: '100%', marginTop: '8px' }}>
              Create Echo
            </button>
          </form>
        </div>
      </Html>
    </group>
  );
};

export default AlphaNode;
