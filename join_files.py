"""
Some WASP datasets have two observation files:
Simple function to join both files and output a combined file
"""
import os
import pandas as pd

def load_file(filename):
    data_path = os.path.join(os.getcwd(), 'data')
    hats_path = os.path.join(data_path, 'hats', (filename+".tfalc"))

    df = pd.read_csv(hats_path,
                     delim_whitespace=True,
                     skiprows=1,
                     header=None)
    return df

if __name__ == "__main__":
    WASP_6_a = load_file('WASP-6_3')
    WASP_6_b = load_file('WASP-6_4')

    WASP_6 = WASP_6_a.append(WASP_6_b)

    print(WASP_6)

    out_path = os.path.join(os.getcwd(), 'data', 'hats', "WASP-6.tfalc")

    WASP_6.to_csv(path_or_buf=out_path,
                  sep="\t",
                  header="#HATpipe SVN version: 2625",
                  index=False)
