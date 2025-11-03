# los-botines-vaquero-village

Water System Simulation to resolve regulatory sanctions and achieve compliance with rules and regulations.

## Overview

This repository provides a comprehensive Python interface for EPANET (Environmental Protection Agency's water distribution system modeling software). It enables water utilities to:

- Simulate water distribution systems
- Analyze hydraulic performance
- Check regulatory compliance
- Generate compliance reports
- Export detailed analysis results

## Quick Start

### Installation

```bash
pip install -r requirements.txt
```

### Basic Usage

```bash
# Run the basic example
python examples/basic_usage.py

# Analyze an existing EPANET network file
python examples/load_inp_file.py path/to/network.inp
```

### Python API

```python
from epanet_interface import EPANETInterface

# Create interface and example network
epanet = EPANETInterface()
epanet.create_simple_network()

# Run 24-hour simulation
epanet.run_simulation(duration=86400)

# Check compliance
compliance = epanet.check_pressure_compliance()
print(f"System is {'compliant' if compliance['compliant'] else 'non-compliant'}")

# Generate report
epanet.generate_compliance_report(output_file="report.txt")
```

## Documentation

For detailed documentation, see [EPANET_GUIDE.md](EPANET_GUIDE.md)

## Features

- **Network Loading**: Load existing EPANET .inp files or create networks programmatically
- **Hydraulic Simulation**: Run detailed hydraulic simulations over extended periods
- **Compliance Checking**: Automatically verify pressure compliance against regulatory standards
- **Comprehensive Reporting**: Generate detailed reports for regulatory review
- **Data Export**: Export results to CSV for further analysis
- **Network Analysis**: Analyze pressure, flow, and demand throughout the system

## Requirements

- Python 3.7+
- wntr (Water Network Tool for Resilience)
- numpy
- pandas
- matplotlib

## License

This project is for water utility compliance and analysis purposes.
