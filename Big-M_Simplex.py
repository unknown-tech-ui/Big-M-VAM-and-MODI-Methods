def print_tableau(tableau, title):
    print(f"\n{'-'*75}")
    print(f" {title}")
    print(f"{'-'*75}")
    print("Row |\t    x1\t    x2\t    s1\t    s2\t    A1\t    A2\t   RHS")
    print("-" * 75)
    for i, row in enumerate(tableau):
        row_name = "Z   " if i == 3 else f"R{i+1}  "
        print(f"{row_name}|\t" + "\t".join([f"{val:6.1f}" for val in row]))
    print("-" * 75)

def solve_big_m():
    M = 10000.0
    
    print("===========================================================================")
    print(" BIG-M SIMPLEX PROBLEM FORMULATION")
    print("===========================================================================")
    print("1. ORIGINAL LINEAR PROGRAMMING PROBLEM:")
    print("   Minimize Z = 4x1 + x2")
    print("   Subject to:")
    print("      3x1 +  x2  = 3")
    print("      4x1 + 3x2 >= 6")
    print("       x1 + 2x2 <= 4")
    print("       x1,   x2 >= 0")
    
    print("\n2. CONVERSION TO STANDARD FORM:")
    print("   - Constraint 1 (=) : Add Artificial variable A1")
    print("   - Constraint 2 (>=): Subtract Surplus variable s1, Add Artificial A2")
    print("   - Constraint 3 (<=): Add Slack variable s2")
    
    print("\n   New Equations:")
    print("      3x1 +  x2 +  0s1 + 0s2 + 1A1 + 0A2 = 3")
    print("      4x1 + 3x2 -  1s1 + 0s2 + 0A1 + 1A2 = 6")
    print("       x1 + 2x2 +  0s1 + 1s2 + 0A1 + 0A2 = 4")
    
    print("\n3. MODIFIED OBJECTIVE FUNCTION (Maximization Form):")
    print("   Since standard Simplex maximizes, we Maximize -Z.")
    print("   We assign a huge penalty (-M) to artificial variables.")
    print("   Maximize -Z = -4x1 - x2 + 0s1 + 0s2 - MA1 - MA2")
    print("   Z-Row Equation: -Z + 4x1 + x2 + 0s1 + 0s2 + MA1 + MA2 = 0")
    print("===========================================================================\n")

    tableau = [
        [3.0,  1.0,  0.0,  0.0,  1.0,  0.0,  3.0], 
        [4.0,  3.0, -1.0,  0.0,  0.0,  1.0,  6.0],
        [1.0,  2.0,  0.0,  1.0,  0.0,  0.0,  4.0],
        [-4.0,-1.0,  0.0,  0.0, -M,   -M,    0.0] 
    ]
    
    print_tableau(tableau, "STEP 1: Raw Initial Tableau (Directly from standard form)")
    
    print("\n[PREPARATION]: The basic variables for our initial solution are A1, A2, and s2.")
    print("A basic variable must have a '0' in the Z-row. Right now, A1 and A2 have '-10000.0'.")
    print("We clear them by substituting the rows: New Z-Row = Old Z-Row + M*(R1) + M*(R2).")
    
    for j in range(7):
        tableau[3][j] += M * tableau[0][j]
        tableau[3][j] += M * tableau[1][j]
        
    iteration = 0
    while True:
        print_tableau(tableau, f"ITERATION {iteration}")
        
        z_row = tableau[3][:-1]
        min_z = min(z_row)
        
        if min_z >= -0.001:
            print("\n*** ALL Z-ROW VALUES ARE >= 0. OPTIMAL SOLUTION REACHED! ***")
            break
            
        entering_col = z_row.index(min_z)
        print(f"\n-> Most negative Z-row value is {min_z:.2f} at Column {entering_col} (Variable enters basis).")
        
        best_ratio = 9999999
        leaving_row = -1
        
        for i in range(3): 
            if tableau[i][entering_col] > 0:
                ratio = tableau[i][6] / tableau[i][entering_col]
                print(f"   R{i+1} Ratio: {tableau[i][6]:.2f} / {tableau[i][entering_col]:.2f} = {ratio:.2f}")
                if ratio < best_ratio:
                    best_ratio = ratio
                    leaving_row = i
            else:
                print(f"   R{i+1} Ratio: N/A (Value in entering column <= 0)")
                    
        print(f"-> Minimum positive ratio is {best_ratio:.2f} in Row {leaving_row+1} (Variable leaves basis).")
        
        pivot_val = tableau[leaving_row][entering_col]
        print(f"-> Pivot Element is {pivot_val:.2f}. Executing row operations to make it 1, and rest of column 0.")
        
        for j in range(7):
            tableau[leaving_row][j] /= pivot_val
            
        for i in range(4): 
            if i != leaving_row:
                factor = tableau[i][entering_col]
                for j in range(7):
                    tableau[i][j] -= factor * tableau[leaving_row][j]
                    
        iteration += 1

    print("\n===========================================================================")
    print(" FINAL SUMMARY REPORT (ALLOTMENTS & COST)")
    print("===========================================================================")
    
    x1_val = tableau[1][6] 
    x2_val = tableau[0][6] 
    s1_val = 0.0           
    s2_val = tableau[2][6] 
    min_z  = -tableau[3][6]

    print("Decision Variables (Allotments):")
    print(f" -> x1 = {x1_val:.2f} units")
    print(f" -> x2 = {x2_val:.2f} units")
    print("\nSlack/Surplus Variables:")
    print(f" -> s1 = {s1_val:.2f} (Surplus for constraint 2 is zero)")
    print(f" -> s2 = {s2_val:.2f} (Slack for constraint 3, representing unused capacity)")
    
    print("\n---------------------------------------------------------------------------")
    print(f" FINAL MINIMUM OBJECTIVE COST (Z) = {min_z:.2f}")
    print("---------------------------------------------------------------------------")

solve_big_m()