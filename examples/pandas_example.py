import numpy as np
import pandas as pd

# Create a sample DataFrame
df = pd.DataFrame(
    {"A": np.random.randn(5), "B": np.random.randn(5), "C": np.random.randn(5)}
)

# Using deprecated DataFrame.append method
new_row = pd.DataFrame({"A": [0.1], "B": [0.2], "C": [0.3]})
df = df.append(new_row, ignore_index=True)

# Using deprecated DataFrame.ix indexer
value = df.ix[0, "A"]

# Using deprecated inplace parameter
df.drop("B", axis=1, inplace=True)

# Using deprecated DataFrame.as_matrix method
matrix = df.as_matrix()

# Using deprecated pd.datetime.now method
current_time = pd.datetime.now()

# Using current methods
df["D"] = np.random.randn(6)
df.loc[6] = [0.1, 0.2, 0.3]
df = pd.concat([df, new_row], ignore_index=True)
matrix = df.values

print(df)
