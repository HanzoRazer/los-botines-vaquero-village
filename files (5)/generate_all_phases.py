#!/usr/bin/env python3
"""
Los Botines Vaquero Village - Complete Phase INP Generator
Rebuilds all phase configurations from baseline

Phases:
- Phase 1 (Baseline): 640 gal tank, 20 GPM booster, 2.469" trunks
- Phase 2: 1,280 gal tank, 40 GPM booster
- Phase 3: + Network loops (V14↔V15, V13↔SNT5)
- Phase 4: + Enlarged trunks (4.5"), Hunter's Method compliance

Scenarios per phase:
- 0.14 GPM (Agreed Order)
- 0.60 GPM (TCEQ Minimum)
- 0.75 GPM (RV Park Modified / Hunter 50%)
- 1.25 GPM (Stress Test)
"""

import re
import os
from pathlib import Path

# ============================================================================
# CONFIGURATION
# ============================================================================

# Use script directory as base for relative paths
_SCRIPT_DIR = Path(__file__).parent.resolve()
_PROJECT_ROOT = _SCRIPT_DIR.parent

# Input/Output folder structure
INP_BASE_DIR = _PROJECT_ROOT / 'Los_Botines_All_Phases_INP'
SOURCE_FILE = INP_BASE_DIR / 'PHASE1_AGREED_ORDER' / 'PHASE1_AGREED_ORDER_0.140_GPM.inp'
OUTPUT_DIR = INP_BASE_DIR

NUM_CONNECTIONS = 80

SCENARIOS = [
    {'gpm': 0.14, 'name': 'AGREED_ORDER', 'desc': 'Agreed Order Waiver'},
    {'gpm': 0.60, 'name': 'TCEQ_MINIMUM', 'desc': 'TCEQ Regulatory Minimum'},
    {'gpm': 0.75, 'name': 'RV_PARK_MODIFIED', 'desc': 'RV Park Modified (Hunter 50%)'},
    {'gpm': 1.25, 'name': 'STRESS_TEST', 'desc': 'Stress Test (Theoretical Max)'},
]

PHASES = {
    1: {
        'name': 'BASELINE',
        'desc': 'Baseline System',
        'tank_diameter': 1.50,  # ~640 gal
        'booster_curve': [(0, 80), (20, 60), (30, 40)],  # 20 GPM rated
        'booster_capacity': 20,
        'trunk_diameter': 2.469,
        'loops': False,
        'upgrades': [
            'Pressure Tank: 640 gallons (38-60 psi operating range)',
            'Well Pump: 20 GPM (source replenishment)',
            'Booster Pump: 20 GPM (distribution delivery)',
            'Trunk Diameter: 2.469 inches (nominal 2.5")',
        ]
    },
    2: {
        'name': 'STORAGE_UPGRADE',
        'desc': 'Storage & Pump Capacity Upgrade',
        'tank_diameter': 2.10,  # ~1,280 gal
        'booster_curve': [(0, 80), (40, 60), (60, 40)],  # 40 GPM rated
        'booster_capacity': 40,
        'trunk_diameter': 2.469,
        'loops': False,
        'upgrades': [
            'Pressure Tank: 1,280 gallons (DOUBLED from 640)',
            'Well Pump: 20 GPM (unchanged)',
            'Booster Pump: 40 GPM (DOUBLED from 20)',
            'Trunk Diameter: 2.469 inches (unchanged)',
        ]
    },
    3: {
        'name': 'NETWORK_LOOPS',
        'desc': 'Network Loops Added',
        'tank_diameter': 2.10,
        'booster_curve': [(0, 80), (40, 60), (60, 40)],
        'booster_capacity': 40,
        'trunk_diameter': 2.469,
        'loops': True,
        'loop_pipes': [
            # (pipe_id, node1, node2, length, diameter, roughness)
            ('P_LOOP_V14_V15', 'J_V14_OUT', 'J_V15_IN', 400.0, 2.469, 130.0),
            ('P_LOOP_V13_SNT5', 'J_V13_OUT', 'J_SNT5_BEND_IN_130', 75.0, 2.469, 130.0),
        ],
        'upgrades': [
            'Pressure Tank: 1,280 gallons',
            'Booster Pump: 40 GPM',
            'ADDED: Loop V14↔V15 (400 ft)',
            'ADDED: Loop V13↔SNT5 (75 ft)',
            'Trunk Diameter: 2.469 inches',
        ]
    },
    4: {
        'name': 'TRUNK_ENLARGEMENT',
        'desc': 'Trunk Line Enlargement + Hunter Method',
        'tank_diameter': 2.10,
        'booster_curve': [(0, 80), (40, 60), (60, 40)],
        'booster_capacity': 40,
        'trunk_diameter': 4.50,  # Enlarged
        'loops': True,
        'loop_pipes': [
            ('P_LOOP_V14_V15', 'J_V14_OUT', 'J_V15_IN', 400.0, 2.469, 130.0),
            ('P_LOOP_V13_SNT5', 'J_V13_OUT', 'J_SNT5_BEND_IN_130', 75.0, 2.469, 130.0),
        ],
        'upgrades': [
            'Pressure Tank: 1,280 gallons',
            'Booster Pump: 40 GPM',
            'Network Loops: V14↔V15, V13↔SNT5',
            'SNT1/SNT2 Trunk: 4.5 inches (ENLARGED from 2.469)',
            'Design Method: Hunter\'s Probabilistic Approach',
        ]
    }
}

# ============================================================================
# MODIFICATION FUNCTIONS
# ============================================================================

def update_title(content, phase_num, phase_info, scenario):
    """Update the [TITLE] section."""
    gpm = scenario['gpm']
    total_demand = gpm * NUM_CONNECTIONS
    
    upgrades_text = '\n'.join([f'- {u}' for u in phase_info['upgrades']])
    
    # Hunter's method note for Phase 4
    hunter_note = ""
    if phase_num == 4:
        hunter_note = """
DESIGN METHODOLOGY: Hunter's Probabilistic Demand Estimation
- Based on fixture unit analysis (486 total f/u)
- 99th percentile demand per Hunter's Curve
- 50% RV Park transient adjustment applied
- Ref: PDHonline M126 (Bhatia 2020), Hunter BMS 65 (1940)
"""
    
    new_title = f"""[TITLE]
Los Botines Vaquero Village - Water Distribution System
PHASE {phase_num} - {phase_info['desc']}
Scenario: {scenario['desc']} ({gpm:.2f} GPM)

PHASE {phase_num} CONFIGURATION:
{upgrades_text}

TEST PARAMETERS:
- Service Connections: {NUM_CONNECTIONS}
- Flow Rate: {gpm:.2f} GPM per connection
- Total System Demand: {total_demand:.2f} GPM
- Booster Capacity: {phase_info['booster_capacity']} GPM
- Demand/Capacity Ratio: {total_demand/phase_info['booster_capacity']*100:.0f}%
{hunter_note}
"""
    
    content = re.sub(
        r'\[TITLE\].*?\[JUNCTIONS\]',
        new_title + '\n[JUNCTIONS]',
        content,
        flags=re.DOTALL
    )
    
    return content

def update_demand(content, gpm):
    """Update customer node demands."""
    # Update pattern multiplier
    pattern_section = f"""[PATTERNS]
;ID              \tMultipliers
;--- Demand Pattern: {gpm:.2f} GPM per connection ---
 DailyUse        \t{gpm:.2f}\t{gpm:.2f}\t{gpm:.2f}\t{gpm:.2f}\t{gpm:.2f}\t{gpm:.2f}
 DailyUse        \t{gpm:.2f}\t{gpm:.2f}\t{gpm:.2f}\t{gpm:.2f}\t{gpm:.2f}\t{gpm:.2f}
 DailyUse        \t{gpm:.2f}\t{gpm:.2f}\t{gpm:.2f}\t{gpm:.2f}\t{gpm:.2f}\t{gpm:.2f}
 DailyUse        \t{gpm:.2f}\t{gpm:.2f}\t{gpm:.2f}\t{gpm:.2f}\t{gpm:.2f}\t{gpm:.2f}

"""
    
    content = re.sub(
        r'\[PATTERNS\].*?\[CURVES\]',
        pattern_section + '[CURVES]',
        content,
        flags=re.DOTALL
    )
    
    return content

def update_tank(content, diameter):
    """Update tank diameter for storage capacity."""
    # Tank T1 line format: T1 Elev InitLevel MinLevel MaxLevel Diameter MinVol
    # Change diameter from 1.50 to new value
    
    content = re.sub(
        r'(T1\s+[\d.]+\s+[\d.]+\s+[\d.]+\s+[\d.]+\s+)[\d.]+(\s+)',
        f'\\g<1>{diameter:.2f}\\2',
        content
    )
    
    # Update comment about tank volume
    if diameter >= 2.0:
        vol_comment = f";--- D={diameter:.2f}ft gives ~1280 gal between 87.78-138.6 ft (38-60 psi) ---"
    else:
        vol_comment = f";--- D={diameter:.2f}ft gives ~640 gal between 87.78-138.6 ft (38-60 psi) ---"
    
    content = re.sub(
        r';--- D=[\d.]+ft gives ~\d+ gal.*?---',
        vol_comment,
        content
    )
    
    return content

def update_booster_curve(content, curve_points):
    """Update booster pump curve."""
    curve_lines = '\n'.join([f' BOOST_CURVE     \t{flow}\t{head}' for flow, head in curve_points])
    
    # Find and replace BOOST_CURVE entries
    content = re.sub(
        r';--- Booster Pump Curve.*?(?=\n\n|\[)',
        f';--- Booster Pump Curve ({curve_points[1][0]} GPM @ {curve_points[1][1]} ft) ---\n{curve_lines}\n',
        content,
        flags=re.DOTALL
    )
    
    return content

def update_trunk_diameter(content, new_diameter):
    """Update SNT1 and SNT2 trunk pipe diameters."""
    # Match pipes that contain SNT1 or SNT2 in their ID
    # Pipe format: ID Node1 Node2 Length Diameter Roughness MinorLoss Status
    
    def replace_trunk_diameter(match):
        pipe_id = match.group(1)
        rest_before_diam = match.group(2)
        old_diam = match.group(3)
        rest_after = match.group(4)
        
        # Only change if it's a trunk pipe (SNT1 or SNT2) and has the old diameter
        if ('SNT1' in pipe_id or 'SNT2' in pipe_id) and float(old_diam) == 2.469:
            return f'{pipe_id}{rest_before_diam}{new_diameter:.3f}{rest_after}'
        return match.group(0)
    
    # This regex is tricky - we need to identify pipe lines
    # Format: P_xxx... Node1 Node2 Length Diameter ...
    content = re.sub(
        r'(P_\S*SNT[12]\S*\s+\S+\s+\S+\s+[\d.]+\s+)(2\.469)(\s+)',
        lambda m: f'{m.group(1)}{new_diameter:.3f}{m.group(3)}',
        content
    )
    
    # Also update the main trunk connection from manifold
    content = re.sub(
        r'(J_M1_SNT1_160\s+\S+\s+\S+\s+[\d.]+\s+)(2\.469)(\s+)',
        lambda m: f'{m.group(1)}{new_diameter:.3f}{m.group(3)}',
        content
    )
    
    return content

def add_network_loops(content, loop_pipes):
    """Add loop pipes to the network."""
    if not loop_pipes:
        return content
    
    # Find the end of [PIPES] section and add loop pipes
    loop_lines = "\n;--- Network Loops for Redundancy ---\n"
    for pipe in loop_pipes:
        pipe_id, node1, node2, length, diameter, roughness = pipe
        loop_lines += f" {pipe_id}\t{node1}\t{node2}\t{length:.2f}\t{diameter:.3f}\t{roughness:.2f}\t0.00\tOpen\t;\n"
    
    # Insert before [PUMPS] section
    content = re.sub(
        r'(\n\[PUMPS\])',
        loop_lines + '\n\\1',
        content
    )
    
    return content

def update_report_section(content):
    """Ensure comprehensive reporting is enabled."""
    report_section = """[REPORT]
 Status             \tFull
 Summary            \tYes
 Page               \t0
 Energy             \tYes
 Nodes              \tALL
 Links              \tALL
 PRESSURE           \tPRECISION 2
 HEAD               \tPRECISION 2
 DEMAND             \tPRECISION 4
 FLOW               \tPRECISION 4
 VELOCITY           \tPRECISION 3
 HEADLOSS           \tPRECISION 4

"""
    
    content = re.sub(
        r'\[REPORT\].*?\[OPTIONS\]',
        report_section + '[OPTIONS]',
        content,
        flags=re.DOTALL
    )
    
    return content

# ============================================================================
# MAIN GENERATOR
# ============================================================================

def generate_phase_scenario(source_content, phase_num, scenario):
    """Generate a single phase/scenario INP file."""
    phase_info = PHASES[phase_num]
    
    content = source_content
    
    # Apply modifications in order
    content = update_title(content, phase_num, phase_info, scenario)
    content = update_demand(content, scenario['gpm'])
    content = update_tank(content, phase_info['tank_diameter'])
    content = update_booster_curve(content, phase_info['booster_curve'])
    content = update_report_section(content)
    
    # Phase-specific modifications
    if phase_info.get('loops') and phase_info.get('loop_pipes'):
        content = add_network_loops(content, phase_info['loop_pipes'])
    
    if phase_num == 4:
        content = update_trunk_diameter(content, phase_info['trunk_diameter'])
    
    return content

def main():
    # Create output directory
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # Read source file
    with open(SOURCE_FILE, 'r') as f:
        source_content = f.read()
    
    print("=" * 80)
    print("LOS BOTINES VAQUERO VILLAGE - PHASE INP GENERATOR")
    print("=" * 80)
    print()
    
    generated_files = []
    
    for phase_num in sorted(PHASES.keys()):
        phase_info = PHASES[phase_num]
        
        print(f"\n{'─' * 80}")
        print(f"PHASE {phase_num}: {phase_info['desc']}")
        print(f"{'─' * 80}")
        
        for scenario in SCENARIOS:
            gpm = scenario['gpm']
            total = gpm * NUM_CONNECTIONS
            
            # Generate content
            content = generate_phase_scenario(source_content, phase_num, scenario)
            
            # Create filename
            filename = f"PHASE{phase_num}_{scenario['name']}_{gpm:.3f}_GPM.inp"
            filepath = os.path.join(OUTPUT_DIR, filename)
            
            # Save file
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            
            generated_files.append({
                'phase': phase_num,
                'scenario': scenario['name'],
                'gpm': gpm,
                'total': total,
                'capacity': phase_info['booster_capacity'],
                'filename': filename
            })
            
            ratio = total / phase_info['booster_capacity'] * 100
            status = "✅" if ratio <= 100 else "⚠️" if ratio <= 150 else "❌"
            print(f"  {status} {filename}")
            print(f"      Demand: {total:.2f} GPM | Capacity: {phase_info['booster_capacity']} GPM | Ratio: {ratio:.0f}%")
    
    # Summary table
    print("\n" + "=" * 80)
    print("GENERATION SUMMARY")
    print("=" * 80)
    print(f"\nTotal files generated: {len(generated_files)}")
    print(f"Output directory: {OUTPUT_DIR}")
    
    print("\n" + "─" * 100)
    print(f"{'Phase':<8} {'Scenario':<20} {'GPM/CNT':<10} {'Total':<10} {'Capacity':<10} {'Ratio':<10} {'Status'}")
    print("─" * 100)
    
    for f in generated_files:
        ratio = f['total'] / f['capacity'] * 100
        if ratio <= 100:
            status = "PASS"
        elif ratio <= 150:
            status = "MARGINAL"
        else:
            status = "FAIL"
        
        print(f"{f['phase']:<8} {f['scenario']:<20} {f['gpm']:<10.2f} {f['total']:<10.2f} {f['capacity']:<10} {ratio:<10.0f}% {status}")
    
    print("─" * 100)
    
    print("\n" + "=" * 80)
    print("PHASE CONFIGURATION SUMMARY")
    print("=" * 80)
    
    for phase_num, phase_info in PHASES.items():
        print(f"\nPhase {phase_num}: {phase_info['desc']}")
        for upgrade in phase_info['upgrades']:
            print(f"  • {upgrade}")
    
    print("\n✓ All files ready for EPANET simulation!")

if __name__ == '__main__':
    main()
