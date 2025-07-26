import React, { useState, useEffect, useMemo } from 'react';
import { OrbitControls, Stars } from '@react-three/drei';
import useWebSocket from '../hooks/useWebSocket';
import Zone from './Zone';
import Echo from './Echo';
import RetiredEcho from './RetiredEcho';
import AlphaNode from './AlphaNode';

// Define the layout and properties of the zones
const ZONES_LAYOUT = {
  ALPHA_HALL: { name: 'Alpha Hall', position: [-6, 0, -6], color: '#3b82f6' },
  ECHO_PLAZA: { name: 'Echo Plaza', position: [6, 0, -6], color: '#22c55e' },
  DOCKER_CORE: { name: 'Docker Core', position: [-6, 0, 6], color: '#f97316' },
  OMEGA_GATE: { name: 'Omega Gate', position: [6, 0, 6], color: '#ef4444' },
  THE_VOID: { name: 'The Void', position: [0, 0, 0], color: '#6b7280' },
};

// Replicate the backend logic to assign agents to zones
const assignZone = (agentStatus) => {
  const status = agentStatus?.toLowerCase() || '';
  if (['created'].includes(status)) return 'ALPHA_HALL';
  if (['running', 'up'].includes(status)) return 'ECHO_PLAZA';
  if (['restarting', 'paused'].includes(status)) return 'DOCKER_CORE';
  if (['exited', 'dead', 'stopped'].includes(status)) return 'OMEGA_GATE';
  return 'THE_VOID';
};

const Scene = () => {
  const { data, sendMessage } = useWebSocket('ws://localhost:8502/ws');
  const [agents, setAgents] = useState([]);
  const [retiredAgents, setRetiredAgents] = useState([]);
  const [selectedAgentId, setSelectedAgentId] = useState(null);
  const [agentLogs, setAgentLogs] = useState({}); // Stores logs by agent ID

  const activeAgents = useMemo(() => agents.filter(a => a.active), [agents]);

  // Memoize agent positions so they don't jump around on every render
  const agentPositions = useMemo(() => {
    const positions = {};
    agents.forEach(agent => { // Use the main agents list for stable positioning
      const zoneKey = assignZone(agent.status);
      const zone = ZONES_LAYOUT[zoneKey];
      // Generate a stable, pseudo-random position based on the agent's ID to prevent jitter
      const idHashX = parseInt(agent.id.substring(0, 4), 16);
      const idHashZ = parseInt(agent.id.substring(4, 8), 16);
      const offsetX = (idHashX / 0xFFFF - 0.5) * 8;
      const offsetZ = (idHashZ / 0xFFFF - 0.5) * 8;

      positions[agent.id] = [
        zone.position[0] + offsetX,
        0.5,
        zone.position[2] + offsetZ
      ];
    });
    return positions;
  }, [agents]);

  useEffect(() => {
    if (!data) return;

    if (data.type === 'full_update' && data.agents) {
      setAgents(data.agents.filter(a => a.active));
      setRetiredAgents(data.agents.filter(a => !a.active));
    } else if (data.type === 'logs' && data.container_id) {
      setAgentLogs(prevLogs => ({
        ...prevLogs,
        [data.container_id]: data.logs || 'No logs received or an error occurred.',
      }));
    }
  }, [data]);

    const handleSelectAgent = (agentId) => {
    setSelectedAgentId(prevId => (prevId === agentId ? null : agentId));
  };

  const handleControlCommand = (container_id, action) => {
    console.log(`Sending command: ${action} to ${container_id.substring(0, 12)}`);
    sendMessage({ action, container_id });
  };

  const handleCreateAgent = (name, image) => {
    console.log(`Sending create_agent command: ${name}, ${image}`);
    sendMessage({ action: 'create_agent', name, image });
  };

  return (
    <>
      <color attach="background" args={['#1a1a1a']} />
      <ambientLight intensity={0.3} />
      <pointLight position={[0, 20, 20]} intensity={1.5} />
      <Stars radius={100} depth={50} count={5000} factor={4} saturation={0} fade speed={1} />

      {Object.values(ZONES_LAYOUT).map(zone => (
        <Zone key={zone.name} name={zone.name} position={zone.position} size={[10, 10]} />
      ))}

      {/* Render Active Echos */}
      {activeAgents.map(agent => {
        const zoneKey = assignZone(agent.status);
        const zone = ZONES_LAYOUT[zoneKey];
        const position = agentPositions[agent.id] || zone.position;

        return (
                    <Echo
            key={agent.id}
            agent={agent}
            position={position}
            color={zone.color}
            isSelected={selectedAgentId === agent.id}
            onSelect={handleSelectAgent}
            onCommand={handleControlCommand}
            logs={agentLogs[agent.id]}
          />
        );
      })}

      {/* Render Retired Echos in the Omega Gate */}
      {retiredAgents.map(agent => {
        const zone = ZONES_LAYOUT.OMEGA_GATE;
        const position = agentPositions[agent.id] || zone.position;
        return (
          <RetiredEcho 
            key={agent.id} 
            agent={agent} 
            position={position} 
          />
        );
      })}

      <AlphaNode 
        position={ZONES_LAYOUT.ALPHA_HALL.position} 
        onCreateAgent={handleCreateAgent} 
      />

      <OrbitControls />
    </>
  );
};

export default Scene;
