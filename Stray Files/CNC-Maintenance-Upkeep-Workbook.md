# CNC Machine Maintenance & Upkeep Workbook
## A Comprehensive Guide for Hobbyist CNC Operators

**Version 1.0** | Created: November 15, 2025  
**Source**: Sienci Labs Resources Repository (Forked by HANZORAZER)  
**License**: CC BY-SA 4.0

---

## Table of Contents

1. [Introduction](#introduction)
2. [Safety First](#safety-first)
3. [Understanding Your CNC Machine](#understanding-your-cnc-machine)
4. [Maintenance Schedule Overview](#maintenance-schedule-overview)
5. [Tools & Supplies Required](#tools--supplies-required)
6. [Routine Maintenance Procedures](#routine-maintenance-procedures)
7. [Troubleshooting Common Issues](#troubleshooting-common-issues)
8. [Consumable Parts Replacement](#consumable-parts-replacement)
9. [Maintenance Logs & Checklists](#maintenance-logs--checklists)
10. [Alarm & Error Code Reference](#alarm--error-code-reference)
11. [Advanced Tuning & Optimization](#advanced-tuning--optimization)
12. [Resources & Further Reading](#resources--further-reading)

---

## Introduction

### Why Maintenance Matters

All CNC machines require regular maintenance to ensure:
- **Precision**: Maintain cutting accuracy over time
- **Longevity**: Extend the life of your machine and components
- **Safety**: Prevent accidents caused by mechanical failures
- **Performance**: Keep your machine running at peak efficiency
- **Cost savings**: Catch problems early before they become expensive repairs

Regular checkups ensure that issues are caught before they affect your projects, and your machine will run at the top of its game for many years.

### About This Workbook

This workbook consolidates maintenance best practices from Sienci Labs' extensive CNC documentation, adapted for general hobbyist CNC machines. While examples reference specific products (LongMill MK2, Mill One, Vortex), the principles apply universally to:

- Hobby CNC routers with V-wheel gantry systems
- Lead screw-driven machines
- Linear rail systems
- ACME thread anti-backlash systems
- grbl and grblHAL-based controllers

### How to Use This Workbook

1. **Read the safety section** before operating your machine
2. **Identify your maintenance schedule** based on usage patterns
3. **Follow procedures step-by-step** with appropriate tools
4. **Log all maintenance activities** in the tracking section
5. **Reference troubleshooting** when issues arise
6. **Keep this workbook** near your CNC workspace

---

## Safety First

### General Safety Guidelines

When working with your CNC machine, noise and dust can be just as dangerous as cutting tools. Follow these essential safety practices:

#### Personal Protective Equipment (PPE)

**ALWAYS WEAR:**
- ✓ **Safety glasses or goggles** - Chips and fine dust fly unpredictably
- ✓ **Dust mask or respirator** (minimum N95) - Some materials release toxic dust or fumes
- ✓ **Ear protection** - CNCs with dust collection can exceed 85dB
- ✓ **Proper footwear** - Closed-toe shoes, no sandals

**NEVER WEAR:**
- ✗ Loose clothing or jewelry
- ✗ Long sleeves near moving parts (roll them up)
- ✗ Dangling hair (tie it back)

#### Operational Safety Rules

1. **Stay alert** - Never operate when tired, distracted, or impaired
2. **Never leave machine unattended** - Unexpected movements or tool failures happen quickly
3. **Never lean on or rest hands on machine during operation**
4. **Assume sudden movement** - Machine can jerk rapidly during G0 movements
5. **Pause before adjusting** - Use push sticks, never your hands
6. **Handle tools carefully** - Cutting tools can shatter or cut skin
7. **Dispose responsibly** - Materials may ignite in dust collection or disposal

#### Material-Specific Hazards

- **Check MSDS sheets** for toxic materials
- **Never mix metal dust with wood dust** - Hot metal chips can ignite sawdust
- **Avoid cutting unknown materials** - They may release toxic fumes
- **Be aware of fire hazards** - Especially with dust collection bins

> **⚠️ CRITICAL WARNING**: The machine can move at high speed during rapid movements. A big hazard is how fast the machine can suddenly jerk to a different position. Best scenario is to never put your hands near moving parts during a job.

---

## Understanding Your CNC Machine

### Key Components for Maintenance

#### Motion System
- **V-wheels**: Roll on rails, held by eccentric nuts for tension adjustment
- **Eccentric nuts**: Off-center nuts that allow V-wheel tension adjustment
- **Rails**: Linear guides (X and Y axes typically use steel rails)
- **Linear guides**: Z-axis precision rails with sealed bearings

#### Drive System
- **Lead screws**: ACME threaded rods (T8 or T12 pitch)
- **Anti-backlash nuts**: Delrin or spring-loaded nuts that eliminate play
- **Couplers**: Connect stepper motors to lead screws
- **Stepper motors**: Provide precise motion control

#### Structural Components
- **Gantry plates**: X-axis and Y-axis mounting plates
- **Z-axis assembly**: Vertical movement system
- **Frame**: Base rails and support structure
- **Router/spindle mount**: Holds cutting tool

#### Fasteners & Hardware
- **M5 bolts**: Primary structural fasteners
- **M3 screws**: Linear rail and plate mounting
- **Set screws**: Coupler and locking nut retention
- **Nylock nuts**: Self-locking nuts to resist vibration
- **Spring washers**: Additional vibration resistance

---

## Maintenance Schedule Overview

### Maintenance Frequency Guide

Maintenance frequency depends on several factors:
- **Dust collection effectiveness**: Better collection = less frequent cleaning
- **Material hardness**: Harder materials = more frequent maintenance
- **Production level**: Continuous use = more frequent checks
- **Environmental conditions**: Dusty shops require more attention

#### Light Use Schedule
*Hobby use, good dust collection, soft materials (wood, MDF)*

| Interval | Tasks |
|----------|-------|
| **Every 10-20 hours** | Clean rails & V-wheels, check eccentric nuts, tension anti-backlash nuts |
| **Every 20-30 hours** | Lubricate linear guides, check loose hardware |
| **Every 50 hours** | Deep clean entire machine, inspect belts |
| **Every 1,500-2,000 hours** | Replace V-wheels and anti-backlash nuts (consumables) |

#### Heavy Use Schedule
*Production work, poor dust collection, hard materials (aluminum, hardwoods)*

| Interval | Tasks |
|----------|-------|
| **Every 5-10 hours** | Clean rails & V-wheels, check eccentric nuts |
| **Every 10-15 hours** | Tension anti-backlash nuts, lubricate linear guides |
| **Every 20-30 hours** | Check all hardware, inspect couplers |
| **Every 30 hours** | Deep clean and full inspection |
| **Every 1,000-1,500 hours** | Replace consumables earlier due to wear |

#### Pre-Operation Checklist (Every Use)
- [ ] Visual inspection for loose parts or damage
- [ ] Check router/spindle mounting security
- [ ] Verify power connections
- [ ] Test E-stop functionality
- [ ] Clear work area of debris
- [ ] Ensure proper dust collection setup

#### Post-Operation Checklist (Every Use)
- [ ] Power down properly (not during movement)
- [ ] Remove dust and chips from work area
- [ ] Vacuum around machine components
- [ ] Store cutting tools properly
- [ ] Check for any unusual wear or sounds noted during operation

---

## Tools & Supplies Required

### Essential Maintenance Tools

#### Hand Tools
- **Allen key set** (metric: M3, M5 most common)
- **LongMill wrench** or adjustable wrench (for eccentric nuts)
- **Small flathead screwdriver** (for terminal connectors)
- **Phillips screwdriver** (various sizes)
- **Needle-nose pliers**
- **Wire cutters/strippers** (for electrical work)
- **Calipers or ruler** (for measurements)
- **Multimeter** (for electrical diagnostics)

#### Cleaning Supplies
- **Small brushes** (wire brush, brass brush, toothbrush)
- **Plastic scrapers** (won't damage rails)
- **Compressed air** or air compressor
- **Shop vacuum** (dedicated for CNC)
- **Clean rags** or shop towels
- **Paper towels**
- **Isopropyl alcohol** (for cleaning electronic contacts)

#### Lubrication & Maintenance Materials
- **3-in-1 oil** or general-purpose machine oil
- **Lithium grease** (for linear bearings)
- **Thread locker** (blue Loctite for set screws)
- **Cotton swabs** (for precise cleaning)
- **Degreaser** (for heavy buildup)

**❌ AVOID:**
- Dry lubricants
- Graphite-based lubricants
- WD-40 (not a lubricant, breaks down oils)
- Particulate-containing lubricants

#### Safety Equipment
- **Safety glasses**
- **Dust mask/respirator (N95 minimum)**
- **Ear protection** (plugs or muffs)
- **Work gloves** (for handling sharp components)
- **First aid kit**

#### Diagnostic Tools (Optional but Helpful)
- **Dial indicator** (for tramming and precision checks)
- **Feeler gauges** (for gap measurements)
- **Flashlight or headlamp** (for inspecting tight spaces)
- **Magnifying glass** (for detailed inspection)
- **Camera/phone** (document issues before and after)

### Consumable Parts Inventory

Keep these on hand for replacements:

- **V-wheels** (check your machine's count: typically 12-16)
- **Anti-backlash nuts** (T8 and/or T12 depending on machine)
- **Bearings** (608 or 625 type, depending on V-wheels)
- **Set screws** (M3 and M5 sizes)
- **Spare M5 bolts and nuts**
- **Spare stepper motor cables**
- **Spare limit switch cables** (if equipped)
- **Router brushes** (for router-based spindles)
- **Fuses** (for power supply and controller)

---

## Routine Maintenance Procedures

### 1. Cleaning Rails and V-Wheels

**Frequency**: Every 10-20 hours (light use) or 5-10 hours (heavy use)

**Why**: Over time, black splotches appear on rails and grey buildup accumulates on wheels. This happens when ambient dust settles on rail edges and wheels repeatedly roll over it, creating friction and reducing smooth movement.

#### Procedure:

1. **Power down the machine** completely
2. **Inspect the rails** on all axes (X, Y, Z)
   - Look for black buildup on rail edges (top and bottom)
   - Note any scratches or damage
3. **Clean the rails**:
   - Use a small brush, plastic scraper, wood scrap, or fingernails
   - Clean both top and bottom rail edges
   - Work in one direction to push debris away
   - Use isopropyl alcohol for stubborn gunk
4. **Clean the V-wheels**:
   - Rotate each wheel by hand to inspect full circumference
   - Look for grey buildup in the groove
   - Remove buildup with fingernails or thin material
   - **Pro tip**: Insert a thin material (playing card, thin plastic) into the top of the wheel groove while rotating to push out gunk along entire circumference
5. **Clean wheel crevices**:
   - Use compressed air to blow out dust from bearing areas
   - Use cotton swabs for detailed cleaning
   - Check both sides of each wheel
6. **Final inspection**:
   - Spin each wheel to ensure smooth rotation
   - Check for any rough spots or resistance
   - Verify rails are clean and smooth to touch

**Signs You Need to Clean More Often**:
- Visible black streaks on rails
- Rough or gritty feeling when manually moving axes
- Increased noise during operation
- Reduced accuracy in cuts

---

### 2. Adjusting Eccentric Nuts (V-Wheel Tensioning)

**Frequency**: Every 10-20 hours or when wheels feel loose/tight

**Why**: Eccentric nuts are "off-center" nuts that allow adjustment of the gap between V-wheels and rails. Proper tension ensures rigid yet smooth motion. Over time, wheels wear and require re-tensioning.

#### Understanding Eccentric Nuts

The eccentric nut has an off-center hole. As you rotate the nut, the distance between the V-wheel and the rail changes:
- **Fully open**: Largest gap (wheel loose)
- **Fully closed**: Smallest gap (wheel tight)
- **Sweet spot**: Can barely turn wheel with fingers

#### The "Sweet Spot" Test

For each V-wheel, test by hand:
- ✓ **CORRECT**: You can barely turn the wheel with your fingers (requires effort)
- ✗ **TOO LOOSE**: Wheel spins freely
- ✗ **TOO TIGHT**: Wheel doesn't turn at all or requires excessive force

**Note**: The top wheel in any pair will always be slightly harder to spin due to gravity.

#### Adjustment Procedure:

**Tools Required**: LongMill wrench (or adjustable wrench), M5 Allen key

1. **Identify eccentric nuts** on your machine:
   - X-axis gantry: 4 wheels (2 with eccentric nuts)
   - Y-axis plates: 4 wheels per side (2 with eccentric nuts each)
   - Z-axis: 4 wheels (2 with eccentric nuts)

2. **Test each wheel** using the "sweet spot" test

3. **For wheels needing adjustment**:
   - **Loosen** the M5 bolt with Allen key (don't remove, just loosen enough to rotate nut)
   - **Rotate** the eccentric nut with the wrench:
     - Clockwise (typically): Brings wheel closer to rail
     - Counter-clockwise: Moves wheel away from rail
   - **Make tiny adjustments** - very small rotation has big impact
   - **Re-tighten** the M5 bolt firmly with Allen key
   - **Re-test** the wheel and its partner wheel on opposite side

4. **Check partner wheels**:
   - Each eccentric wheel has a "static" partner on the opposite side
   - Both must be properly tensioned
   - Adjust as needed

5. **Test axis movement**:
   - Manually move the axis smoothly back and forth
   - Should move with consistent resistance
   - No binding or loose spots

#### Troubleshooting:

- **Can't rotate eccentric nut**: Loosen M5 bolt more
- **Nut rotates but wheel doesn't adjust**: Bolt may be too tight, preventing nut rotation
- **Over-tightened**: Causes premature wear and excessive stress on machine
- **Eccentric adjustment maxed out**: Time to replace V-wheels (see Consumable Parts section)

**⚠️ WARNING**: Over-tightening can cause:
- Premature V-wheel wear
- Increased stress on frame and motors
- Motor stalling or skipped steps
- Reduced accuracy

---

### 3. Adjusting Anti-Backlash Nuts

**Frequency**: Every 10-20 hours or when axis feels loose

**Why**: Anti-backlash nuts eliminate "play" or "wiggle" in the axis. Backlash is the slight movement possible when the lead screw is stationary. Left unchecked, it reduces accuracy and sturdiness.

#### Types of Anti-Backlash Nuts

**White Spring-Loaded Nuts** (Modern):
- Self-adjusting with internal springs
- Require NO manual maintenance
- Replace when they no longer self-adjust (wiggle appears)
- T8 size: Most axes
- T12 size: 48" X-axis machines

**Black Delrin Nuts** (Older):
- Require manual tensioning via M5 screw
- Wear over time, need periodic adjustment
- Eventually wear out and need replacement

#### Testing for Backlash

1. **Power down** or **disconnect USB** (with power on)
2. **Hold the lead screw stationary** (don't let it rotate)
3. **Wiggle the plate/gantry** back and forth
4. **Feel for play**: Any movement while lead screw stays still = backlash

Test all axes:
- X-axis plate
- Both Y-axis plates (left and right)
- Z-axis plate

#### Adjustment Procedure (Black Delrin Nuts Only)

**Tools Required**: M5 Allen key

**⚠️ CRITICAL**: Adjustments must be **TINY** - very small rotation at a time!

1. **Remove dust shield** (if equipped) to access mechanics

2. **Locate tensioning screws**:
   - **Y-axis nuts**: On each Y-axis plate (mirror locations)
   - **X-axis nut**: On X-axis gantry plate
   - **Z-axis nut**: On Z-axis plate

3. **Tension procedure**:
   - Insert M5 Allen key into tensioning screw
   - Rotate clockwise **1/16 turn or less**
   - Test for wiggle again
   - Repeat in tiny increments until wiggle is gone
   - **STOP when wiggle is eliminated** - don't over-tighten

4. **Test axis movement**:
   - Manually rotate lead screw
   - Should move smoothly without binding
   - Check for increased resistance (sign of over-tightening)

5. **Repeat for all axes** showing backlash

#### Understanding How It Works

Tightening the screw **widens the nut** (splits it apart), pressing against the threads of the lead screw more firmly. This eliminates the gap that causes backlash.

#### Replacement Indicators

Replace anti-backlash nuts when:
- ✗ Tensioning screw is fully tightened but wiggle remains
- ✗ M5 bolt head starts rubbing against lead screw threads
- ✗ Visible wear grooves in Delrin material
- ✗ Excessive play that can't be adjusted out

**⚠️ DANGER**: If Delrin is worn excessively, the M5 bolt head can rub or bind against the lead screw and **damage it** (expensive repair). Replace nuts before this happens.

---

### 4. Lubricating Linear Guides (Z-Axis)

**Frequency**: Every 20-30 hours or when you hear grinding/roughness

**Why**: Linear guides have sealed bearings that require periodic lubrication. Grinding noises or rough movement indicates insufficient lubrication. Proper lubrication ensures smooth, quiet, long-lasting operation.

#### Signs You Need to Lubricate

- Grinding or scraping noises during Z-axis movement
- Roughness felt when manually moving Z-axis
- Increased resistance to movement
- Squeaking sounds
- Visible dry/dirty linear rails

#### Lubrication Procedure

**Tools Required**: Machine oil (3-in-1 oil or equivalent), clean cloth, shop towels

**Recommended Lubricants**:
- General-purpose machine oil (3-in-1 oil)
- Light lithium grease
- Dedicated linear bearing oil

**❌ DO NOT USE**:
- WD-40 (displaces existing lubricant)
- Dry lubricants
- Graphite-based lubricants
- Lubricants with particulates

#### Step-by-Step:

1. **Clean first**:
   - Wipe linear guides with clean cloth or paper towel
   - Remove accumulated dust and debris
   - Move Z-axis up and down to expose full rail length
   - Clean the entire visible rail surface

2. **Apply lubricant**:
   - Apply **liberal amount** of machine oil to linear guides
   - Apply along the full length of both rails
   - Don't be stingy - excess will distribute into bearings

3. **Distribute lubricant**:
   - Manually move Z-axis up and down several times
   - Move slowly through full range of motion
   - Repeat 5-10 times to ensure bearings get coated
   - Excess oil will squeeze out (this is normal)

4. **Wipe excess**:
   - Use clean cloth to wipe away excess surface oil
   - Leave a thin film on rails
   - Check for smooth movement

5. **Test**:
   - Move Z-axis through full range
   - Should feel noticeably smoother
   - No grinding or rough spots
   - Consistent resistance throughout travel

#### Additional Resources

For detailed technical information on linear bearing lubrication:
- Thomson Linear: "What Should Be Used to Lubricate Linear Bearings"
- Hiwin: "Lubricating Instructions" (PDF)

#### Maintenance Tips

- Keep a lubrication log (see Maintenance Logs section)
- Increase frequency in dusty environments
- After cleaning, always re-lubricate
- Consider dust boots for additional protection

---

### 5. Checking for Loose Hardware

**Frequency**: Every 20-30 hours

**Why**: Vibrations from cutting slowly loosen bolts and nuts over time, even with nylock nuts and spring washers. Loose hardware can cause:
- Loss of machine position
- Reduced accuracy
- Mechanical failures
- Safety hazards
- Damaged components

#### Hardware Inspection Checklist

**Tool Required**: M3 and M5 Allen keys, appropriate wrenches

#### Set Screws (CRITICAL)

Check tightness of set screws on:
- [ ] **All motor couplers** (usually 2 per coupler)
  - One should contact flat on motor shaft
  - One should contact flat on lead screw
- [ ] **ACME locking nuts** on lead screws
- [ ] **Pulleys** (if equipped with belts)

**⚠️ IMPORTANT**: Set screws are critical for motion transfer. Loose set screws cause:
- Coupler slipping
- Lost position
- Inconsistent movement
- Stripped threads (if allowed to slip repeatedly)

#### Structural Fasteners

##### M5 Bolts/Screws:
- [ ] **Feet mounting** to Y-rails
- [ ] **Y-axis plates** to X-rail
- [ ] **Stepper motor mounting** to steel plates (usually 4 per motor)
- [ ] **Router/spindle mount** (front and rear)
- [ ] **V-wheel bolts** (ensure properly tightened after eccentric adjustments)

##### M3 Screws:
- [ ] **Z-axis steel plate** mounting
- [ ] **Linear rails** to X-axis plate (usually many small screws)
- [ ] **Drag chain mounts** (if equipped)
- [ ] **Limit switch mounting** (if equipped)

#### Electronics and Wiring

- [ ] **Power supply connections** (barrel connector or terminal blocks)
- [ ] **E-stop wiring** (terminal connections)
- [ ] **Stepper motor connectors** (fully seated)
- [ ] **Limit switch connectors** (if equipped)
- [ ] **USB cable** (secure connection)

#### Add-On Hardware (If Equipped)

- [ ] **Dust shoe mounting**
- [ ] **Laser module mounting**
- [ ] **Touch plate connectors**
- [ ] **T-track mounting bolts**
- [ ] **Rotary axis mounting** (Vortex, etc.)

#### Inspection Procedure

1. **Visual inspection first**:
   - Look for obviously loose or missing hardware
   - Check for cracks in plates or mounts
   - Verify nothing is bent or misaligned

2. **Systematic tightening**:
   - Start at one corner of machine
   - Work methodically through all accessible hardware
   - Use appropriate tool for each fastener
   - Apply firm pressure but don't over-torque

3. **Torque considerations**:
   - **Set screws**: Snug, not over-tight (can strip)
   - **Structural bolts**: Firm and secure
   - **Stepper motor mounts**: Tight (loose causes noise)
   - **Delicate components**: Finger-tight plus 1/4 turn

4. **Special attention areas**:
   - Router mount (high vibration area)
   - Motor couplers (critical for accuracy)
   - Y-axis plates (high stress during operation)

5. **Document findings**:
   - Note any hardware that frequently loosens
   - Consider thread locker (blue Loctite) for repeat offenders
   - Log in maintenance records

#### Preventive Measures

- **Blue thread locker** on set screws (removable)
- **Nylock nuts** where possible (self-locking)
- **Spring washers** under bolt heads (vibration resistance)
- **Regular checks** prevent major issues

**⚠️ NOTE**: Some loosening is normal over first 50-100 hours as machine "breaks in". Check more frequently during initial period.

---

### 6. Deep Cleaning and Full Inspection

**Frequency**: Every 50 hours or quarterly (whichever comes first)

**Why**: A thorough deep clean and inspection catches issues before they become problems and keeps your machine in optimal condition.

#### Full Inspection Checklist

##### Mechanical Systems:
- [ ] All V-wheels for wear, flat spots, or cracks
- [ ] Rails for scratches, dings, or damage
- [ ] Lead screws for wear, bends, or debris in threads
- [ ] Anti-backlash nuts for excessive wear
- [ ] Couplers for cracks or deformation
- [ ] Belt tension (if equipped) - proper tension, no fraying
- [ ] Linear guides for smooth operation
- [ ] Motor shafts for any play or wobble

##### Structural:
- [ ] Frame for cracks or stress points
- [ ] Plates for cracks, especially around mounting holes
- [ ] Wasteboard for excessive wear or gouges
- [ ] Machine mounting to table (secure)
- [ ] Leveling of machine (use precision level)

##### Electrical:
- [ ] All wire connections secure
- [ ] Wires for chafing, cuts, or damage
- [ ] Connectors clean and corrosion-free
- [ ] E-stop button functionality
- [ ] Power switch operation (if equipped)
- [ ] Controller LED lights (all functioning)
- [ ] Stepper motors not excessively hot during operation

##### Cutting Tool System:
- [ ] Router/spindle securely mounted
- [ ] Router brushes condition (if equipped)
- [ ] Spindle bearings smooth (no grinding)
- [ ] Router power cable condition
- [ ] Collet condition (clean, not worn)

#### Deep Cleaning Procedure:

1. **Complete disassembly** (optional but thorough):
   - Remove dust shoe and accessories
   - Remove router/spindle
   - Provides access to hard-to-reach areas

2. **Vacuum thoroughly**:
   - All horizontal surfaces
   - Under machine and table
   - Inside motor mounting areas
   - Controller enclosure ventilation

3. **Detailed cleaning**:
   - All rails (see Rail Cleaning section)
   - All V-wheels (see V-wheel Cleaning section)
   - Lead screw threads (brush and compressed air)
   - Linear guides (see Lubrication section)
   - Electrical contacts (isopropyl alcohol on cotton swab)

4. **Degrease if needed**:
   - Heavy buildup on metal surfaces
   - Use appropriate degreaser
   - Rinse/wipe clean
   - Re-lubricate after degreasing

5. **Reassemble and test**:
   - Reinstall components
   - Check all fasteners
   - Test all axes for smooth movement
   - Run test file to verify accuracy

#### Documentation:

Take photos before and after:
- Overall machine condition
- Problem areas
- Wear patterns
- Reference for future maintenance

---

## Troubleshooting Common Issues

### Motor and Movement Issues

#### Motor Not Moving or Moving Erratically

**Symptoms**:
- One or more motors don't respond to commands
- Erratic, stuttering movement
- Motor makes noise but doesn't turn
- Intermittent movement

**Diagnostic Steps**:

1. **Check connections**:
   - Disconnect and reconnect motor plugs (both ends)
   - Verify all wires in connector are secure
   - Check for bent pins or damaged connectors

2. **Swap motor to different axis**:
   - If motor works on different axis = controller issue
   - If motor doesn't work on any axis = motor issue
   - Helps isolate problem

3. **Check controller**:
   - Verify driver LED is illuminated for that axis
   - Check DIP switch settings (microstepping)
   - Verify Arduino is fully seated (if applicable)

4. **Check for mechanical binding**:
   - Manually move axis (motor disconnected)
   - Should move smoothly without excessive force
   - Look for over-tightened wheels or nuts

5. **Verify wiring color pattern**:
   - Standard pattern: Blue, Yellow, Green, Red
   - Compare to working motor
   - Incorrect order causes wrong/no movement

**Solutions**:
- Re-seat all connections
- Correct DIP switch settings
- Adjust mechanical tension
- Replace damaged cables
- Contact manufacturer if controller issue

---

#### Motors Stalling or Skipping Steps

**Symptoms**:
- Motors make grinding noise but don't move
- Machine "loses" position during job
- Only happens at higher speeds or under load

**Diagnostic Steps**:

1. **Check mechanical resistance**:
   - Test each axis by hand (power off)
   - Should move relatively easily
   - Identify which axis has resistance

2. **Check V-wheel tension**:
   - Over-tightened wheels cause excess friction
   - Adjust per V-wheel section
   - Test again after adjustment

3. **Check anti-backlash nuts**:
   - Over-tightened nuts bind on lead screw
   - Back off tension slightly
   - Should move smoothly when tensioned correctly

4. **Check couplers**:
   - Loose set screws cause slipping
   - Tighten set screws (one per flat)
   - Verify coupler not cracked

5. **Check for debris**:
   - Chips in lead screw threads
   - Dust buildup on rails
   - Clean thoroughly

6. **Reduce speed/acceleration**:
   - Lower firmware settings ($110-112 for max rate)
   - Lower acceleration settings ($120-122)
   - Test at reduced speeds

**Solutions**:
- Adjust mechanical components
- Clean drive system
- Reduce speeds/accelerations in firmware
- Verify motor current settings (advanced)

---

#### Machine Moving Wrong Direction

**Symptoms**:
- Axis moves opposite of commanded direction
- Mirrored cuts
- Homing moves away from switches

**Diagnostic Steps**:

1. **Check wire connections**:
   - Verify all motor plugs fully seated
   - Compare wire color patterns between motors
   - Standard: Blue, Yellow, Green, Red

2. **Check firmware settings**:
   - Direction invert settings may be incorrect
   - Use `$$` command to view all settings
   - Compare to manufacturer defaults

**Solutions**:
- Reload default EEPROM settings: `$rst=$`
- Swap two wires in motor connector (reverses direction)
- Check machine profile in controller software
- Power cycle controller after changes

---

#### Machine Not Moving Correct Distance

**Symptoms**:
- Cuts are wrong size
- Squares aren't square
- Measurements don't match g-code

**Diagnostic Steps**:

1. **Check microstepping**:
   - Verify DIP switch settings on drivers
   - Should be 1/8 microstepping (typically)
   - Check manufacturer documentation

2. **Check steps/mm settings**:
   - Use `$$` to view firmware settings
   - $100 (X), $101 (Y), $102 (Z)
   - Compare to manufacturer defaults

3. **Check for mechanical slipping**:
   - Loose couplers (set screws)
   - Worn V-wheels
   - Stripped lead screw threads

4. **Test with precision movement**:
   - Jog 100mm and measure actual travel
   - Calculate error percentage
   - Adjust steps/mm if needed

**Solutions**:
- Correct DIP switches
- Tighten couplers and check set screws
- Adjust firmware steps/mm values
- Replace worn mechanical components

---

### Controller and Electronics Issues

#### Controller Not Powering On

**Symptoms**:
- No LED lights on controller
- No response from machine
- Power supply LED on but controller dead

**Diagnostic Steps**:

1. **Check power supply**:
   - Verify green LED on power brick is lit
   - Test outlet with another device
   - Check power cable connections

2. **Check E-stop** (if equipped):
   - Twist counterclockwise to release
   - Red light should be on when released
   - Verify E-stop wiring in terminal block

3. **Check power switch** (if equipped):
   - Toggle on/off
   - Check internal wiring if accessible

4. **Check polarity**:
   - White wire = positive (typically)
   - Black wire = negative (typically)
   - Try reversing if necessary

5. **Check fuses**:
   - Some controllers have fuses
   - Test with multimeter or swap with known good fuse

**Solutions**:
- Correct power connections
- Replace power supply if faulty
- Release E-stop
- Contact manufacturer if internal controller issue

---

#### Connection/Communication Issues

**Symptoms**:
- Computer doesn't detect CNC
- Frequent disconnections during jobs
- "Port not found" errors

**Diagnostic Steps**:

1. **Check USB cable**:
   - Try different USB cable
   - Try different USB port on computer
   - Avoid USB hubs (use direct connection)
   - Cable length under 15 feet ideal

2. **Check drivers**:
   - Verify USB drivers installed (CH340, FTDI, etc.)
   - Update drivers if available
   - Check device manager for errors

3. **Check for interference**:
   - Route USB away from power cables
   - Use shielded USB cable
   - Ferrite bead on USB cable helps

4. **Try different computer/software**:
   - Isolates computer vs. controller issue
   - Test with different control software

5. **Check controller indicators**:
   - Power LED should be steady
   - Communication LED may blink during data transfer

**Solutions**:
- Use quality shielded USB cable
- Install correct drivers
- Switch to Ethernet if available (grblHAL)
- Minimize cable length
- Add ferrite choke to USB cable

---

### Accuracy and Cut Quality Issues

#### Cuts Not Accurate / Lost Position

**Symptoms**:
- Cuts don't match expected dimensions
- Machine "loses" position during job
- Repeated patterns don't align

**Possible Causes & Solutions**:

1. **Backlash in anti-backlash nuts**:
   - Test and adjust per Anti-backlash section
   - Replace if excessively worn

2. **Loose V-wheels**:
   - Check and adjust eccentric nuts
   - Replace if worn flat

3. **Motor stalling**:
   - See Motor Stalling section
   - Reduce speeds/accelerations

4. **Loose couplers**:
   - Check all set screws
   - Apply thread locker if repeatedly loose

5. **Loose router mount**:
   - Check all mounting bolts
   - Ensure router is firmly clamped

6. **Loose workpiece**:
   - Improve workholding
   - Verify material not shifting

**Diagnostic Test**:
- Cut a precision square (100mm x 100mm)
- Measure with calipers
- Diagonal measurements should be equal
- Identifies which axis has issue

---

#### Rough Surface Finish / Chatter

**Symptoms**:
- Wavy cut surfaces
- Vibration marks in material
- Excessive noise during cutting

**Possible Causes & Solutions**:

1. **Dull or damaged bit**:
   - Inspect cutting edges
   - Replace if chipped or dull
   - Use sharp, quality bits

2. **Incorrect feeds and speeds**:
   - Too fast = rough finish
   - Too slow = burning, melting
   - Consult feeds/speeds tables

3. **Loose mechanical components**:
   - Check all hardware per Loose Hardware section
   - Pay attention to router mount
   - Verify V-wheel tension

4. **Deflection from improper cutting**:
   - Reduce depth of cut
   - Increase stepover (reduce radial engagement)
   - Use climb milling for better finish

5. **Machine not level/stable**:
   - Check table mounting
   - Verify machine sits flat
   - Add weight to table for damping

6. **Router RPM incorrect**:
   - Too low = chattering
   - Match to bit and material
   - Typical range: 10,000-25,000 RPM

---

## Consumable Parts Replacement

### When to Replace Components

#### V-Wheels

**Lifespan**: 1,500-2,000 hours (typical hobby use)

**Replace When**:
- Eccentric nuts can't be rotated further to tighten
- Visible flat spots on wheels
- Cracks in wheel material
- Bearing feels rough or gritty
- Excessive wobble even when tightened

**Replacement Procedure**:

1. **Order correct wheels**:
   - Check bearing size (608 or 625 type)
   - Count wheels needed per axis
   - Order extras for future

2. **Remove old wheel**:
   - Loosen M5 bolt completely
   - Remove bolt, washer, and spacers
   - Note spacer arrangement (photograph)
   - Clean bolt and bearing surfaces

3. **Install new wheel**:
   - Reassemble in reverse order
   - Ensure proper spacer placement
   - Finger-tighten first
   - Adjust eccentric nut to proper tension
   - Fully tighten M5 bolt

4. **Test movement**:
   - Check sweet spot tension
   - Verify smooth rolling
   - Test axis for consistent resistance

**Video Reference**: Bucky's Customs V-wheel replacement guide

---

#### Anti-Backlash Nuts

**Lifespan**: 1,500-2,000 hours (typical hobby use)

**Replace When**:
- Tensioning screw fully tightened but backlash remains
- M5 bolt head contacts/rubs lead screw threads
- Visible wear grooves in Delrin
- Nut splits or cracks
- Spring-loaded nuts no longer self-adjust

**Replacement Procedure**:

1. **Order correct nuts**:
   - **T8 nuts**: Most axes (8mm lead screw, 2mm pitch)
   - **T12 nuts**: 48" X-axis machines (12mm lead screw)
   - Specify Delrin or spring-loaded type
   - Order one spare per axis

2. **Remove old nut**:
   - Remove dust shield (if equipped)
   - Unbolt nut from gantry/plate (typically 2x M5 bolts)
   - Unthread lead screw from nut (rotate lead screw)
   - Clean lead screw threads thoroughly

3. **Install new nut**:
   - Thread lead screw into new nut
   - May need to press arm down slightly to align threads
   - Bolt nut to gantry/plate (don't overtighten)
   - For black Delrin: tension per Anti-backlash section
   - For spring-loaded: jog back and forth to break in

4. **Test axis**:
   - Check for wiggle (should be none)
   - Verify smooth movement
   - Adjust tension if needed

**Video Reference**: Sienci Labs anti-backlash nut replacement guide

---

#### Router Brushes

**Lifespan**: Varies by router model and use

**Replace When**:
- Router loses power or stops
- Excessive sparking at brush ports
- Router runs erratically
- Brushes worn to wear line indicator

**Replacement Procedure**:

1. **Identify router model** and order correct brushes
2. **Power off completely** and disconnect
3. **Remove from mount** if necessary for access
4. **Locate brush caps** (typically on sides of router)
5. **Unscrew brush caps** and remove old brushes
6. **Check brush length** against wear indicators
7. **Install new brushes**:
   - Ensure proper orientation (spring end first)
   - Screw caps in firmly
8. **Run router** at low speed to seat brushes (5-10 min)

**Tip**: Replace brushes in pairs for even wear

---

### Preventive Replacement Schedule

Consider replacing these items proactively:

| Component | Preventive Interval | Cost vs. Failure Cost |
|-----------|--------------------|-----------------------|
| V-wheels | 1,500 hours | Low cost, prevents accuracy issues |
| Anti-backlash nuts | 1,500 hours | Low cost, prevents lead screw damage |
| Router brushes | Per manufacturer | Low cost, prevents router damage |
| Belts (if equipped) | 2,000 hours | Medium cost, prevents sudden failure |
| Lead screws | Inspect yearly | High cost, look for wear |

---

## Maintenance Logs & Checklists

### Why Keep Maintenance Logs?

- **Track patterns**: Identify components that wear faster
- **Plan ahead**: Order parts before they fail
- **Warranty**: Documentation for warranty claims
- **Resale value**: Shows well-maintained machine
- **Troubleshooting**: Historical data helps diagnose issues

### How to Use These Logs

1. **Print or copy** to notebook kept near machine
2. **Fill out immediately** after maintenance
3. **Review monthly** for patterns
4. **Note unusual findings** in comments section
5. **Keep digital backup** (photo or scan)

---

### Pre-Operation Checklist

**Date**: _____________ **Operator**: _____________

| Item | Check | Notes |
|------|-------|-------|
| Visual inspection for loose/damaged parts | ☐ | |
| Router/spindle securely mounted | ☐ | |
| Workpiece securely clamped | ☐ | |
| Tool properly installed in collet | ☐ | |
| Power connections secure | ☐ | |
| E-stop functional | ☐ | |
| Work area clear of debris | ☐ | |
| Dust collection connected | ☐ | |
| Safety equipment on hand (glasses, mask, ear protection) | ☐ | |
| G-code file verified/simulated | ☐ | |
| Machine homed (if required) | ☐ | |
| Zero positions set correctly | ☐ | |

**Ready to cut?** ☐ YES  ☐ NO (resolve issues first)

---

### Maintenance Activity Log

| Date | Hours | Activity | Components | Time Spent | Findings/Notes | Next Action |
|------|-------|----------|------------|-----------|----------------|-------------|
| | | Rails & wheels cleaned | All axes | | | |
| | | Eccentric nuts adjusted | X-axis | | | |
| | | Anti-backlash tensioned | Y1, Y2 | | | |
| | | Linear guides lubricated | Z-axis | | | |
| | | Hardware check | All | | | |
| | | V-wheels replaced | X-axis | | | |
| | | Deep clean | Full machine | | | |

---

### Cumulative Hours Tracker

**Machine Model**: _________________ **Serial #**: _________________

| Date | Session Hours | Cumulative Hours | Material Cut | Notes |
|------|--------------|------------------|--------------|-------|
| | | | | |
| | | | | |
| | | | | |

**Current Total Hours**: _________

**Last Maintenance at**: _________ hours  
**Next Maintenance Due**: _________ hours

---

### Component Replacement Log

| Date | Hours | Component | Part Number | Reason | Cost | Supplier |
|------|-------|-----------|-------------|--------|------|----------|
| | | | | | | |
| | | | | | | |

---

### Issue/Troubleshooting Log

| Date | Hours | Issue Description | Diagnosis | Solution | Time to Resolve | Preventive Action |
|------|-------|-------------------|-----------|----------|-----------------|-------------------|
| | | | | | | |

---

## Alarm & Error Code Reference

### grbl Alarm Codes (Common on Hobby CNCs)

| Code | Name | Description | Solution |
|------|------|-------------|----------|
| **1** | Hard Limit | Hard limit triggered, position likely lost | Re-home machine, check limit switches |
| **2** | Soft Limit | Motion exceeds machine travel | Unlock with `$X`, verify g-code within limits |
| **3** | Abort During Cycle | Unexpected stop during job | Re-home recommended, check for interference |
| **4** | Probe Fail | Probe already triggered before cycle | Move bit away from touch plate |
| **5** | Probe Fail | Probe didn't contact within travel | Move bit closer to touch plate (6-12mm) |
| **6** | Homing Fail | Homing cycle reset | Check limit switch wiring |
| **7** | Homing Fail | Safety door opened during homing | Close door, restart homing |
| **8** | Homing Fail | Pull-off failed to clear limit | Increase pull-off distance ($27) |
| **9** | Homing Fail | Limit switch not found | Increase max travel or check wiring |

**How to Clear Alarms**:
- Type `$X` in Console and press Enter/Run
- Click "Unlock" button in gSender or UGS
- Some alarms require power cycle

---

### grbl Error Codes

| Code | Description | Solution |
|------|-------------|----------|
| **1** | Expected Command Letter | Check g-code syntax |
| **2** | Bad Number Format | Verify numbers in g-code |
| **8** | grbl Locked | Reset then unlock with `$X` |
| **9** | Unlock Failed | Alarm condition still active |
| **10** | Soft Limit Error | Can't enable without homing enabled |
| **20** | Unsupported Command | Check firmware version compatibility |
| **24** | Check Door | Safety door open or laser mode mismatch |

---

### grblHAL-Specific Alarms (SuperLongBoard, etc.)

| Code | Name | Description | Solution |
|------|------|-------------|----------|
| **10** | E-stop | Emergency stop activated | Release E-stop, unlock, reset |
| **14** | Spindle Setup | Spindle communication error | Check VFD wiring and settings |

**Special Notes**:
- Alarm 10 on startup: Click "Unlock Machine" in gSender
- Multiple alarms may stack but clear together
- After E-stop: Always reset then unlock

---

### Useful Console Commands

| Command | Function |
|---------|----------|
| `$` | Show all available commands |
| `$$` | List all firmware settings |
| `$X` | Unlock machine (clear alarm) |
| `$H` | Run homing cycle |
| `$rst=$` | Reset all settings to defaults |
| `?` | Report status and active inputs |
| `$i` | Show firmware version |
| `$#` | Show stored work offsets |

---

## Advanced Tuning & Optimization

### Fine-Tuning Machine Performance

#### Optimizing Firmware Settings

**Key Settings to Understand** (grbl):

| Setting | Parameter | Typical Value | Purpose |
|---------|-----------|---------------|---------|
| $100-102 | Steps per mm | Varies | Match to mechanical setup |
| $110-112 | Max rate (mm/min) | 5000-8000 | Maximum axis speed |
| $120-122 | Acceleration (mm/sec²) | 500-800 | How quickly speed changes |
| $130-132 | Max travel (mm) | Machine size | Soft limit boundaries |
| $10 | Status report mask | 511 | Enable all status reporting |
| $22 | Homing enabled | 1 | Enable homing cycle |
| $27 | Homing pull-off (mm) | 3-5 | Distance to back off switch |

**Adjusting for Performance**:

1. **Increase max rates** ($110-112):
   - Start conservative (5000 mm/min)
   - Incrementally increase (500 mm/min steps)
   - Test at each level for stalling
   - Back off 10% from stall point for safety margin

2. **Tune accelerations** ($120-122):
   - Higher = faster direction changes
   - Too high = stalling or overshooting
   - Balance between speed and accuracy

3. **Test methodology**:
   - Create test pattern with rapid movements
   - Run at various speeds
   - Measure accuracy with calipers
   - Find sweet spot for your use case

#### Mechanical Tuning

**Squaring the Machine**:

1. Measure diagonals of work area (should be equal)
2. Adjust Y-axis rail alignment if needed
3. Use precision square to verify axes perpendicular
4. Tram router/spindle to table

**Reducing Backlash Further**:

1. Use spring-loaded anti-backlash nuts (upgrade)
2. Ensure lead screws are straight
3. Verify coupler alignment
4. Consider upgrading to ball screws (advanced)

**Improving Rigidity**:

1. Add weight to table (damping)
2. Secure machine firmly to table
3. Ensure table is level and stable
4. Consider bracing for larger machines

---

### When to Seek Professional Help

Contact manufacturer or professional service if:

- Controller consistently malfunctions after troubleshooting
- Structural damage (cracked plates, bent rails)
- Electrical issues beyond basic checks
- Stepper motors physically damaged
- Lead screws bent or threads damaged
- Repeated issues after multiple repair attempts

---

## Resources & Further Reading

### Official Documentation

- **Sienci Labs Resources**: resources.sienci.com
- **grbl GitHub**: github.com/gnea/grbl/wiki
- **grblHAL GitHub**: github.com/grblHAL/core

### Community Forums

- **Sienci Labs Facebook Group**: facebook.com/groups/mill.one
- **grbl Community**: Various online forums
- **Reddit**: r/hobbycnc, r/CNC

### Video Resources

- **Sienci Labs YouTube**: Complete assembly and maintenance videos
- **Bucky's Customs**: Excellent troubleshooting and maintenance guides
- **Winston Moy**: CNC fundamentals and techniques

### Technical References

- **Backlash Explanation**: machinetoolhelp.com/Repairing/What_is_backlash.html
- **Linear Bearing Lubrication**: thomsonlinear.com/support/tips
- **Hiwin Lubrication Guide**: hiwin.com/pdf/lubricating_instructions.pdf

### Recommended Tools & Supplies

- **Quality Allen Key Sets**: Wera, Wiha, Bondhus
- **Machine Oil**: 3-in-1, Mobil DTE, Way Oil
- **Calipers**: Digital calipers for precision measurement
- **Multimeter**: For electrical diagnostics

---

## Appendix: Quick Reference Tables

### Maintenance Quick Reference

| Every Use | Every 10-20 Hrs | Every 20-30 Hrs | Every 50 Hrs | Every 1,500-2,000 Hrs |
|-----------|-----------------|-----------------|--------------|----------------------|
| Visual check | Clean rails & wheels | Lubricate Z-axis | Deep clean | Replace V-wheels |
| Safety check | Check eccentric nuts | Check hardware | Full inspection | Replace anti-backlash nuts |
| Clear debris | Tension backlash nuts | | Test accuracy | |

### Troubleshooting Quick Guide

| Symptom | Most Likely Cause | First Check |
|---------|-------------------|-------------|
| Motor not moving | Connection issue | Reseat motor plugs |
| Motor stalling | Over-tightened wheels | Adjust eccentric nuts |
| Lost position | Loose couplers | Check set screws |
| Rough cuts | Dull bit | Replace cutting tool |
| Controller dead | Power issue | Check power supply LED |
| Backlash in axis | Worn anti-backlash nut | Test and tension/replace |

### Torque Specifications

| Fastener | Application | Torque |
|----------|-------------|--------|
| M3 screws | Linear rails, Z-plate | Snug (don't strip) |
| M5 bolts | Structural | Firm, secure |
| Set screws | Couplers | Snug on flat |
| V-wheel bolts | After eccentric adjustment | Firm |

---

## Revision History

| Version | Date | Changes | Author |
|---------|------|---------|--------|
| 1.0 | Nov 15, 2025 | Initial creation from Sienci Labs resources | HANZORAZER |

---

## About This Workbook

This workbook was compiled from the extensive documentation provided by Sienci Labs for their CNC products, including the LongMill MK2, Mill One, Vortex, and SuperLongBoard. While examples reference specific products, the maintenance principles apply broadly to hobby CNC routers with similar mechanical designs.

**Source Repository**: https://github.com/HanzoRazer/Resources (Forked from Sienci Labs)

**Original License**: CC BY-SA 4.0 (Creative Commons Attribution-ShareAlike 4.0)

**Acknowledgments**:
- Sienci Labs for comprehensive documentation
- Community contributors on Facebook groups and forums
- Video creators: Bucky's Customs, Winston Moy, and others

---

## Your Notes & Customizations

Use this space to document machine-specific information:

**My Machine Details**:
- Model: ______________________
- Serial Number: ______________________
- Purchase Date: ______________________
- Modifications: ______________________

**My Specific Settings**:
- $100 (X steps/mm): ______
- $101 (Y steps/mm): ______
- $102 (Z steps/mm): ______
- $110 (X max rate): ______
- $111 (Y max rate): ______
- $112 (Z max rate): ______

**Supplier Contacts**:
- Parts Supplier: ______________________
- Technical Support: ______________________
- Local CNC Shop: ______________________

**Machine-Specific Quirks**:
_____________________________________
_____________________________________
_____________________________________

---

**END OF WORKBOOK**

Remember: **Consistent maintenance is the key to a long-lasting, accurate CNC machine!**
