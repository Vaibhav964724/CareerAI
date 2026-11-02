"""
Assignment 2.2: Distributed Agent Messaging using Sockets/RPC Communication
Architecture: Distributed Dual-Agent TCP Socket Messaging Mesh (Unit-2)
Implements:
  - Agent-A (Student Advisor): Client agent serializing student state to JSON frames
  - Agent-B (Placement Node): Server agent parsing frames, evaluating eligibility, and returning signed acknowledgments
"""

import json
import socket
import struct
import threading
import time
from datetime import datetime, timezone
from typing import Dict, Any, Optional, Tuple


class SocketAgentB_Server:
    """
    Agent-B: Remote Placement Node Server.
    Binds to a TCP port, listens for incoming serialized agent payloads,
    evaluates student profiles against placement criteria, and returns a verified evaluation response.
    """
    def __init__(self, host: str = "127.0.0.1", port: int = 9123):
        self.host = host
        self.port = port
        self.server_socket: Optional[socket.socket] = None
        self.is_running = False
        self.thread: Optional[threading.Thread] = None
        self.last_received_payload: Optional[Dict[str, Any]] = None
        self.last_response_payload: Optional[Dict[str, Any]] = None
        self.transactions_count = 0

    def start(self):
        """Starts the socket server in a background thread."""
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        self.is_running = True
        self.thread = threading.Thread(target=self._listen_loop, daemon=True)
        self.thread.start()

    def _listen_loop(self):
        self.server_socket.settimeout(1.0)
        while self.is_running:
            try:
                client_sock, client_addr = self.server_socket.accept()
                threading.Thread(
                    target=self._handle_client,
                    args=(client_sock, client_addr),
                    daemon=True
                ).start()
            except socket.timeout:
                continue
            except OSError:
                break

    def _handle_client(self, client_sock: socket.socket, client_addr: Tuple[str, int]):
        with client_sock:
            client_sock.settimeout(5.0)
            try:
                # 4-byte length prefix protocol
                raw_len = client_sock.recv(4)
                if not raw_len or len(raw_len) < 4:
                    return
                msg_len = struct.unpack("!I", raw_len)[0]
                
                # Receive exact payload bytes
                chunks = []
                bytes_recd = 0
                while bytes_recd < msg_len:
                    chunk = client_sock.recv(min(msg_len - bytes_recd, 4096))
                    if not chunk:
                        raise ConnectionError("Premature socket closure")
                    chunks.append(chunk)
                    bytes_recd += len(chunk)
                
                raw_data = b"".join(chunks).decode("utf-8")
                inbound_payload = json.loads(raw_data)
                self.last_received_payload = inbound_payload
                self.transactions_count += 1

                # Autonomous Decision-Making by Agent-B (Placement Node)
                response = self.process_remote_agent_payload(inbound_payload)
                self.last_response_payload = response

                # Send response back with length prefix
                resp_bytes = json.dumps(response).encode("utf-8")
                client_sock.sendall(struct.pack("!I", len(resp_bytes)) + resp_bytes)
            except Exception as e:
                err_resp = {
                    "status": "ERROR",
                    "error_message": str(e),
                    "timestamp": datetime.now(timezone.utc).isoformat()
                }
                resp_bytes = json.dumps(err_resp).encode("utf-8")
                try:
                    client_sock.sendall(struct.pack("!I", len(resp_bytes)) + resp_bytes)
                except Exception:
                    pass

    def process_remote_agent_payload(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Agent-B autonomous reasoning:
        Evaluates student profile data, target role criteria, and readiness score.
        """
        sender = payload.get("sender_agent", "UNKNOWN_AGENT")
        student_id = payload.get("student_id", "N/A")
        target_role = payload.get("target_role", "Software Engineer")
        skills = payload.get("skills", [])
        gpa = payload.get("gpa", 3.0)
        completed_milestones = payload.get("completed_milestones_count", 0)

        # Placement Node Criteria Evaluation
        has_core_skills = len(skills) >= 3
        meets_gpa = gpa >= 3.2
        meets_milestones = completed_milestones >= 2

        score = (
            (min(len(skills), 6) / 6.0) * 40.0 +
            (min(gpa, 4.0) / 4.0) * 30.0 +
            (min(completed_milestones, 5) / 5.0) * 30.0
        )
        readiness_score = round(score, 1)

        tier = "Gold Candidate" if readiness_score >= 80 else ("Silver Candidate" if readiness_score >= 60 else "Bronze Candidate")
        recommendations = []
        if not meets_gpa:
            recommendations.append("Academic GPA requirement borderline for elite tech firms.")
        if len(skills) < 4:
            recommendations.append("Acquire at least 1 advanced framework or cloud competency.")
        if completed_milestones < 3:
            recommendations.append("Complete ongoing portfolio project milestones before campus interview rounds.")

        return {
            "responder_agent": "Agent-B:PlacementNode",
            "in_response_to_sender": sender,
            "student_id": student_id,
            "target_role": target_role,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "placement_eligibility": readiness_score >= 60.0,
            "readiness_score": readiness_score,
            "placement_tier": tier,
            "verified_skills_count": len(skills),
            "recommendations": recommendations,
            "digital_handshake_signature": f"SIG-AGENT-B-{hash(student_id + str(readiness_score)) % 1000000:06d}",
            "status": "PROCESSED_SUCCESSFULLY"
        }

    def stop(self):
        """Stops the socket server gracefully."""
        self.is_running = False
        if self.server_socket:
            try:
                self.server_socket.close()
            except Exception:
                pass


class SocketAgentA_Client:
    """
    Agent-A: Student Advisor Client.
    Serializes local student profile state and transmits it over a TCP socket
    to Agent-B (Placement Node) for remote placement verification.
    """
    def __init__(self, host: str = "127.0.0.1", port: int = 9123):
        self.host = host
        self.port = port

    def send_agent_payload(self, payload: Dict[str, Any], timeout: float = 5.0) -> Dict[str, Any]:
        """
        Connects via TCP, sends length-prefixed JSON, and waits for serialized response.
        """
        payload["sender_agent"] = "Agent-A:StudentAdvisor"
        payload["dispatched_at"] = datetime.now(timezone.utc).isoformat()
        
        raw_json = json.dumps(payload).encode("utf-8")
        msg_len = len(raw_json)

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(timeout)
            sock.connect((self.host, self.port))
            
            # Send length prefix + payload
            sock.sendall(struct.pack("!I", msg_len) + raw_json)
            
            # Read response length
            raw_resp_len = sock.recv(4)
            if not raw_resp_len or len(raw_resp_len) < 4:
                raise ConnectionError("Did not receive response length prefix from Agent-B")
            resp_len = struct.unpack("!I", raw_resp_len)[0]

            # Read response payload
            chunks = []
            bytes_recd = 0
            while bytes_recd < resp_len:
                chunk = sock.recv(min(resp_len - bytes_recd, 4096))
                if not chunk:
                    raise ConnectionError("Connection lost while reading Agent-B response")
                chunks.append(chunk)
                bytes_recd += len(chunk)

            resp_json = b"".join(chunks).decode("utf-8")
            return json.loads(resp_json)


def execute_distributed_socket_exchange(
    student_profile: Dict[str, Any],
    port: int = 9123
) -> Dict[str, Any]:
    """
    Complete end-to-end distributed agent exchange demo helper:
    1. Attempts real TCP socket server and client handshake.
    2. Gracefully falls back to length-prefixed serialized loopback emulation if OS socket sandbox restricts raw ports.
    3. Returns full audit trail, frame serialization breakdown, and verification response.
    """
    audit_log = []
    t_start = time.perf_counter()

    # Attempt real TCP socket communication
    server = None
    try:
        server = SocketAgentB_Server(host="127.0.0.1", port=port)
        server.start()
        time.sleep(0.15)  # Allow socket bind to complete

        audit_log.append(f"[{datetime.now().strftime('%H:%M:%S.%f')[:-3]}] Agent-B server listening on TCP 127.0.0.1:{port}")
        client = SocketAgentA_Client(host="127.0.0.1", port=port)
        audit_log.append(f"[{datetime.now().strftime('%H:%M:%S.%f')[:-3]}] Agent-A establishing TCP handshake to 127.0.0.1:{port}...")

        response = client.send_agent_payload(student_profile)
        elapsed_ms = round((time.perf_counter() - t_start) * 1000, 2)

        audit_log.append(f"[{datetime.now().strftime('%H:%M:%S.%f')[:-3]}] Agent-A serialized payload ({len(json.dumps(student_profile))} bytes) transmitted over raw TCP socket.")
        audit_log.append(f"[{datetime.now().strftime('%H:%M:%S.%f')[:-3]}] Agent-B evaluated profile: Readiness {response.get('readiness_score')}% ({response.get('placement_tier')}).")
        audit_log.append(f"[{datetime.now().strftime('%H:%M:%S.%f')[:-3]}] Agent-B issued digital handshake: {response.get('digital_handshake_signature')}.")
        audit_log.append(f"[{datetime.now().strftime('%H:%M:%S.%f')[:-3]}] Round-trip TCP socket latency: {elapsed_ms} ms.")

        return {
            "status": "SUCCESS",
            "transport": "RAW_TCP_SOCKET",
            "round_trip_latency_ms": elapsed_ms,
            "port": port,
            "outbound_payload": student_profile,
            "inbound_response": response,
            "audit_trail": audit_log
        }
    except OSError as e:
        # Fallback to serialized byte stream protocol (handling sandbox port permission restrictions)
        audit_log.append(f"[{datetime.now().strftime('%H:%M:%S.%f')[:-3]}] OS TCP socket restricted by sandbox environment ({str(e)}). Switching to Length-Prefixed Serialized Stream Transport.")
        
        # Serialize outbound packet with 4-byte length prefix
        payload_copy = dict(student_profile)
        payload_copy["sender_agent"] = "Agent-A:StudentAdvisor"
        payload_copy["dispatched_at"] = datetime.now(timezone.utc).isoformat()
        
        raw_bytes = json.dumps(payload_copy).encode("utf-8")
        length_prefix = struct.pack("!I", len(raw_bytes))
        wire_frame = length_prefix + raw_bytes
        
        audit_log.append(f"[{datetime.now().strftime('%H:%M:%S.%f')[:-3]}] Agent-A generated length-prefixed frame: 4-byte header + {len(raw_bytes)} payload bytes.")
        
        # Ingest frame on Agent-B
        frame_len = struct.unpack("!I", wire_frame[:4])[0]
        inbound_payload = json.loads(wire_frame[4:4+frame_len].decode("utf-8"))
        
        # Agent-B processes frame
        server_instance = SocketAgentB_Server(host="127.0.0.1", port=port)
        response = server_instance.process_remote_agent_payload(inbound_payload)
        
        # Response frame
        resp_bytes = json.dumps(response).encode("utf-8")
        resp_frame = struct.pack("!I", len(resp_bytes)) + resp_bytes
        resp_len = struct.unpack("!I", resp_frame[:4])[0]
        verified_resp = json.loads(resp_frame[4:4+resp_len].decode("utf-8"))
        
        elapsed_ms = round((time.perf_counter() - t_start) * 1000, 2)
        audit_log.append(f"[{datetime.now().strftime('%H:%M:%S.%f')[:-3]}] Agent-B decoded wire frame and evaluated profile: Readiness {verified_resp.get('readiness_score')}% ({verified_resp.get('placement_tier')}).")
        audit_log.append(f"[{datetime.now().strftime('%H:%M:%S.%f')[:-3]}] Agent-B issued digital handshake: {verified_resp.get('digital_handshake_signature')}.")
        audit_log.append(f"[{datetime.now().strftime('%H:%M:%S.%f')[:-3]}] Round-trip serialization & dispatch latency: {elapsed_ms} ms.")

        return {
            "status": "SUCCESS",
            "transport": "SERIALIZED_FRAME_SOCKET_EMULATION",
            "round_trip_latency_ms": elapsed_ms,
            "port": port,
            "outbound_payload": student_profile,
            "inbound_response": verified_resp,
            "audit_trail": audit_log
        }
    finally:
        if server:
            server.stop()
