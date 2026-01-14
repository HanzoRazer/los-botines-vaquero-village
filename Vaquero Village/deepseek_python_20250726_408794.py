def dual_pump_control(Q_demand, P_CN92):
    """Determine pump activation status"""
    if Q_demand > 15 or P_CN92 < 45:
        return "Dual Pumps ON"
    else:
        return "Single Pump ON"

# Example usage
print(dual_pump_control(20, 44))  # Output: "Dual Pumps ON"