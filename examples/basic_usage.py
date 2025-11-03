#!/usr/bin/env python3
"""
Basic Usage Example for EPANET Interface

This script demonstrates the basic functionality of the EPANET interface
for water system simulation and compliance checking.
"""

import sys
import os

# Add parent directory to path to import epanet_interface
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from epanet_interface import EPANETInterface


def main():
    """Run basic EPANET interface example."""
    
    print("=" * 70)
    print("BASIC EPANET INTERFACE USAGE EXAMPLE")
    print("=" * 70)
    
    # Step 1: Create an EPANET interface instance
    print("\nStep 1: Creating EPANET interface...")
    epanet = EPANETInterface()
    
    # Step 2: Create a simple network (or load from .inp file)
    print("\nStep 2: Creating example water network...")
    epanet.create_simple_network()
    
    # Step 3: Get network information
    print("\nStep 3: Network Information")
    print("-" * 70)
    info = epanet.get_network_info()
    print(f"Junctions: {info['num_junctions']}")
    print(f"Pipes: {info['num_pipes']}")
    print(f"Tanks: {info['num_tanks']}")
    print(f"Reservoirs: {info['num_reservoirs']}")
    
    # Step 4: Run simulation
    print("\nStep 4: Running hydraulic simulation (24 hours)...")
    epanet.run_simulation(duration=86400)  # 24 hours in seconds
    
    # Step 5: Check pressure compliance
    print("\nStep 5: Checking Pressure Compliance")
    print("-" * 70)
    compliance = epanet.check_pressure_compliance(min_pressure=20.0, max_pressure=100.0)
    
    if compliance['compliant']:
        print("✓ System is COMPLIANT with pressure regulations")
    else:
        print("✗ System is NON-COMPLIANT with pressure regulations")
        print(f"  Low pressure violations: {compliance['low_pressure_violations']}")
        print(f"  High pressure violations: {compliance['high_pressure_violations']}")
        
        if compliance['low_pressure_nodes']:
            print(f"  Nodes with low pressure: {', '.join(compliance['low_pressure_nodes'])}")
        if compliance['high_pressure_nodes']:
            print(f"  Nodes with high pressure: {', '.join(compliance['high_pressure_nodes'])}")
    
    # Step 6: Display pressure summary
    print("\nStep 6: Pressure Summary")
    print("-" * 70)
    pressure_summary = epanet.get_pressure_summary()
    print(pressure_summary)
    
    # Step 7: Display flow summary
    print("\nStep 7: Flow Summary")
    print("-" * 70)
    flow_summary = epanet.get_flow_summary()
    print(flow_summary)
    
    # Step 8: Generate compliance report
    print("\nStep 8: Generating compliance report...")
    report_file = "compliance_report.txt"
    report = epanet.generate_compliance_report(output_file=report_file)
    print(f"Report saved to: {report_file}")
    
    # Step 9: Export results to CSV
    print("\nStep 9: Exporting results to CSV files...")
    files = epanet.export_results(prefix="example_results")
    print("Exported files:")
    for result_type, filename in files.items():
        print(f"  {result_type}: {filename}")
    
    print("\n" + "=" * 70)
    print("Example completed successfully!")
    print("=" * 70)


if __name__ == "__main__":
    main()
