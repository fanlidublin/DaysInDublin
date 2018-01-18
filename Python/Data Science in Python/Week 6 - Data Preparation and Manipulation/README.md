# Lecture Notes  

```
> pd.Series([45, 232, 45, 67])  
> pop = pd.Series([1357000000, 1252000000, 321068000, 249900000], ["China", "India", "USA", "Indonesia"])  
> pd.Series(["China", "India", "USA", "Indonesia"], [1357000000, 1252000000, 321068000, 249900000])  
## first values and then the key  
> p = pop.describe()  
> print (p["mean"])  
> Series slicing is possible  
> pop > 100000000  
## returns true false  
> pop[pop > 100000000]  
## returns the values with population greater than 100000000  
> pop.index  
```

### DATAFRAMES   

```
> countries = pd.DataFrame({"Country":["China", "India", "USA", "Indonesia"], "Population":[1357000000, 1252000000, 321068000, 249900000], "GDP":[11384760, 2182580, 17968200, 888648], "Life Expectancy":[75.41, 68.13, 79.68, 72.45]}) # can it accept JSON  
> countries.shape # difference between shape and mean() type method  
> df = pd.read_csv("countries.csv")  
> df = pd.read_csv("countries.csv", index_col = "Country ID")  
> df.describe()  
> df.mean()  
> df["School Years"]  
> df["CPI", "School Years"]  
> df.iloc[0] # for numeric positions   
> df.loc["Sweden"] # for index name  
```  

### Go through slide 19  
