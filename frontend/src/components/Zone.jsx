import React from 'react';
import { Text } from '@react-three/drei';

const Zone = ({ name, position, size = [10, 10] }) => {
  return (
    <group position={position}>
      <mesh rotation={[-Math.PI / 2, 0, 0]}>
        <planeGeometry args={size} />
        <meshStandardMaterial color="#3a3a3a" transparent opacity={0.6} />
      </mesh>
      <Text
        position={[0, 0.5, 0]}
        color="white"
        fontSize={0.6}
        anchorX="center"
        anchorY="middle"
        outlineColor="black"
        outlineWidth={0.02}
      >
        {name}
      </Text>
    </group>
  );
};

export default Zone;
