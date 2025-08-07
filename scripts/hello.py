def main():
    import pandas as pd
    import numpy as np
    df = pd.DataFrame({'a': np.arange(5), 'b': np.arange(5, 10)})
    return {"sum_a": int(df['a'].sum()), "max_b": int(df['b'].max())}