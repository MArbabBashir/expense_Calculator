from operator import index

try:
    import os
    import pandas as pd
except ImportError:
    print("Please install the pandas package.")
print("Test Yourself for CSV Manipulation")

path = "./Data/data.csv"
cols = ["ID","Name","Category","Amount"]

if not os.path.exists(path) or os.path.getsize(path) == 0:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    print("Created new directory in " + path)
    df = pd.DataFrame( columns = cols)
    df.to_csv(path, index=False)

while(True):
    print("============= Expense Calculator ===========")
    choice = input(" 1. View CSV (r) \n 1. Write into CSV (w) \n  3. update expenditure (u) \n Please enter your choice:  ").lower()
    match choice:
        case 'r':
            df = pd.read_csv(path, index_col = 0)
            print("Reading csv..... ")
            print("============= Showing CSV ===========")
            print(df)
        case 'w':
            rd = pd.read_csv(path)
            highest_id = rd["ID"].max() if not rd.empty else 0
            print(f"mask is {highest_id}")

            df = pd.DataFrame([[highest_id+1, "shirt", "shopping", 1000]], columns=cols)
            df.to_csv(path, index=False, mode='a', header=False)

        case 'u':
            tk_name = input("Please enter expense name to edit: ")
            tk_amount = int(input("Please enter updated amount: "))

            rd = pd.read_csv(path, index_col = 0)
            mask = rd["Name"] == tk_name

            rd.loc[mask, "Amount"] = tk_amount
            rd.to_csv(path)



# to_csv    ==>  w
# to_csv (mode=a) ==   a