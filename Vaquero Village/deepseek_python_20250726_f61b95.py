def stagnation_risk(Q_gpm, D_pipe):
    """Check flow velocity against AWWA guidelines"""
    Q = Q_gpm * (1/7.48052) / 60  # ft³/s
    v = Q / (np.pi * (D_pipe/2)**2)
    return "High Risk" if v < 0.1 else "Low Risk"

# Example usage
print(stagnation_risk(0.5, dia_CN))  # Output: "High Risk"