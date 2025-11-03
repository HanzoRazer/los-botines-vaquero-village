# EPANET Interface Guide

## Overview

This repository provides a comprehensive Python interface for EPANET (Environmental Protection Agency's water distribution system modeling software). The interface helps water utilities resolve regulatory sanctions and achieve compliance with water system rules and regulations.

## What is EPANET?

EPANET is a software application used throughout the world to model water distribution piping systems. It performs extended period simulation of hydraulic and water quality behavior within pressurized pipe networks.

## Features

Our EPANET interface provides:

- **Network Loading**: Load existing EPANET .inp files or create networks programmatically
- **Hydraulic Simulation**: Run detailed hydraulic simulations over time
- **Compliance Checking**: Automatically check pressure compliance against regulatory standards
- **Comprehensive Reporting**: Generate detailed compliance reports for regulatory review
- **Data Export**: Export simulation results to CSV for further analysis
- **Network Analysis**: Analyze pressure, flow, and demand throughout the system

## Installation

### Prerequisites

- Python 3.7 or higher
- pip (Python package installer)

### Install Dependencies

```bash
pip install -r requirements.txt
```

This will install:
- `wntr` (Water Network Tool for Resilience) - Python package for EPANET
- `numpy` - Numerical computing
- `pandas` - Data analysis and manipulation
- `matplotlib` - Plotting and visualization

## Quick Start

### Example 1: Basic Usage with Example Network

```python
from epanet_interface import EPANETInterface

# Create an interface instance
epanet = EPANETInterface()

# Create a simple example network
epanet.create_simple_network()

# Run a 24-hour simulation
epanet.run_simulation(duration=86400)

# Check pressure compliance
compliance = epanet.check_pressure_compliance()
print(f"System is {'compliant' if compliance['compliant'] else 'non-compliant'}")

# Generate a compliance report
report = epanet.generate_compliance_report(output_file="report.txt")
print(report)
```

### Example 2: Loading an Existing Network

```python
from epanet_interface import EPANETInterface

# Load an existing EPANET .inp file
epanet = EPANETInterface("path/to/network.inp")

# Run simulation
epanet.run_simulation(duration=86400)

# Get pressure summary
pressure_summary = epanet.get_pressure_summary()
print(pressure_summary)

# Export results
epanet.export_results(prefix="my_results")
```

## Running Example Scripts

### Basic Usage Example

```bash
cd /home/runner/work/los-botines-vaquero-village/los-botines-vaquero-village
python examples/basic_usage.py
```

This script demonstrates:
- Creating a simple network
- Running simulations
- Checking compliance
- Generating reports
- Exporting data

### Loading an Existing Network

```bash
python examples/load_inp_file.py path/to/your/network.inp
```

Options:
- `-d, --duration`: Simulation duration in seconds (default: 86400 = 24 hours)

Example:
```bash
python examples/load_inp_file.py network.inp --duration 172800  # 48-hour simulation
```

## API Reference

### EPANETInterface Class

#### Constructor

```python
EPANETInterface(inp_file: Optional[str] = None)
```

Creates an EPANET interface instance. Optionally loads a network from an .inp file.

#### Methods

##### `load_network(inp_file: str)`
Load an EPANET network model from an .inp file.

##### `create_simple_network()`
Create a simple example network for testing and demonstration.

##### `run_simulation(duration: int = 86400)`
Run hydraulic simulation on the loaded network.
- `duration`: Simulation duration in seconds (default: 86400 = 24 hours)

##### `get_pressure_summary() -> pd.DataFrame`
Get summary statistics (min, max, mean, std) of pressure at all junctions.

##### `get_flow_summary() -> pd.DataFrame`
Get summary statistics of flow in all pipes.

##### `check_pressure_compliance(min_pressure: float = 20.0, max_pressure: float = 100.0) -> Dict`
Check if pressures meet regulatory compliance requirements.
- `min_pressure`: Minimum acceptable pressure in meters (default: 20m)
- `max_pressure`: Maximum acceptable pressure in meters (default: 100m)

Returns a dictionary with:
- `compliant`: Boolean indicating overall compliance
- `low_pressure_violations`: Count of low pressure violations
- `high_pressure_violations`: Count of high pressure violations
- `low_pressure_nodes`: List of nodes with low pressure
- `high_pressure_nodes`: List of nodes with high pressure

##### `generate_compliance_report(output_file: Optional[str] = None) -> str`
Generate a comprehensive compliance report.
- `output_file`: Optional path to save the report

##### `export_results(prefix: str = "results") -> Dict[str, str]`
Export simulation results to CSV files.
- `prefix`: Prefix for output filenames

Returns a dictionary mapping result type to filename.

##### `get_network_info() -> Dict`
Get basic information about the loaded network.

## Compliance Checking

The interface provides automated compliance checking for pressure regulations:

```python
compliance = epanet.check_pressure_compliance(
    min_pressure=20.0,  # Minimum acceptable pressure (meters)
    max_pressure=100.0  # Maximum acceptable pressure (meters)
)

if not compliance['compliant']:
    print(f"Violations found:")
    print(f"  Low pressure: {compliance['low_pressure_violations']}")
    print(f"  High pressure: {compliance['high_pressure_violations']}")
    print(f"  Affected nodes: {compliance['low_pressure_nodes']}")
```

## Reporting

Generate comprehensive reports for regulatory review:

```python
# Generate and display report
report = epanet.generate_compliance_report()
print(report)

# Save report to file
epanet.generate_compliance_report(output_file="compliance_report.txt")
```

The report includes:
- Network information (junctions, pipes, tanks, etc.)
- Pressure compliance status
- Detailed pressure and flow summaries
- Lists of nodes with violations

## Data Export

Export simulation results for further analysis:

```python
files = epanet.export_results(prefix="simulation_2024")
# Creates:
#   - simulation_2024_pressure.csv
#   - simulation_2024_flow.csv
#   - simulation_2024_demand.csv
```

## Common Use Cases

### 1. Regulatory Compliance Assessment

Assess whether a water distribution system meets regulatory pressure requirements.

```python
epanet = EPANETInterface("current_network.inp")
epanet.run_simulation(duration=86400)
compliance = epanet.check_pressure_compliance()

if compliance['compliant']:
    print("System meets all regulatory requirements")
else:
    report = epanet.generate_compliance_report("compliance_report.txt")
    print("Non-compliant. Review report for details.")
```

### 2. Network Performance Analysis

Analyze system performance over time.

```python
epanet = EPANETInterface("network.inp")
epanet.run_simulation(duration=604800)  # 7 days

pressure_summary = epanet.get_pressure_summary()
flow_summary = epanet.get_flow_summary()

# Identify problem areas
low_pressure = pressure_summary[pressure_summary['Min_Pressure_m'] < 20]
print(f"Nodes with low pressure: {low_pressure.index.tolist()}")
```

### 3. Scenario Comparison

Compare multiple network configurations or operating scenarios.

```python
scenarios = ['baseline.inp', 'upgrade_pipes.inp', 'add_pump.inp']
results = {}

for scenario in scenarios:
    epanet = EPANETInterface(scenario)
    epanet.run_simulation()
    results[scenario] = epanet.check_pressure_compliance()
    
# Compare results
for scenario, compliance in results.items():
    print(f"{scenario}: {'PASS' if compliance['compliant'] else 'FAIL'}")
```

## Troubleshooting

### Common Issues

**ImportError: No module named 'wntr'**
- Solution: Install dependencies with `pip install -r requirements.txt`

**"Failed to load network file"**
- Check that the .inp file path is correct
- Verify the .inp file is a valid EPANET file
- Ensure you have read permissions for the file

**"No simulation results"**
- Make sure to run `run_simulation()` before accessing results
- Check that the simulation completed without errors

### Getting Help

For issues specific to EPANET modeling:
- EPANET Documentation: https://epanet22.readthedocs.io/
- WNTR Documentation: https://wntr.readthedocs.io/

For issues with this interface:
- Review the example scripts in the `examples/` directory
- Check the inline documentation in `epanet_interface.py`

## Best Practices

1. **Validate Input Data**: Always verify your .inp file is correct before running simulations
2. **Check Simulation Completion**: Verify that simulations complete successfully
3. **Save Reports**: Generate and save compliance reports for record-keeping
4. **Document Assumptions**: Document any assumptions about regulatory thresholds
5. **Regular Testing**: Test the interface with known networks to ensure accuracy

## Advanced Usage

### Custom Compliance Thresholds

Adjust pressure thresholds based on local regulations:

```python
# California example (hypothetical)
compliance = epanet.check_pressure_compliance(
    min_pressure=30.0,  # 30 meters minimum
    max_pressure=110.0  # 110 meters maximum
)
```

### Extended Simulations

Run longer simulations for seasonal analysis:

```python
# 30-day simulation
epanet.run_simulation(duration=30*24*3600)
```

### Batch Processing

Process multiple networks:

```python
import glob

for inp_file in glob.glob("networks/*.inp"):
    epanet = EPANETInterface(inp_file)
    epanet.run_simulation()
    epanet.generate_compliance_report(
        output_file=f"{inp_file}_report.txt"
    )
```

## License

This interface is provided for water utility compliance and analysis purposes.

## Contributing

Contributions to improve the EPANET interface are welcome. Please ensure:
- Code follows Python best practices
- New features include documentation
- Example scripts are updated as needed

## Acknowledgments

This interface uses the WNTR (Water Network Tool for Resilience) package, which provides Python bindings for EPANET.
