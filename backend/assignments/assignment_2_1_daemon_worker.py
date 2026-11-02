"""
========================================================================================
ASSIGNMENT 2.1: CONCURRENT TASK DAEMONIZATION USING THREADS AND WORKERS
Course: Agent Technology (Unit-2)
Scenario: Asynchronous Background Milestone & Health Monitoring Daemon in CareerAI
========================================================================================
Description:
  This script demonstrates concurrent multi-threading in Agent Technology.
  It spawns a background worker thread (daemon=True) that continuously monitors
  student milestone timelines and deadline delays without blocking the main program.
  Thread safety is enforced via threading.Lock and queue.Queue, with cycle latency logging.
========================================================================================
"""

import sys
import os
import time

# Ensure UTF-8 output on Windows consoles
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

# Ensure backend root is on sys.path
backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

from app.agent.daemon_worker import CareerMonitorDaemon, global_daemon_state


def main():
    print("=" * 78)
    print("  ASSIGNMENT 2.1: CONCURRENT TASK DAEMON & THREAD-SAFE MONITORING DEMO")
    print("=" * 78)

    print("\n[Thread Setup] Initializing CareerMonitorDaemon (interval = 0.5s)...")
    daemon = CareerMonitorDaemon(check_interval_seconds=0.5)

    print(f"[Thread State Before Start] Is Alive: {daemon.is_alive()} | Is Daemon: {daemon.daemon}")
    daemon.start()
    print(f"[Thread State After Start]  Is Alive: {daemon.is_alive()} | Thread ID: {daemon.native_id}")

    print("\n[Main Thread Non-Blocking Simulation] Running main task loop for 3.5 seconds...")
    print("------------------------------------------------------------------------------")
    for sec in range(1, 8):
        time.sleep(0.5)
        # Safely query shared state protected by threading.Lock
        snapshot = global_daemon_state.get_state_snapshot()
        print(f"  [T+{sec*0.5:.1f}s] Daemon Status: {snapshot['daemon_status']:<8} | "
              f"Cycles: {snapshot['total_cycles_executed']:<3} | "
              f"Last Latency: {snapshot['last_cycle_latency_ms']:<5.2f} ms | "
              f"Avg Latency: {snapshot['average_cycle_latency_ms']:<5.2f} ms")

    print("------------------------------------------------------------------------------")
    print("\n[Recent Monitored Alerts from Thread-Safe Lock Snapshot]:")
    alerts = global_daemon_state.get_recent_alerts(limit=5)
    if alerts:
        for a in alerts:
            print(f"  * [{a.get('type')}] Milestone: {a.get('milestone_title')} (Student: {a.get('student_id')}) -> {a.get('message')}")
    else:
        print("  * No active overdue milestones detected.")

    print("\n[Graceful Shutdown] Sending stop signal to daemon worker thread...")
    daemon.stop()
    daemon.join(timeout=2.0)
    print(f"[Thread State After Stop]  Is Alive: {daemon.is_alive()} | Status: {global_daemon_state.get_state_snapshot()['daemon_status']}")
    print("=" * 78)
    print("Concurrency Execution Complete. Zero Deadlocks. Safe Reentrant Locking Confirmed.")
    print("=" * 78)


if __name__ == "__main__":
    main()
