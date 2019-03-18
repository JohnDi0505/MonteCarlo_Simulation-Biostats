import os
import time
import numpy as np
import pandas as pd
import re
import statsmodels as sm
print("\nmodule statsmodels version =%s\n" % str(sm.version.version))
import statsmodels.formula.api as smf
from pandas import DataFrame

# detect output folder "lmer_predict_outputs"
dir_name = "lmer_predict_outputs"
if not os.path.exists(dir_name):
    try:
        os.mkdir(dir_name)
    except:
        print("Can't create output folder!")        

# load input data
flu_df = pd.read_csv("flu.tsv", sep="\t")
flu_df = flu_df.dropna(axis=0).reset_index(drop=True)
positions = np.array([pos for pos in flu_df.columns if re.search(r'pos', pos)])

# define dependent/independent variables and random effects
res_var = 'titre'
rnd_var = 'refv'
ind_var = list(set(flu_df.columns).difference(['titre', 'refv', 'testv', 'treedist', 'test.year', 'ref.year']))

expression = res_var + '~'
predictors = ind_var[0]
for ix in range(1, len(ind_var)):
    predictors += '+' + ind_var[ix]
expression += predictors

# calibrate linear mixed model
md = smf.mixedlm(expression, flu_df, groups=flu_df[rnd_var], missing='drop')
mdf = md.fit()
# write model parameters to file
try:
    model_params = open(dir_name + '/model_params.txt', 'w')
    model_params.write(mdf.summary().as_text())
    model_params.close()
except:
    print("Fail to write model parameters!")

# function to randomly introduce mutations(0 ~ 20) to specific substitution sites; each has 20 runs
iterations = 20
def mutation_simulator(refv_id, testv_id, sites, epochs):
    refv = flu_df[flu_df.refv == refv_id]
    
    # create empty output dataframe
    out_df = DataFrame(columns=["mut|"+str(j) for j in range(len(positions)+1)], index=np.arange(20))
    
    # iterate over number of mutations
    for num_mut in range(len(positions)+1): # number of mutations range from 0 to 20
        for i in range(epochs):
            print("Introduce mutations = %d;\tepoch = %d " % (num_mut, i))
            testv = refv[refv.testv == testv_id]
            mut_sites = np.random.choice(positions, num_mut, False)
            if len(mut_sites) != 0:
                testv.loc[:, mut_sites] = abs(testv.loc[:, mut_sites] - 1)
            out_df.loc[i, "mut|"+str(num_mut)] = mdf.predict(testv).values[0]
    return(out_df)

# extract subset where titre >= 5.0
df_batch = flu_df[flu_df.titre >= 5].reset_index(drop=True)

print("start batch processing...")
start_time = time.time()
# batch iterating all pairs of testv & refv in "df_batch"
for i in df_batch.index:
    tstv_id = df_batch.loc[i, 'testv']
    refv_id = df_batch.loc[i, 'refv']
    print("\nprocessing testv=%s, refv=%s:\n" % (tstv_id, refv_id))
    out_matrix = mutation_simulator(refv_id, tstv_id, positions, iterations)
    tstv_out = tstv_id.replace("vid|", "testv")
    refv_out = refv_id.replace("vid|", "refv")
    out_matrix.to_csv(dir_name + "/mat_%s_%s.csv" % (refv_out, tstv_out), index=None)

stop_time = time.time()
print("\nBatch processing complete. Total duration = %f s." % (stop_time - start_time))
