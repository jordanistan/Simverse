import React from 'react';
import { Canvas } from '@react-three/fiber';
import Scene from './components/Scene';
import './App.css';

function App() {
  return (
    <div id="simverse-container">
      <Canvas camera={{ position: [0, 5, 20], fov: 75 }}>
        <Scene />
      </Canvas>
    </div>
  );
}

export default App;
