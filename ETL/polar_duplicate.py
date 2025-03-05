import polars as pl


data = {'id':[1,2,2,4,5,5,6,6,6,7,7,7,9,10,10,11],'score':[10,20,20,40,50,50,60,90,90,100,100,115,120,120,130,150]}
df = pl.DataFrame(data)
print(df)



detec_dup = df.filter(pl.col('id').is_duplicated())
print(detec_dup) #duplicate gulo ke print korbe



# remove_duplicates_keep_first = df.drop_duplicates()
# print(remove_duplicates_keep_first.T) #duplicate rows and cols ke shoray print korbe

# remove_duplicates_keep_last = df.drop_duplicates(keep='last')
# print(remove_duplicates_keep_last.T) #duplicate rows and cols ke shoray print korbe


#transposed dataframe
# df_transposed = df[df.duplicated()].T

# print(df_transposed)