import pandas as pd

# Dummy data for 1 lakh entries
data = {
    "Name": [f"User{i}" for i in range(1, 100001)],
    "Email": [f"user{i}@test.com" for i in range(1, 100001)],
    "Address": [f"Test Address {i}" for i in range(1, 100001)],
    "Phone number": [f"98765{i:05d}" for i in range(1, 100001)],
    "Comments": [f"Test comment {i}" for i in range(1, 100001)]
}

df = pd.DataFrame(data)

# Save to Excel file
df.to_excel("form_data.xlsx", index=False)

print("✅ Dummy data written to form_data.xlsx")
