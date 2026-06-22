with open("stock_platform/core/technical.py", "r") as f:
    content = f.read()

content = content.replace("df.fillna(method='bfill', inplace=True)", "df.bfill(inplace=True)")

with open("stock_platform/core/technical.py", "w") as f:
    f.write(content)
