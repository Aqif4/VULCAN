input_file = "P_TOI270d_Psurf_1bar_Tsurf_320K_Tstrat_250K.txt"
output_file = "P-20_TOI270d_Psurf_1bar_Tsurf_320K_Tstrat_250K.txt"
shift=-20

with open(input_file, 'r') as f:
	lines = f.readlines()

with open(output_file, 'w') as f:
	for line in lines:
		# Preserve comment/header lines
		if line.strip().startswith("#") or "Pressure" in line or "Temp" in line:
			f.write(line)
		elif line.strip():  # skip empty lines
			parts = line.strip().split()
			if len(parts) == 3:
				pressure = parts[0]
				temp = float(parts[1]) + shift  # subtract 5
				kzz = parts[2]
				f.write(f"{pressure:<12} {temp:5.1f}  {kzz}\n")