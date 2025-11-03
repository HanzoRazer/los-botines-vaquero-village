# EPANET Interface Examples

This directory contains example scripts demonstrating how to use the EPANET interface.

## Example Scripts

### 1. basic_usage.py

Demonstrates basic functionality with a programmatically-created network:

```bash
python basic_usage.py
```

This script shows:
- Creating a simple water network from scratch
- Running a 24-hour hydraulic simulation
- Checking pressure compliance
- Generating compliance reports
- Exporting results to CSV files

### 2. load_inp_file.py

Shows how to load and analyze an existing EPANET network file:

```bash
# Analyze the sample network
python load_inp_file.py networks/sample_network.inp

# Specify custom simulation duration (in seconds)
python load_inp_file.py networks/sample_network.inp --duration 172800

# Get help
python load_inp_file.py --help
```

This script demonstrates:
- Loading an existing .inp file
- Running simulations with custom duration
- Compliance checking
- Automated report generation
- Result export

## Sample Networks

The `networks/` directory contains sample EPANET network files:

### sample_network.inp

A basic water distribution network with:
- 1 reservoir (water source)
- 4 junctions (demand nodes)
- 1 storage tank
- 5 pipes connecting the network

This network can be used to test the interface and understand EPANET modeling.

## Creating Your Own Scripts

You can create your own scripts by importing the interface:

```python
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from epanet_interface import EPANETInterface

# Your code here
epanet = EPANETInterface()
# ...
```

## Common Use Cases

### Batch Processing Multiple Networks

```python
import glob
from epanet_interface import EPANETInterface

for inp_file in glob.glob("networks/*.inp"):
    print(f"\nAnalyzing {inp_file}...")
    epanet = EPANETInterface(inp_file)
    epanet.run_simulation()
    
    compliance = epanet.check_pressure_compliance()
    status = "PASS" if compliance['compliant'] else "FAIL"
    print(f"Compliance: {status}")
```

### Comparing Scenarios

```python
from epanet_interface import EPANETInterface

scenarios = {
    'baseline': 'networks/current.inp',
    'upgrade': 'networks/upgraded.inp',
}

for name, file in scenarios.items():
    epanet = EPANETInterface(file)
    epanet.run_simulation()
    compliance = epanet.check_pressure_compliance()
    
    print(f"{name}: {compliance['low_pressure_violations']} violations")
```

### Custom Analysis

```python
from epanet_interface import EPANETInterface
import pandas as pd

epanet = EPANETInterface('networks/sample_network.inp')
epanet.run_simulation(duration=7*24*3600)  # 7 days

# Get pressure data
pressure_summary = epanet.get_pressure_summary()

# Find problematic nodes
low_pressure = pressure_summary[pressure_summary['Min_Pressure_m'] < 20]
print(f"Nodes with low pressure: {low_pressure.index.tolist()}")

# Export for detailed analysis
epanet.export_results(prefix='weekly_analysis')
```

## Output Files

Running the examples will create several output files:

- `*.txt` - Compliance reports
- `*_pressure.csv` - Pressure data at all nodes over time
- `*_flow.csv` - Flow data in all pipes over time
- `*_demand.csv` - Demand data at all junctions over time

These files are excluded from version control via `.gitignore`.
