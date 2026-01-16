"""
EPANET Interface Module
========================

This module provides a comprehensive interface to EPANET for water distribution
system simulation and analysis. It helps resolve regulatory sanctions and achieve
compliance with water system rules and regulations.

Key Features:
- Load and simulate EPANET network models
- Analyze hydraulic and water quality parameters
- Generate compliance reports
- Identify system vulnerabilities
- Optimize water distribution operations
"""

import wntr
import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Tuple
import warnings


class EPANETInterface:
    """
    Main interface class for EPANET water distribution system modeling.
    
    This class provides methods to:
    - Load EPANET network models (.inp files)
    - Run hydraulic and water quality simulations
    - Analyze network performance
    - Generate compliance reports
    - Export results for regulatory review
    """
    
    def __init__(self, inp_file: Optional[str] = None):
        """
        Initialize the EPANET interface.
        
        Args:
            inp_file: Path to EPANET .inp file (optional)
        """
        self.wn = None
        self.sim_results = None
        self.inp_file = inp_file
        
        if inp_file:
            self.load_network(inp_file)
    
    def load_network(self, inp_file: str) -> None:
        """
        Load an EPANET network model from an .inp file.
        
        Args:
            inp_file: Path to the EPANET .inp file
        
        Raises:
            FileNotFoundError: If the inp file doesn't exist
            Exception: If the file cannot be parsed
        """
        try:
            self.wn = wntr.network.WaterNetworkModel(inp_file)
            self.inp_file = inp_file
            print(f"Successfully loaded network from {inp_file}")
            print(f"Network contains {self.wn.num_junctions} junctions, "
                  f"{self.wn.num_pipes} pipes, {self.wn.num_tanks} tanks, "
                  f"{self.wn.num_reservoirs} reservoirs")
        except Exception as e:
            raise Exception(f"Failed to load network file: {str(e)}")
    
    def create_simple_network(self) -> None:
        """
        Create a simple example water network for testing and demonstration.
        
        This creates a basic network with:
        - 1 reservoir (source)
        - 3 junctions (nodes)
        - 3 pipes
        - 1 tank for storage
        """
        self.wn = wntr.network.WaterNetworkModel()
        
        # Add reservoir (water source)
        self.wn.add_reservoir('Reservoir1', base_head=100.0)
        
        # Add junctions (demand nodes)
        self.wn.add_junction('Junction1', base_demand=0.01, elevation=50.0)
        self.wn.add_junction('Junction2', base_demand=0.015, elevation=45.0)
        self.wn.add_junction('Junction3', base_demand=0.02, elevation=40.0)
        
        # Add tank
        self.wn.add_tank('Tank1', elevation=60.0, init_level=10.0, 
                         min_level=5.0, max_level=15.0, diameter=10.0)
        
        # Add pipes connecting the network
        self.wn.add_pipe('Pipe1', 'Reservoir1', 'Junction1', 
                         length=1000.0, diameter=0.3, roughness=100)
        self.wn.add_pipe('Pipe2', 'Junction1', 'Junction2', 
                         length=800.0, diameter=0.25, roughness=100)
        self.wn.add_pipe('Pipe3', 'Junction2', 'Junction3', 
                         length=600.0, diameter=0.2, roughness=100)
        self.wn.add_pipe('Pipe4', 'Junction1', 'Tank1', 
                         length=500.0, diameter=0.25, roughness=100)
        
        print("Created simple example network")
    
    def run_simulation(self, duration: int = 86400) -> None:
        """
        Run hydraulic simulation on the loaded network.
        
        Args:
            duration: Simulation duration in seconds (default: 86400 = 24 hours)
        
        Raises:
            ValueError: If no network is loaded
        """
        if self.wn is None:
            raise ValueError("No network loaded. Load a network first or create an example.")
        
        try:
            # Set simulation duration
            self.wn.options.time.duration = duration
            
            # Run simulation
            sim = wntr.sim.EpanetSimulator(self.wn)
            self.sim_results = sim.run_sim()
            
            print(f"Simulation completed successfully for {duration/3600:.1f} hours")
        except Exception as e:
            raise Exception(f"Simulation failed: {str(e)}")
    
    def get_pressure_summary(self) -> pd.DataFrame:
        """
        Get summary statistics of pressure at all junctions.
        
        Returns:
            DataFrame with pressure statistics (min, max, mean) for each junction
        
        Raises:
            ValueError: If simulation hasn't been run
        """
        if self.sim_results is None:
            raise ValueError("No simulation results. Run simulation first.")
        
        pressure = self.sim_results.node['pressure']
        
        summary = pd.DataFrame({
            'Min_Pressure_m': pressure.min(axis=0),
            'Max_Pressure_m': pressure.max(axis=0),
            'Mean_Pressure_m': pressure.mean(axis=0),
            'Std_Pressure_m': pressure.std(axis=0)
        })
        
        return summary
    
    def get_flow_summary(self) -> pd.DataFrame:
        """
        Get summary statistics of flow in all pipes.
        
        Returns:
            DataFrame with flow statistics (min, max, mean) for each pipe
        
        Raises:
            ValueError: If simulation hasn't been run
        """
        if self.sim_results is None:
            raise ValueError("No simulation results. Run simulation first.")
        
        flowrate = self.sim_results.link['flowrate']
        
        summary = pd.DataFrame({
            'Min_Flow_m3/s': flowrate.min(axis=0),
            'Max_Flow_m3/s': flowrate.max(axis=0),
            'Mean_Flow_m3/s': flowrate.mean(axis=0),
            'Std_Flow_m3/s': flowrate.std(axis=0)
        })
        
        return summary
    
    def check_pressure_compliance(self, min_pressure: float = 20.0, 
                                  max_pressure: float = 100.0) -> Dict:
        """
        Check if pressures meet regulatory compliance requirements.
        
        Args:
            min_pressure: Minimum acceptable pressure in meters (default: 20m)
            max_pressure: Maximum acceptable pressure in meters (default: 100m)
        
        Returns:
            Dictionary with compliance status and violations
        
        Raises:
            ValueError: If simulation hasn't been run
        """
        if self.sim_results is None:
            raise ValueError("No simulation results. Run simulation first.")
        
        pressure = self.sim_results.node['pressure']
        
        # Find violations
        low_pressure_violations = (pressure < min_pressure).sum().sum()
        high_pressure_violations = (pressure > max_pressure).sum().sum()
        
        # Identify nodes with violations
        low_pressure_nodes = pressure.columns[
            (pressure < min_pressure).any(axis=0)
        ].tolist()
        high_pressure_nodes = pressure.columns[
            (pressure > max_pressure).any(axis=0)
        ].tolist()
        
        compliant = (low_pressure_violations == 0 and high_pressure_violations == 0)
        
        return {
            'compliant': compliant,
            'low_pressure_violations': low_pressure_violations,
            'high_pressure_violations': high_pressure_violations,
            'low_pressure_nodes': low_pressure_nodes,
            'high_pressure_nodes': high_pressure_nodes,
            'min_pressure_threshold': min_pressure,
            'max_pressure_threshold': max_pressure
        }
    
    def generate_compliance_report(self, output_file: Optional[str] = None) -> str:
        """
        Generate a comprehensive compliance report.
        
        Args:
            output_file: Optional path to save the report (text file)
        
        Returns:
            String containing the compliance report
        
        Raises:
            ValueError: If simulation hasn't been run
        """
        if self.sim_results is None:
            raise ValueError("No simulation results. Run simulation first.")
        
        report_lines = []
        report_lines.append("=" * 70)
        report_lines.append("WATER SYSTEM COMPLIANCE REPORT")
        report_lines.append("=" * 70)
        report_lines.append("")
        
        # Network information
        report_lines.append("NETWORK INFORMATION:")
        report_lines.append(f"  Input File: {self.inp_file if self.inp_file else 'N/A'}")
        report_lines.append(f"  Junctions: {self.wn.num_junctions}")
        report_lines.append(f"  Pipes: {self.wn.num_pipes}")
        report_lines.append(f"  Tanks: {self.wn.num_tanks}")
        report_lines.append(f"  Reservoirs: {self.wn.num_reservoirs}")
        report_lines.append("")
        
        # Pressure compliance
        report_lines.append("PRESSURE COMPLIANCE:")
        compliance = self.check_pressure_compliance()
        report_lines.append(f"  Status: {'COMPLIANT' if compliance['compliant'] else 'NON-COMPLIANT'}")
        report_lines.append(f"  Low Pressure Violations: {compliance['low_pressure_violations']}")
        report_lines.append(f"  High Pressure Violations: {compliance['high_pressure_violations']}")
        
        if compliance['low_pressure_nodes']:
            report_lines.append(f"  Nodes with Low Pressure: {', '.join(compliance['low_pressure_nodes'])}")
        if compliance['high_pressure_nodes']:
            report_lines.append(f"  Nodes with High Pressure: {', '.join(compliance['high_pressure_nodes'])}")
        report_lines.append("")
        
        # Pressure summary
        report_lines.append("PRESSURE SUMMARY:")
        pressure_summary = self.get_pressure_summary()
        report_lines.append(pressure_summary.to_string())
        report_lines.append("")
        
        # Flow summary
        report_lines.append("FLOW SUMMARY:")
        flow_summary = self.get_flow_summary()
        report_lines.append(flow_summary.to_string())
        report_lines.append("")
        
        report_lines.append("=" * 70)
        
        report = "\n".join(report_lines)
        
        if output_file:
            with open(output_file, 'w') as f:
                f.write(report)
            print(f"Compliance report saved to {output_file}")
        
        return report
    
    def export_results(self, prefix: str = "results") -> Dict[str, str]:
        """
        Export simulation results to CSV files.
        
        Args:
            prefix: Prefix for output files (default: "results")
        
        Returns:
            Dictionary mapping result type to filename
        
        Raises:
            ValueError: If simulation hasn't been run
        """
        if self.sim_results is None:
            raise ValueError("No simulation results. Run simulation first.")
        
        files = {}
        
        # Export pressure data
        pressure_file = f"{prefix}_pressure.csv"
        self.sim_results.node['pressure'].to_csv(pressure_file)
        files['pressure'] = pressure_file
        
        # Export flow data
        flow_file = f"{prefix}_flow.csv"
        self.sim_results.link['flowrate'].to_csv(flow_file)
        files['flow'] = flow_file
        
        # Export demand data
        demand_file = f"{prefix}_demand.csv"
        self.sim_results.node['demand'].to_csv(demand_file)
        files['demand'] = demand_file
        
        print(f"Results exported: {', '.join(files.values())}")
        
        return files
    
    def get_network_info(self) -> Dict:
        """
        Get basic information about the loaded network.
        
        Returns:
            Dictionary with network statistics
        
        Raises:
            ValueError: If no network is loaded
        """
        if self.wn is None:
            raise ValueError("No network loaded.")
        
        return {
            'num_junctions': self.wn.num_junctions,
            'num_pipes': self.wn.num_pipes,
            'num_tanks': self.wn.num_tanks,
            'num_reservoirs': self.wn.num_reservoirs,
            'num_pumps': self.wn.num_pumps,
            'num_valves': self.wn.num_valves,
            'junction_names': self.wn.junction_name_list,
            'pipe_names': self.wn.pipe_name_list,
        }


def main():
    """
    Example usage of the EPANET Interface.
    """
    print("EPANET Interface - Example Usage")
    print("=" * 50)
    
    # Create an interface instance
    epanet = EPANETInterface()
    
    # Create a simple example network
    print("\n1. Creating example network...")
    epanet.create_simple_network()
    
    # Get network info
    print("\n2. Network information:")
    info = epanet.get_network_info()
    for key, value in info.items():
        if not isinstance(value, list):
            print(f"   {key}: {value}")
    
    # Run simulation
    print("\n3. Running 24-hour simulation...")
    epanet.run_simulation(duration=86400)
    
    # Check compliance
    print("\n4. Checking pressure compliance...")
    compliance = epanet.check_pressure_compliance()
    print(f"   Compliant: {compliance['compliant']}")
    print(f"   Low pressure violations: {compliance['low_pressure_violations']}")
    print(f"   High pressure violations: {compliance['high_pressure_violations']}")
    
    # Get summaries
    print("\n5. Pressure summary:")
    print(epanet.get_pressure_summary())
    
    print("\n6. Flow summary:")
    print(epanet.get_flow_summary())
    
    # Generate compliance report
    print("\n7. Generating compliance report...")
    report = epanet.generate_compliance_report()
    print("\n" + report)


if __name__ == "__main__":
    main()
