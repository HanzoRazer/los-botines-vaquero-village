#!/usr/bin/env python3
"""
Example: Loading and Analyzing an Existing EPANET .inp File

This script demonstrates how to load an existing EPANET network file
and perform analysis on it.
"""

import sys
import os
import argparse

# Add parent directory to path to import epanet_interface
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from epanet_interface import EPANETInterface


def analyze_network(inp_file: str, duration: int = 86400):
    """
    Load and analyze an EPANET network file.
    
    Args:
        inp_file: Path to the EPANET .inp file
        duration: Simulation duration in seconds (default: 24 hours)
    """
    
    print("=" * 70)
    print("EPANET NETWORK ANALYSIS")
    print("=" * 70)
    print(f"Input file: {inp_file}")
    print(f"Simulation duration: {duration/3600:.1f} hours")
    print()
    
    try:
        # Load the network
        print("Loading network...")
        epanet = EPANETInterface(inp_file)
        
        # Display network info
        print("\nNetwork Information:")
        print("-" * 70)
        info = epanet.get_network_info()
        print(f"  Junctions: {info['num_junctions']}")
        print(f"  Pipes: {info['num_pipes']}")
        print(f"  Tanks: {info['num_tanks']}")
        print(f"  Reservoirs: {info['num_reservoirs']}")
        print(f"  Pumps: {info['num_pumps']}")
        print(f"  Valves: {info['num_valves']}")
        
        # Run simulation
        print(f"\nRunning simulation for {duration/3600:.1f} hours...")
        epanet.run_simulation(duration=duration)
        
        # Check compliance
        print("\nPressure Compliance Check:")
        print("-" * 70)
        compliance = epanet.check_pressure_compliance()
        
        if compliance['compliant']:
            print("✓ Network is COMPLIANT with pressure regulations")
        else:
            print("✗ Network is NON-COMPLIANT with pressure regulations")
            print(f"  Low pressure violations: {compliance['low_pressure_violations']}")
            print(f"  High pressure violations: {compliance['high_pressure_violations']}")
        
        # Generate and save report
        print("\nGenerating compliance report...")
        base_name = os.path.splitext(os.path.basename(inp_file))[0]
        report_file = f"{base_name}_compliance_report.txt"
        epanet.generate_compliance_report(output_file=report_file)
        print(f"Report saved to: {report_file}")
        
        # Export results
        print("\nExporting simulation results...")
        files = epanet.export_results(prefix=f"{base_name}_results")
        for result_type, filename in files.items():
            print(f"  {result_type}: {filename}")
        
        print("\n" + "=" * 70)
        print("Analysis completed successfully!")
        print("=" * 70)
        
    except Exception as e:
        print(f"\nError: {str(e)}")
        print("Please check that the input file exists and is a valid EPANET .inp file")
        sys.exit(1)


def main():
    """Parse command line arguments and run analysis."""
    
    parser = argparse.ArgumentParser(
        description="Analyze an EPANET network file",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s network.inp
  %(prog)s network.inp --duration 172800  # 48 hours
  %(prog)s /path/to/network.inp --duration 3600  # 1 hour
        """
    )
    
    parser.add_argument(
        'inp_file',
        help='Path to EPANET .inp file'
    )
    
    parser.add_argument(
        '-d', '--duration',
        type=int,
        default=86400,
        help='Simulation duration in seconds (default: 86400 = 24 hours)'
    )
    
    args = parser.parse_args()
    
    # Validate input file
    if not os.path.exists(args.inp_file):
        print(f"Error: File not found: {args.inp_file}")
        sys.exit(1)
    
    # Run analysis
    analyze_network(args.inp_file, args.duration)


if __name__ == "__main__":
    main()
