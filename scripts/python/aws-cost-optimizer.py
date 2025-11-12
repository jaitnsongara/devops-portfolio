#!/usr/bin/env python3
"""
AWS Cost Optimization Script
Author: Jatin Songara
Description: Identify and report on AWS cost optimization opportunities
"""

import boto3
import json
from datetime import datetime, timedelta
from typing import Dict, List
from dataclasses import dataclass, asdict

@dataclass
class CostRecommendation:
    resource_type: str
    resource_id: str
    current_cost: float
    potential_savings: float
    recommendation: str
    priority: str

class AWSCostOptimizer:
    def __init__(self, region='us-east-1'):
        self.region = region
        self.ec2 = boto3.client('ec2', region_name=region)
        self.cloudwatch = boto3.client('cloudwatch', region_name=region)
        self.rds = boto3.client('rds', region_name=region)
        self.recommendations: List[CostRecommendation] = []
    
    def check_underutilized_ec2(self):
        """Find underutilized EC2 instances"""
        print("🔍 Checking for underutilized EC2 instances...")
        
        instances = self.ec2.describe_instances(
            Filters=[{'Name': 'instance-state-name', 'Values': ['running']}]
        )
        
        for reservation in instances['Reservations']:
            for instance in reservation['Instances']:
                instance_id = instance['InstanceId']
                instance_type = instance['InstanceType']
                
                # Get CPU utilization
                cpu_stats = self.cloudwatch.get_metric_statistics(
                    Namespace='AWS/EC2',
                    MetricName='CPUUtilization',
                    Dimensions=[{'Name': 'InstanceId', 'Value': instance_id}],
                    StartTime=datetime.now() - timedelta(days=7),
                    EndTime=datetime.now(),
                    Period=3600,
                    Statistics=['Average']
                )
                
                if cpu_stats['Datapoints']:
                    avg_cpu = sum(d['Average'] for d in cpu_stats['Datapoints']) / len(cpu_stats['Datapoints'])
                    
                    if avg_cpu < 10:
                        self.recommendations.append(CostRecommendation(
                            resource_type='EC2',
                            resource_id=instance_id,
                            current_cost=self.estimate_ec2_cost(instance_type),
                            potential_savings=self.estimate_ec2_cost(instance_type) * 0.8,
                            recommendation=f'Instance {instance_id} has {avg_cpu:.1f}% CPU utilization. Consider stopping or downsizing.',
                            priority='HIGH'
                        ))
    
    def check_unattached_volumes(self):
        """Find unattached EBS volumes"""
        print("🔍 Checking for unattached EBS volumes...")
        
        volumes = self.ec2.describe_volumes(
            Filters=[{'Name': 'status', 'Values': ['available']}]
        )
        
        for volume in volumes['Volumes']:
            volume_id = volume['VolumeId']
            size = volume['Size']
            monthly_cost = size * 0.10  # Approximate cost per GB
            
            self.recommendations.append(CostRecommendation(
                resource_type='EBS',
                resource_id=volume_id,
                current_cost=monthly_cost,
                potential_savings=monthly_cost,
                recommendation=f'Unattached {size}GB volume. Delete if not needed.',
                priority='MEDIUM'
            ))
    
    def check_old_snapshots(self):
        """Find old EBS snapshots"""
        print("🔍 Checking for old EBS snapshots...")
        
        snapshots = self.ec2.describe_snapshots(OwnerIds=['self'])
        cutoff_date = datetime.now() - timedelta(days=90)
        
        for snapshot in snapshots['Snapshots']:
            snapshot_id = snapshot['SnapshotId']
            start_time = snapshot['StartTime'].replace(tzinfo=None)
            
            if start_time < cutoff_date:
                size = snapshot['VolumeSize']
                monthly_cost = size * 0.05  # Approximate snapshot cost
                
                self.recommendations.append(CostRecommendation(
                    resource_type='Snapshot',
                    resource_id=snapshot_id,
                    current_cost=monthly_cost,
                    potential_savings=monthly_cost,
                    recommendation=f'Snapshot older than 90 days. Review retention policy.',
                    priority='LOW'
                ))
    
    def check_elastic_ips(self):
        """Find unassociated Elastic IPs"""
        print("🔍 Checking for unassociated Elastic IPs...")
        
        addresses = self.ec2.describe_addresses()
        
        for address in addresses['Addresses']:
            if 'InstanceId' not in address:
                allocation_id = address.get('AllocationId', 'N/A')
                public_ip = address.get('PublicIp', 'N/A')
                
                self.recommendations.append(CostRecommendation(
                    resource_type='EIP',
                    resource_id=allocation_id,
                    current_cost=3.60,  # $0.005/hour * 720 hours
                    potential_savings=3.60,
                    recommendation=f'Unassociated Elastic IP {public_ip}. Release if not needed.',
                    priority='HIGH'
                ))
    
    def estimate_ec2_cost(self, instance_type: str) -> float:
        """Estimate monthly EC2 cost (simplified)"""
        # Simplified pricing - in production, use AWS Price List API
        pricing = {
            't2.micro': 8.50,
            't2.small': 17.00,
            't2.medium': 34.00,
            't3.micro': 7.50,
            't3.small': 15.00,
            't3.medium': 30.00,
            'm5.large': 70.00,
            'm5.xlarge': 140.00,
        }
        return pricing.get(instance_type, 50.00)
    
    def generate_report(self):
        """Generate cost optimization report"""
        print("\n" + "="*70)
        print("AWS COST OPTIMIZATION REPORT")
        print(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Region: {self.region}")
        print("="*70 + "\n")
        
        if not self.recommendations:
            print("✅ No cost optimization opportunities found!")
            return
        
        # Sort by potential savings
        sorted_recs = sorted(
            self.recommendations,
            key=lambda x: x.potential_savings,
            reverse=True
        )
        
        total_savings = sum(r.potential_savings for r in sorted_recs)
        
        print(f"💰 Total Potential Monthly Savings: ${total_savings:.2f}\n")
        
        # Group by priority
        for priority in ['HIGH', 'MEDIUM', 'LOW']:
            priority_recs = [r for r in sorted_recs if r.priority == priority]
            if priority_recs:
                print(f"\n{priority} PRIORITY ({len(priority_recs)} items)")
                print("-" * 70)
                
                for rec in priority_recs:
                    print(f"\n{rec.resource_type}: {rec.resource_id}")
                    print(f"  Current Cost: ${rec.current_cost:.2f}/month")
                    print(f"  Potential Savings: ${rec.potential_savings:.2f}/month")
                    print(f"  Recommendation: {rec.recommendation}")
        
        # Save to JSON
        report_file = f"cost-optimization-report-{datetime.now().strftime('%Y%m%d')}.json"
        with open(report_file, 'w') as f:
            json.dump(
                {
                    'generated_at': datetime.now().isoformat(),
                    'region': self.region,
                    'total_potential_savings': total_savings,
                    'recommendations': [asdict(r) for r in sorted_recs]
                },
                f,
                indent=2
            )
        
        print(f"\n\n📄 Report saved to: {report_file}")
    
    def run_analysis(self):
        """Run all cost optimization checks"""
        print("🚀 Starting AWS Cost Optimization Analysis...\n")
        
        try:
            self.check_underutilized_ec2()
            self.check_unattached_volumes()
            self.check_old_snapshots()
            self.check_elastic_ips()
            
            self.generate_report()
            
        except Exception as e:
            print(f"❌ Error during analysis: {str(e)}")
            raise

def main():
    import argparse
    
    parser = argparse.ArgumentParser(
        description='AWS Cost Optimization Analysis'
    )
    parser.add_argument(
        '--region',
        default='us-east-1',
        help='AWS region to analyze (default: us-east-1)'
    )
    
    args = parser.parse_args()
    
    optimizer = AWSCostOptimizer(region=args.region)
    optimizer.run_analysis()

if __name__ == '__main__':
    main()
