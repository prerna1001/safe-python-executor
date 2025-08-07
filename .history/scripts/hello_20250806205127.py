def main():
    import pandas as pd
    print("This print should not be in 'result'.")
    df = pd.DataFrame({'a': [1,2], 'b': [3,4]})
    return {"message": "Success!", "sum": int( df['a'].sum())}
