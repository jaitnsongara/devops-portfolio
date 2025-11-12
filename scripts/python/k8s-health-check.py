#!/usr/bin/env python3
"""
Kubernetes Cluster Health Check Script
Author: Jatin Songara
Description: Comprehensive health monitoring for Kubernetes clusters
"""

import sys
import json
import subprocess
from datetime import datetime
from typing import Dict, List, Tuple
from dataclasses import dataclass
from enum import Enum

class HealthStatus(Enum):
    HEALTHY = "✓ HEALTHY"
    WARNING = "⚠ WARNING"
    CRITICAL = "✗ CRITICAL"
    UNKNOWN = "? UNKNOWN"

@dataclass
class CheckResult:
    name: str
    status: HealthStatus
    message: str
    details: Dict = None

class K8sHealthChecker:
    def __init__(self, namespace: str = "default"):
        self.namespace = namespace
        self.results: List[CheckResult] = []
    
    def run_kubectl(self, args: List[str]) -> Tuple[str, int]:
        """Execute kubectl command and return output"""
        try:
            cmd = ["kubectl"] + args
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=30
            )
            return result.stdout, result.returncode
        except subprocess.TimeoutExpired:
            return "", 1
        except Exception as e:
            return str(e), 1
    
    def check_cluster_connectivity(self) -> CheckResult:
        """Check if cluster is accessible"""
        output, returncode = self.run_kubectl(["cluster-info"])
        
        if returncode == 0:
            return CheckResult(
                name="Cluster Connectivity",
                status=HealthStatus.HEALTHY,
                message="Cluster is accessible"
            )
        else:
            return CheckResult(
                name="Cluster Connectivity",
                status=HealthStatus.CRITICAL,
                message="Cannot connect to cluster"
            )
    
    def check_nodes(self) -> CheckResult:
        """Check node status"""
        output, returncode = self.run_kubectl([
            "get", "nodes",
            "-o", "json"
        ])
        
        if returncode != 0:
            return CheckResult(
                name="Node Health",
                status=HealthStatus.CRITICAL,
                message="Failed to get node information"
            )
        
        try:
            nodes = json.loads(output)
            total_nodes = len(nodes.get("items", []))
            ready_nodes = 0
            not_ready = []
            
            for node in nodes.get("items", []):
                node_name = node["metadata"]["name"]
                conditions = node["status"]["conditions"]
                
                for condition in conditions:
                    if condition["type"] == "Ready":
                        if condition["status"] == "True":
                            ready_nodes += 1
                        else:
                            not_ready.append(node_name)
            
            if ready_nodes == total_nodes:
                status = HealthStatus.HEALTHY
                message = f"All {total_nodes} nodes are ready"
            elif ready_nodes > 0:
                status = HealthStatus.WARNING
                message = f"{ready_nodes}/{total_nodes} nodes ready. Not ready: {', '.join(not_ready)}"
            else:
                status = HealthStatus.CRITICAL
                message = "No nodes are ready"
            
            return CheckResult(
                name="Node Health",
                status=status,
                message=message,
                details={"total": total_nodes, "ready": ready_nodes}
            )
        except json.JSONDecodeError:
            return CheckResult(
                name="Node Health",
                status=HealthStatus.UNKNOWN,
                message="Failed to parse node information"
            )
    
    def check_pods(self) -> CheckResult:
        """Check pod status in namespace"""
        output, returncode = self.run_kubectl([
            "get", "pods",
            "-n", self.namespace,
            "-o", "json"
        ])
        
        if returncode != 0:
            return CheckResult(
                name="Pod Health",
                status=HealthStatus.CRITICAL,
                message=f"Failed to get pods in namespace {self.namespace}"
            )
        
        try:
            pods = json.loads(output)
            total_pods = len(pods.get("items", []))
            
            if total_pods == 0:
                return CheckResult(
                    name="Pod Health",
                    status=HealthStatus.WARNING,
                    message=f"No pods found in namespace {self.namespace}"
                )
            
            running = 0
            pending = 0
            failed = 0
            unknown = 0
            
            for pod in pods.get("items", []):
                phase = pod["status"]["phase"]
                if phase == "Running":
                    running += 1
                elif phase == "Pending":
                    pending += 1
                elif phase == "Failed":
                    failed += 1
                else:
                    unknown += 1
            
            if failed > 0:
                status = HealthStatus.CRITICAL
                message = f"{failed} pods failed, {running} running, {pending} pending"
            elif pending > total_pods * 0.3:
                status = HealthStatus.WARNING
                message = f"{pending} pods pending, {running} running"
            else:
                status = HealthStatus.HEALTHY
                message = f"{running}/{total_pods} pods running"
            
            return CheckResult(
                name="Pod Health",
                status=status,
                message=message,
                details={
                    "total": total_pods,
                    "running": running,
                    "pending": pending,
                    "failed": failed
                }
            )
        except json.JSONDecodeError:
            return CheckResult(
                name="Pod Health",
                status=HealthStatus.UNKNOWN,
                message="Failed to parse pod information"
            )
    
    def check_deployments(self) -> CheckResult:
        """Check deployment status"""
        output, returncode = self.run_kubectl([
            "get", "deployments",
            "-n", self.namespace,
            "-o", "json"
        ])
        
        if returncode != 0:
            return CheckResult(
                name="Deployment Health",
                status=HealthStatus.WARNING,
                message="Failed to get deployments"
            )
        
        try:
            deployments = json.loads(output)
            total = len(deployments.get("items", []))
            
            if total == 0:
                return CheckResult(
                    name="Deployment Health",
                    status=HealthStatus.HEALTHY,
                    message="No deployments in namespace"
                )
            
            healthy = 0
            unhealthy = []
            
            for deploy in deployments.get("items", []):
                name = deploy["metadata"]["name"]
                spec_replicas = deploy["spec"]["replicas"]
                status = deploy.get("status", {})
                ready_replicas = status.get("readyReplicas", 0)
                
                if ready_replicas == spec_replicas:
                    healthy += 1
                else:
                    unhealthy.append(f"{name}({ready_replicas}/{spec_replicas})")
            
            if healthy == total:
                status = HealthStatus.HEALTHY
                message = f"All {total} deployments are healthy"
            else:
                status = HealthStatus.WARNING
                message = f"{len(unhealthy)} unhealthy: {', '.join(unhealthy)}"
            
            return CheckResult(
                name="Deployment Health",
                status=status,
                message=message,
                details={"total": total, "healthy": healthy}
            )
        except json.JSONDecodeError:
            return CheckResult(
                name="Deployment Health",
                status=HealthStatus.UNKNOWN,
                message="Failed to parse deployment information"
            )
    
    def check_pvc(self) -> CheckResult:
        """Check PersistentVolumeClaim status"""
        output, returncode = self.run_kubectl([
            "get", "pvc",
            "-n", self.namespace,
            "-o", "json"
        ])
        
        if returncode != 0:
            return CheckResult(
                name="Storage Health",
                status=HealthStatus.WARNING,
                message="Failed to get PVC information"
            )
        
        try:
            pvcs = json.loads(output)
            total = len(pvcs.get("items", []))
            
            if total == 0:
                return CheckResult(
                    name="Storage Health",
                    status=HealthStatus.HEALTHY,
                    message="No PVCs in namespace"
                )
            
            bound = 0
            pending = []
            
            for pvc in pvcs.get("items", []):
                name = pvc["metadata"]["name"]
                phase = pvc["status"]["phase"]
                
                if phase == "Bound":
                    bound += 1
                else:
                    pending.append(f"{name}({phase})")
            
            if bound == total:
                status = HealthStatus.HEALTHY
                message = f"All {total} PVCs are bound"
            else:
                status = HealthStatus.WARNING
                message = f"{len(pending)} not bound: {', '.join(pending)}"
            
            return CheckResult(
                name="Storage Health",
                status=status,
                message=message,
                details={"total": total, "bound": bound}
            )
        except json.JSONDecodeError:
            return CheckResult(
                name="Storage Health",
                status=HealthStatus.UNKNOWN,
                message="Failed to parse PVC information"
            )
    
    def run_all_checks(self):
        """Run all health checks"""
        print(f"\n{'='*60}")
        print(f"Kubernetes Health Check - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Namespace: {self.namespace}")
        print(f"{'='*60}\n")
        
        checks = [
            self.check_cluster_connectivity,
            self.check_nodes,
            self.check_pods,
            self.check_deployments,
            self.check_pvc
        ]
        
        for check in checks:
            result = check()
            self.results.append(result)
            self.print_result(result)
        
        self.print_summary()
    
    def print_result(self, result: CheckResult):
        """Print individual check result"""
        print(f"{result.status.value:15} | {result.name:20} | {result.message}")
        if result.details:
            print(f"{'':15} | {'':20} | Details: {result.details}")
        print()
    
    def print_summary(self):
        """Print overall summary"""
        print(f"\n{'='*60}")
        print("SUMMARY")
        print(f"{'='*60}")
        
        status_counts = {
            HealthStatus.HEALTHY: 0,
            HealthStatus.WARNING: 0,
            HealthStatus.CRITICAL: 0,
            HealthStatus.UNKNOWN: 0
        }
        
        for result in self.results:
            status_counts[result.status] += 1
        
        print(f"Total Checks: {len(self.results)}")
        print(f"Healthy: {status_counts[HealthStatus.HEALTHY]}")
        print(f"Warnings: {status_counts[HealthStatus.WARNING]}")
        print(f"Critical: {status_counts[HealthStatus.CRITICAL]}")
        print(f"Unknown: {status_counts[HealthStatus.UNKNOWN]}")
        
        # Exit code based on worst status
        if status_counts[HealthStatus.CRITICAL] > 0:
            sys.exit(2)
        elif status_counts[HealthStatus.WARNING] > 0:
            sys.exit(1)
        else:
            sys.exit(0)

def main():
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Kubernetes Cluster Health Check"
    )
    parser.add_argument(
        "-n", "--namespace",
        default="default",
        help="Kubernetes namespace to check (default: default)"
    )
    
    args = parser.parse_args()
    
    checker = K8sHealthChecker(namespace=args.namespace)
    checker.run_all_checks()

if __name__ == "__main__":
    main()
