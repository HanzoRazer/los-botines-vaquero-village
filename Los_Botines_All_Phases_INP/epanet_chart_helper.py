#!/usr/bin/env python3
"""
EPANET Data Parser and Chart Generator
Handles EPANET's native export format and generates compliance charts

USAGE:
  python epanet_chart_helper.py file1.xlsx file2.xlsx ... [--scenario "Scenario Name"]

This script:
1. Parses EPANET's native Time Series export format
2. Combines multiple single-node exports into one dataset
3. Generates all compliance charts automatically
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from pathlib import Path
import sys
import argparse

# ============================================================================
# CONFIGURATION
# ============================================================================

COMPLIANCE_THRESHOLD = 20.0  # psi
OPERATING_MIN = 38.0
OPERATING_MAX = 60.0
FIGURE_DPI = 300

COLORS = {
    'threshold': '#DC3545',
    'envelope_fill': '#3498DB',
    'envelope_edge': '#1A5276',
    'pass': '#28A745',
    'fail': '#DC3545',
    'warn': '#FFC107',
}

NODE_COLORS = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd',
               '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf']

# ============================================================================
# EPANET PARSER
# ============================================================================

# EPANET uses very large negative values to indicate errors (disconnected nodes, etc.)
INVALID_PRESSURE_THRESHOLD = -1000.0

def parse_epanet_timeseries(filepath):
    """
    Parse EPANET Time Series export (Excel, CSV, or TXT).
    
    EPANET format typically has:
    - Row 0: Title
    - Row 1: Headers (Series, Time, Pressure)
    - Row 2+: Data with node name repeated in column 1
    
    Handles files with multiple nodes concatenated together.
    Filters out invalid EPANET error values (< -1000 psi).
    
    Returns: DataFrame with Time as index, node names as columns
    """
    filepath = Path(filepath)
    
    # Read raw data
    if filepath.suffix.lower() in ['.xlsx', '.xls']:
        df_raw = pd.read_excel(filepath, header=None)
    elif filepath.suffix.lower() == '.txt':
        # Tab or whitespace delimited text file - use flexible whitespace separator
        df_raw = pd.read_csv(filepath, header=None, sep=r'\s+', engine='python')
    else:
        df_raw = pd.read_csv(filepath, header=None)
    
    # Find the data start row (look for rows starting with "Node")
    data_start = 0
    for i, row in df_raw.iterrows():
        try:
            # Check if first column is "Node" (EPANET format)
            if str(row.iloc[0]).strip() == 'Node':
                data_start = i
                break
            # Fallback: check if second column looks like time (numeric)
            float(row.iloc[1])
            data_start = i
            break
        except (ValueError, TypeError, IndexError):
            continue
    
    # Determine column layout based on first data row
    first_row = df_raw.iloc[data_start]
    if str(first_row.iloc[0]).strip() == 'Node':
        # Format: Node, NodeName, Time, Pressure (4+ columns)
        # Extract all data rows
        data_rows = df_raw.iloc[data_start:].copy()
        data_rows = data_rows[data_rows.iloc[:, 0] == 'Node']  # Keep only "Node" rows
        
        node_names = data_rows.iloc[:, 1].astype(str).str.strip()
        times = pd.to_numeric(data_rows.iloc[:, 2], errors='coerce')
        pressures = pd.to_numeric(data_rows.iloc[:, 3], errors='coerce')
        
        # Build a dataframe with all data
        all_data = pd.DataFrame({
            'NodeName': node_names.values,
            'Time': times.values,
            'Pressure': pressures.values
        }).dropna()
        
        # Filter out invalid EPANET error values
        valid_mask = all_data['Pressure'] > INVALID_PRESSURE_THRESHOLD
        invalid_count = (~valid_mask).sum()
        if invalid_count > 0:
            invalid_nodes = all_data[~valid_mask]['NodeName'].unique()
            print(f"    ⚠ Filtered {invalid_count} invalid readings from nodes: {', '.join(invalid_nodes)}")
        all_data = all_data[valid_mask]
        
        # Pivot to get nodes as columns
        unique_nodes = all_data['NodeName'].unique().tolist()
        df = all_data.pivot_table(index='Time', columns='NodeName', values='Pressure', aggfunc='first')
        df.index.name = 'Time (hours)'
        
        return df, unique_nodes
    else:
        # Original format: NodeName, Time, Pressure (3 columns)
        node_name = str(first_row.iloc[0]).replace('Node ', '').strip()
        times = pd.to_numeric(df_raw.iloc[data_start:, 1], errors='coerce')
        pressures = pd.to_numeric(df_raw.iloc[data_start:, 2], errors='coerce')
        
        # Create clean dataframe
        df = pd.DataFrame({
            'Time': times.values,
            node_name: pressures.values
        })
        
        df = df.dropna()
        
        # Filter out invalid EPANET error values
        valid_mask = df[node_name] > INVALID_PRESSURE_THRESHOLD
        invalid_count = (~valid_mask).sum()
        if invalid_count > 0:
            print(f"    ⚠ Filtered {invalid_count} invalid readings from {node_name}")
        df = df[valid_mask]
        
        df = df.set_index('Time')
        df.index.name = 'Time (hours)'
        
        return df, [node_name]

def combine_node_data(filepaths):
    """
    Combine multiple EPANET exports into one DataFrame.
    Handles files with single or multiple nodes.
    Adds file-based suffix to handle duplicate node names across files.
    """
    combined = None
    nodes = []
    file_index = 0
    
    for fp in filepaths:
        try:
            df, node_names = parse_epanet_timeseries(fp)
            
            # If multiple files, add suffix to avoid column name conflicts
            if len(filepaths) > 1:
                suffix = f"_f{file_index + 1}"
                df.columns = [f"{col}{suffix}" for col in df.columns]
                renamed_nodes = [f"{n}{suffix}" for n in node_names]
            else:
                renamed_nodes = node_names
            
            nodes.extend(renamed_nodes)
            
            if combined is None:
                combined = df
            else:
                # Merge on time index
                combined = combined.join(df, how='outer')
            
            node_list = ', '.join(node_names) if isinstance(node_names, list) else node_names
            print(f"  ✓ Loaded: {node_list} from {Path(fp).name}")
            file_index += 1
        except Exception as e:
            print(f"  ✗ Error loading {fp}: {e}")
    
    return combined, nodes

# ============================================================================
# CHART GENERATION
# ============================================================================

def create_overlay_chart(df, title, output_path, scenario=""):
    """Multi-node overlay with compliance threshold."""
    fig, ax = plt.subplots(figsize=(12, 7))
    
    for i, col in enumerate(df.columns):
        color = NODE_COLORS[i % len(NODE_COLORS)]
        ax.plot(df.index, df[col], label=col, color=color, linewidth=1.5)
    
    # Compliance threshold
    ax.axhline(y=COMPLIANCE_THRESHOLD, color=COLORS['threshold'],
               linestyle='--', linewidth=2.5, 
               label=f'Compliance Threshold ({COMPLIANCE_THRESHOLD} psi)')
    
    # Shade non-compliance zone
    ymin, ymax = ax.get_ylim()
    ax.axhspan(ymin, COMPLIANCE_THRESHOLD, color=COLORS['threshold'], alpha=0.1)
    ax.set_ylim(ymin, ymax)
    
    ax.set_xlabel('Time (hours)', fontsize=12, fontweight='bold')
    ax.set_ylabel('Pressure (psi)', fontsize=12, fontweight='bold')
    ax.set_title(title, fontsize=14, fontweight='bold', pad=15)
    
    if scenario:
        ax.text(0.5, 1.02, scenario, transform=ax.transAxes,
                fontsize=11, ha='center', style='italic')
    
    ax.grid(True, alpha=0.3)
    ax.legend(loc='best', fontsize=9)
    
    plt.tight_layout()
    save_figure(fig, output_path)
    return fig

def create_envelope_chart(df, title, output_path, scenario=""):
    """Pressure envelope showing min/max band."""
    fig, ax = plt.subplots(figsize=(12, 7))
    
    p_min = df.min(axis=1)
    p_max = df.max(axis=1)
    p_mean = df.mean(axis=1)
    
    # Envelope
    ax.fill_between(df.index, p_min, p_max,
                    color=COLORS['envelope_fill'], alpha=0.3,
                    label='Pressure Range')
    ax.plot(df.index, p_min, color=COLORS['fail'], linewidth=2,
            label='Minimum (critical)')
    ax.plot(df.index, p_max, color=COLORS['pass'], linewidth=1.5,
            linestyle='--', label='Maximum')
    ax.plot(df.index, p_mean, color=COLORS['envelope_edge'], linewidth=1.5,
            linestyle=':', label='Mean')
    
    # Threshold
    ax.axhline(y=COMPLIANCE_THRESHOLD, color=COLORS['threshold'],
               linestyle='--', linewidth=2.5, alpha=0.8,
               label=f'Threshold ({COMPLIANCE_THRESHOLD} psi)')
    
    # Find first failure
    failure_mask = p_min < COMPLIANCE_THRESHOLD
    if failure_mask.any():
        t_fail = df.index[failure_mask][0]
        ax.axvline(x=t_fail, color=COLORS['threshold'], linestyle='-',
                   linewidth=1.5, alpha=0.7)
        ax.annotate(f'First Failure\nt = {t_fail:.2f} hrs',
                    xy=(t_fail, COMPLIANCE_THRESHOLD),
                    xytext=(t_fail + 0.15, COMPLIANCE_THRESHOLD + 5),
                    fontsize=10, color=COLORS['threshold'],
                    arrowprops=dict(arrowstyle='->', color=COLORS['threshold']))
    
    ax.set_xlabel('Time (hours)', fontsize=12, fontweight='bold')
    ax.set_ylabel('Pressure (psi)', fontsize=12, fontweight='bold')
    ax.set_title(title, fontsize=14, fontweight='bold', pad=15)
    
    # Stats box
    stats = f"Min: {p_min.min():.1f} psi\nMax: {p_max.max():.1f} psi\nNodes: {len(df.columns)}"
    ax.text(0.02, 0.98, stats, transform=ax.transAxes, fontsize=10,
            verticalalignment='top',
            bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
    
    ax.grid(True, alpha=0.3)
    ax.legend(loc='upper right', fontsize=9)
    
    plt.tight_layout()
    save_figure(fig, output_path)
    return fig

def create_timeline_chart(df, title, output_path, scenario=""):
    """Dual-panel compliance timeline."""
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8),
                                    height_ratios=[2, 1], sharex=True)
    
    p_min = df.min(axis=1)
    compliant = (df >= COMPLIANCE_THRESHOLD).sum(axis=1)
    compliance_pct = (compliant / len(df.columns)) * 100
    
    # Top: Minimum pressure
    ax1.plot(df.index, p_min, color=COLORS['envelope_edge'], linewidth=2,
             label='Minimum System Pressure')
    ax1.axhline(y=COMPLIANCE_THRESHOLD, color=COLORS['threshold'],
                linestyle='--', linewidth=2,
                label=f'Threshold ({COMPLIANCE_THRESHOLD} psi)')
    ax1.fill_between(df.index, p_min, COMPLIANCE_THRESHOLD,
                     where=(p_min < COMPLIANCE_THRESHOLD),
                     color=COLORS['threshold'], alpha=0.3)
    ax1.set_ylabel('Pressure (psi)', fontsize=11, fontweight='bold')
    ax1.legend(loc='upper right', fontsize=9)
    ax1.grid(True, alpha=0.3)
    ax1.set_title(title, fontsize=14, fontweight='bold', pad=10)
    
    # Bottom: Compliance percentage
    ax2.fill_between(df.index, compliance_pct, color=COLORS['envelope_fill'], alpha=0.5)
    ax2.plot(df.index, compliance_pct, color=COLORS['envelope_edge'], linewidth=2)
    ax2.axhline(y=100, color=COLORS['pass'], linestyle='--',
                linewidth=1.5, alpha=0.7, label='100% Compliant')
    ax2.set_ylabel('Nodes Compliant (%)', fontsize=11, fontweight='bold')
    ax2.set_xlabel('Time (hours)', fontsize=11, fontweight='bold')
    ax2.set_ylim(0, 105)
    ax2.legend(loc='lower right', fontsize=9)
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    save_figure(fig, output_path)
    return fig

def save_figure(fig, output_path):
    """Save figure as PNG and PDF."""
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Use string concatenation instead of with_suffix() to avoid issues
    # with filenames containing periods (e.g., "0.14_GPM_Baseline")
    base_path = str(output_path)
    png_path = base_path + '.png'
    pdf_path = base_path + '.pdf'
    
    fig.savefig(png_path, dpi=FIGURE_DPI,
                bbox_inches='tight', facecolor='white')
    fig.savefig(pdf_path,
                bbox_inches='tight', facecolor='white')
    print(f"  ✓ Saved: {png_path}")
    print(f"  ✓ Saved: {pdf_path}")

# ============================================================================
# SUMMARY REPORT
# ============================================================================

def generate_summary(df, scenario=""):
    """Generate text summary of compliance analysis."""
    p_min = df.min(axis=1)
    p_max = df.max(axis=1)
    
    lines = []
    lines.append("=" * 60)
    lines.append("COMPLIANCE ANALYSIS SUMMARY")
    if scenario:
        lines.append(f"Scenario: {scenario}")
    lines.append("=" * 60)
    lines.append(f"Duration: {df.index.min():.2f} - {df.index.max():.2f} hours")
    lines.append(f"Nodes: {len(df.columns)}")
    lines.append(f"Time Steps: {len(df.index)}")
    lines.append("")
    lines.append(f"Minimum Pressure: {p_min.min():.2f} psi")
    lines.append(f"Maximum Pressure: {p_max.max():.2f} psi")
    lines.append(f"Compliance Threshold: {COMPLIANCE_THRESHOLD} psi")
    lines.append("")
    
    failure_mask = p_min < COMPLIANCE_THRESHOLD
    if failure_mask.any():
        t_fail = df.index[failure_mask][0]
        lines.append(f"RESULT: NON-COMPLIANT")
        lines.append(f"  First failure at: {t_fail:.2f} hours ({t_fail*60:.1f} minutes)")
        lines.append(f"  Minimum reached: {p_min.min():.2f} psi")
    else:
        margin = p_min.min() - COMPLIANCE_THRESHOLD
        lines.append(f"RESULT: COMPLIANT")
        lines.append(f"  Margin above threshold: {margin:.2f} psi")
    
    lines.append("=" * 60)
    return "\n".join(lines)

# ============================================================================
# MAIN
# ============================================================================

def main():
    # Default output directory is next to this script
    script_dir = Path(__file__).parent
    default_output = script_dir / "charts"
    
    parser = argparse.ArgumentParser(
        description='Parse EPANET exports and generate compliance charts')
    parser.add_argument('files', nargs='+', help='EPANET export files (Excel/CSV)')
    parser.add_argument('--scenario', '-s', default='',
                        help='Scenario name for chart titles')
    parser.add_argument('--output', '-o', default=str(default_output),
                        help='Output directory for charts (default: charts/ next to script)')
    
    args = parser.parse_args()
    
    print("=" * 60)
    print("EPANET COMPLIANCE CHART GENERATOR")
    print("=" * 60)
    print()
    
    # Load and combine data
    print("Loading data files:")
    df, nodes = combine_node_data(args.files)
    
    if df is None or df.empty:
        print("ERROR: No valid data loaded!")
        sys.exit(1)
    
    print(f"\nCombined dataset: {len(df.columns)} nodes, {len(df.index)} time steps")
    print(f"Time range: {df.index.min():.2f} - {df.index.max():.2f} hours")
    print()
    
    # Generate charts
    output_dir = Path(args.output)
    scenario = args.scenario or "EPANET Analysis"
    clean_name = scenario.replace(' ', '_').replace('/', '_')
    
    print("Generating charts:")
    
    create_overlay_chart(
        df,
        title=f"Pressure vs Time - {scenario}",
        output_path=output_dir / f"{clean_name}_overlay",
        scenario=scenario
    )
    
    create_envelope_chart(
        df,
        title=f"Pressure Envelope - {scenario}",
        output_path=output_dir / f"{clean_name}_envelope",
        scenario=scenario
    )
    
    create_timeline_chart(
        df,
        title=f"Compliance Timeline - {scenario}",
        output_path=output_dir / f"{clean_name}_timeline",
        scenario=scenario
    )
    
    # Print summary
    print()
    print(generate_summary(df, scenario))
    
    print()
    print(f"Charts saved to: {output_dir.absolute()}")

if __name__ == '__main__':
    main()
