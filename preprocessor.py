import pandas as pd     


def preprocess(df,region_df):
     
   
    df = df[df['Season']=='Summer']     #filtering for summer olympics
 
    df = df.merge(region_df, on='NOC', how='left')     #merging the two dataframes on NOC column    
 
    df.drop_duplicates(inplace=True)        #removing duplicates
 
    df = pd.concat([df, pd.get_dummies(df['Medal'])], axis=1)  #one hot encoding the medal column
 
    return df  #returning the preprocessed dataframe
