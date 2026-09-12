def solve_transportation_master():
    costs = [
        [3, 1, 7, 4],
        [2, 6, 5, 9],
        [8, 3, 3, 2]
    ]
    supply = [300, 400, 500]
    demand = [250, 350, 400, 200]
    
    rows, cols = len(supply), len(demand)
    allocation = [[0]*cols for _ in range(rows)]
    
    total_supply = sum(supply)
    total_demand = sum(demand)
    
    print("===========================================================================")
    print(" TRANSPORTATION PROBLEM: VAM & MODI STEP-BY-STEP")
    print("===========================================================================")
    print("1. PROBLEM DEFINITION & MATRIX:")
    print("       |  D1  |  D2  |  D3  |  D4  || SUPPLY")
    print("---------------------------------------------")
    for i in range(rows):
        row_str = f"    S{i+1} | "
        for j in range(cols):
            row_str += f"{costs[i][j]:^4} | "
        row_str += f"| {supply[i]}"
        print(row_str)
    print("---------------------------------------------")
    
    dem_str = "DEMAND | "
    for d in demand:
        dem_str += f"{d:^4} | "
    print(dem_str)
    
    print(f"\n[Balance Check] Total Supply ({total_supply}) == Total Demand ({total_demand}). The problem is Balanced.")
    
    print("\n===========================================================================")
    print(" PHASE 1: VAM (Vogel's Approximation Method) - Finding Initial Solution")
    print("===========================================================================")
    print("Rule: Penalty = (Second Lowest Cost - Lowest Cost) in each row/column.")
    print("Allocate to the cheapest cell in the row or column with the HIGHEST penalty.")
    
    supply_left = supply.copy()
    demand_left = demand.copy()
    
    step = 1
    while sum(supply_left) > 0 and sum(demand_left) > 0:
        row_penalties = []
        col_penalties = []
        
        for i in range(rows):
            if supply_left[i] > 0:
                valid_costs = [costs[i][j] for j in range(cols) if demand_left[j] > 0]
                valid_costs.sort()
                row_penalties.append(valid_costs[1] - valid_costs[0] if len(valid_costs) > 1 else valid_costs[0])
            else:
                row_penalties.append(-1)
                
        for j in range(cols):
            if demand_left[j] > 0:
                valid_costs = [costs[i][j] for i in range(rows) if supply_left[i] > 0]
                valid_costs.sort()
                col_penalties.append(valid_costs[1] - valid_costs[0] if len(valid_costs) > 1 else valid_costs[0])
            else:
                col_penalties.append(-1)

        max_r_pen = max(row_penalties)
        max_c_pen = max(col_penalties)
        
        if max_r_pen >= max_c_pen:
            r = row_penalties.index(max_r_pen)
            c = min([(costs[r][j], j) for j in range(cols) if demand_left[j] > 0], key=lambda x: x[0])[1]
        else:
            c = col_penalties.index(max_c_pen)
            r = min([(costs[i][c], i) for i in range(rows) if supply_left[i] > 0], key=lambda x: x[0])[1]
                    
        qty = min(supply_left[r], demand_left[c])
        allocation[r][c] = qty
        
        print(f" -> Step {step}: Max penalty is {'Row' if max_r_pen >= max_c_pen else 'Col'}. "
              f"Allocating {qty:3} units to Cell(S{r+1}, D{c+1}) at cost ${costs[r][c]}.")
        
        supply_left[r] -= qty
        demand_left[c] -= qty
        step += 1

    print("\nInitial Allocation Matrix (VAM):")
    for i in range(rows):
        print("   " + "\t".join([f"{val:4}" for val in allocation[i]]))
        
    vam_total_cost = sum(allocation[i][j] * costs[i][j] for i in range(rows) for j in range(cols))
    print("---------------------------------------------------------------------------")
    print(f" => TOTAL COST BY VAM (Initial Basic Feasible Solution) = ${vam_total_cost}")
    print("---------------------------------------------------------------------------")


    print("\n===========================================================================")
    print(" PHASE 2: MODI METHOD - Testing & Optimizing the Solution")
    print("===========================================================================")
    print("Step A: Calculate Dual Variables (u_i, v_j) for ALLOCATED cells.")
    print("Formula: c_ij = u_i + v_j  (We arbitrarily set u_1 = 0 to start)")
    
    u = [None] * rows
    v = [None] * cols
    u[0] = 0 
    
    for _ in range(rows + cols): 
        for i in range(rows):
            for j in range(cols):
                if allocation[i][j] > 0: 
                    if u[i] is not None and v[j] is None:
                        v[j] = costs[i][j] - u[i]
                    elif v[j] is not None and u[i] is None:
                        u[i] = costs[i][j] - v[j]
                        
    print(f" -> Solved Row Variables (u): {u}")
    print(f" -> Solved Col Variables (v): {v}")

    print("\nStep B: Calculate Opportunity Costs (Delta) for EMPTY cells.")
    print("Formula: Delta_ij = c_ij - (u_i + v_j)")
    print("Condition: If ALL Deltas are >= 0, the current solution is perfectly optimal.")
    
    is_optimal = True
    for i in range(rows):
        for j in range(cols):
            if allocation[i][j] == 0:
                delta = costs[i][j] - (u[i] + v[j])
                print(f" -> Empty Cell (S{i+1}, D{j+1}): Cost({costs[i][j]}) - [u({u[i]}) + v({v[j]})] = {delta}")
                if delta < 0:
                    is_optimal = False

    print("\n---------------------------------------------------------------------------")
    if is_optimal:
        print(" => Optimality Check: PASSED. All empty cell Deltas >= 0.")
        print(f" => TOTAL COST BY MODI (Final Optimal Solution) = ${vam_total_cost}")
    else:
        print(" => Optimality Check: FAILED. Negative Deltas exist.")
        print(" => To find the final MODI cost, you must draw a closed loop starting from")
        print("    the cell with the most negative Delta, shift units, and recalculate.")
    print("---------------------------------------------------------------------------")

    
    print("\n===========================================================================")
    print(" FINAL SHIPMENT PLAN (ALLOCATIONS)")
    print("===========================================================================")
    for i in range(rows):
        for j in range(cols):
            if allocation[i][j] > 0:
                print(f"   [+] Route S{i+1} -> D{j+1} : Ship {allocation[i][j]:3} units (@ ${costs[i][j]}/unit)")

solve_transportation_master()