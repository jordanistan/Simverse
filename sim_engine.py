# sim_engine.py

import time
from threading import Thread, Lock

import docker_bridge as docker
import db

class SimEngine:
    """
    Manages the lifecycle of all agents (Echoes) in the Simverse.
    It runs a background thread to keep the database in sync with Docker.
    """

    def __init__(self, db_session):
        """Initializes the simulation engine.

        Args:
            db_session: An active SQLAlchemy session.
        """
        self.db_session = db_session
        self.is_running = False
        self.lock = Lock()
        self.docker_client = docker.get_docker_client() # Force immediate initialization
        self._sync_thread = Thread(target=self._periodic_sync, daemon=True)

    def start(self):
        """Starts the engine's background synchronization thread."""
        if not self.is_running:
            print("--- Simulation Engine starting ---")
            if self.docker_client:
                print("--- Docker client confirmed. Starting sync thread. ---")
                self.is_running = True
                self._sync_thread.start()
                print("--- Simulation Engine is running ---")
            else:
                print("--- FATAL: Could not get Docker client. SimEngine will not run. ---")

    def stop(self):
        """Stops the engine's background thread."""
        if self.is_running:
            print("--- Simulation Engine stopping ---")
            self.is_running = False
            if self._sync_thread.is_alive():
                self._sync_thread.join()
            print("--- Simulation Engine has stopped ---")

    def _periodic_sync(self):
        """The main loop for the background thread."""
        while self.is_running:
            print("SimEngine: Running periodic sync...")
            self.sync_agents_with_docker()
            time.sleep(10)  # Sync every 10 seconds

    def sync_agents_with_docker(self):
        """Fetches all Docker containers and updates their state in the database."""
        with self.lock:
            print("SimEngine: Acquiring lock and syncing agents.")
            try:
                all_containers = docker.get_all_containers()
                # The get_all_containers function returns None on error, so we check for that.
                all_containers = docker.get_all_containers()
                db.sync_containers_with_db(self.db_session, all_containers)
                if all_containers is not None:
                    print(f"SimEngine: Synced {len(all_containers)} containers.")
            except docker.errors.APIError as e:
                print(f"SimEngine: Docker API error during sync: {e}")
            except Exception as e:
                # Catching other potential errors, e.g., from the DB layer
                print(f"SimEngine: An unexpected error occurred during sync: {e}")

    def create_new_agent(self, name, image="hello-world"):
        """Creates a new agent (Docker container).

        Args:
            name (str): The name for the new agent.
            image (str): The Docker image to use.

        Returns:
            A tuple (success, message_or_id).
        """
        with self.lock:
            print(f"SimEngine: Creating agent '{name}' from image '{image}'.")
            success, result = docker.create_agent(name, image)
            if success:
                # After creation, trigger an immediate sync to update the DB
                self.sync_agents_with_docker()
            return success, result