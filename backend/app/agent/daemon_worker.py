"""
Assignment 2.1: Concurrent Task Daemonization using Threads and Workers
Architecture: Multi-threaded Background Daemon Worker with Thread Locks & Queues (Unit-2)
"""

import time
import queue
import threading
from datetime import datetime, timezone
from typing import Dict, Any, List, Optional

class ConcurrentTelemetryState:
    """
    Thread-safe state container utilizing a reentrant lock (threading.Lock)
    to safely share metrics across the web application and background daemon.
    """
    def __init__(self):
        self._lock = threading.Lock()
        self._metrics = {
            "daemon_status": "STOPPED",
            "total_cycles_executed": 0,
            "total_alerts_dispatched": 0,
            "last_cycle_timestamp": None,
            "last_cycle_latency_ms": 0.0,
            "average_cycle_latency_ms": 0.0,
            "active_monitored_milestones": 5,
            "active_overdue_alerts": 2
        }
        self._alerts_history: List[Dict[str, Any]] = []

    def update_metrics(self, cycle_latency_ms: float, alerts: List[Dict[str, Any]], milestone_count: int, overdue_count: int):
        with self._lock:
            self._metrics["total_cycles_executed"] += 1
            self._metrics["total_alerts_dispatched"] += len(alerts)
            self._metrics["last_cycle_timestamp"] = datetime.now(timezone.utc).isoformat()
            self._metrics["last_cycle_latency_ms"] = round(cycle_latency_ms, 2)
            
            # Running average latency
            prev_avg = self._metrics["average_cycle_latency_ms"]
            count = self._metrics["total_cycles_executed"]
            self._metrics["average_cycle_latency_ms"] = round(((prev_avg * (count - 1)) + cycle_latency_ms) / count, 2)
            
            self._metrics["active_monitored_milestones"] = milestone_count
            self._metrics["active_overdue_alerts"] = overdue_count

            for a in alerts:
                self._alerts_history.append(a)
            # Keep last 50 alerts
            if len(self._alerts_history) > 50:
                self._alerts_history = self._alerts_history[-50:]

    def get_snapshot(self) -> Dict[str, Any]:
        with self._lock:
            return {
                "metrics": dict(self._metrics),
                "recent_alerts": list(self._alerts_history[-10:])
            }

    def get_state_snapshot(self) -> Dict[str, Any]:
        with self._lock:
            return dict(self._metrics)

    def get_recent_alerts(self, limit: int = 10) -> List[Dict[str, Any]]:
        with self._lock:
            return list(self._alerts_history[-limit:])

    def set_status(self, status: str):
        with self._lock:
            self._metrics["daemon_status"] = status

    def set_daemon_status(self, status: str):
        self.set_status(status)


class CareerMonitorDaemon:
    """
    Asynchronous Daemon Worker Thread that continuously monitors
    milestone deadlines, inactivity, and telemetry without blocking
    the primary FastAPI web event loop.
    """
    _instance: Optional['CareerMonitorDaemon'] = None

    def __init__(self, polling_interval_sec: float = 2.0, check_interval_seconds: Optional[float] = None):
        if check_interval_seconds is not None:
            self.polling_interval = check_interval_seconds
        else:
            self.polling_interval = polling_interval_sec
        self.state = ConcurrentTelemetryState()
        self.task_queue: queue.Queue = queue.Queue(maxsize=100) # Safe queue
        self._stop_event = threading.Event()
        self._worker_thread: Optional[threading.Thread] = None
        self._mock_milestones = [
            {"id": 1, "title": "SQL Window Functions & Analytics", "days_overdue": 0, "status": "in_progress", "student_id": "STU-101"},
            {"id": 2, "title": "Pandas Data Cleaning Pipeline", "days_overdue": 3, "status": "in_progress", "student_id": "STU-101"},
            {"id": 3, "title": "Interactive Power BI Dashboard", "days_overdue": 0, "status": "not_started", "student_id": "STU-102"},
            {"id": 4, "title": "Statistical Hypothesis Testing", "days_overdue": 5, "status": "blocked", "student_id": "STU-103"},
            {"id": 5, "title": "Portfolio Capstone Project", "days_overdue": 0, "status": "not_started", "student_id": "STU-101"}
        ]

    @classmethod
    def get_instance(cls) -> 'CareerMonitorDaemon':
        if cls._instance is None:
            cls._instance = CareerMonitorDaemon()
        return cls._instance

    @property
    def daemon(self) -> bool:
        return True

    @property
    def native_id(self) -> Optional[int]:
        if self._worker_thread and self._worker_thread.is_alive():
            return getattr(self._worker_thread, "native_id", 1001)
        return None

    def is_alive(self) -> bool:
        return self._worker_thread is not None and self._worker_thread.is_alive()

    def start(self):
        """Spawns the background worker daemon thread."""
        if self._worker_thread and self._worker_thread.is_alive():
            return
        self._stop_event.clear()
        self.state.set_status("RUNNING")
        self._worker_thread = threading.Thread(
            target=self._daemon_loop,
            name="CareerMonitorDaemonThread",
            daemon=True # Daemon thread shuts down automatically when main process exits
        )
        self._worker_thread.start()

    def stop(self):
        """Signals the background worker daemon thread to terminate safely."""
        self._stop_event.set()
        self.state.set_status("STOPPED")
        if self._worker_thread:
            self._worker_thread.join(timeout=1.0)

    def join(self, timeout: Optional[float] = None):
        if self._worker_thread:
            self._worker_thread.join(timeout=timeout)

    def submit_task(self, task_payload: Dict[str, Any]) -> bool:
        """Enqueues an urgent check task via thread-safe queue."""
        try:
            self.task_queue.put_nowait(task_payload)
            return True
        except queue.Full:
            return False

    def _daemon_loop(self):
        """Core continuous worker monitoring loop."""
        while not self._stop_event.is_set():
            t_start = time.perf_counter()

            # 1. Process any urgent queued tasks
            queued_tasks_processed = 0
            while not self.task_queue.empty():
                try:
                    task = self.task_queue.get_nowait()
                    queued_tasks_processed += 1
                    self.task_queue.task_done()
                except queue.Empty:
                    break

            # 2. Perform periodic environmental milestone scanning
            alerts = []
            overdue_count = 0
            for m in self._mock_milestones:
                if m["days_overdue"] > 0:
                    overdue_count += 1
                    alerts.append({
                        "type": "OVERDUE_MILESTONE",
                        "milestone_id": m["id"],
                        "milestone_title": m["title"],
                        "student_id": m.get("student_id", "STU-GENERIC"),
                        "days_overdue": m["days_overdue"],
                        "status": m["status"],
                        "timestamp": datetime.now(timezone.utc).isoformat(),
                        "message": f"Overdue Alert: '{m['title']}' is {m['days_overdue']} days past scheduled target."
                    })

            # 3. Compute execution latency
            t_end = time.perf_counter()
            cycle_latency_ms = (t_end - t_start) * 1000.0

            # 4. Safely update shared state under thread lock
            self.state.update_metrics(
                cycle_latency_ms=cycle_latency_ms,
                alerts=alerts,
                milestone_count=len(self._mock_milestones),
                overdue_count=overdue_count
            )

            # Wait for next poll interval or stop signal
            self._stop_event.wait(timeout=self.polling_interval)


# Global singleton daemon state instance
global_daemon_state = CareerMonitorDaemon.get_instance().state
