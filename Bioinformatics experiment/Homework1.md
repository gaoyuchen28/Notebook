<style>
  pre code {
    white-space: pre-wrap; /* 强制在代码块内换行 */
    word-break: break-all;
    max-width: 600px;      /* 也可以直接规定像素宽度 */
  }
</style>

1. Preview the iris table and output the first 5 rows (1 points)<br>
    **code:**<br>
    ```R
    View(iris)
    iris[1:5,]
    ```

    **Screenshot:**

    ![1](1.png)

    **Conclusion:**<br>

Successfully output the first 5 rows

|ID|Sepal.L|Sepal.W|Petal.L|Petal.W|Species|
|:---|:---|:---|:---|:---|:---|
|1|5.1|3.5|1.4|0.2|setosa|
|2|4.9|3.0|1.4|0.2|setosa|
|3|4.7|3.2|1.3|0.2|setosa|
|4|4.6|3.1|1.5|0.2|setosa|
|5|5.0|3.6|1.4|0.2|setosa|



2. Print the numbers of rows and columns of the table<br>
   **code:**<br>
   ```R
   cat("Number of rows:", nrow(iris))
   cat("Number of columns:", ncol(iris))
   ```

   **Screenshot:**

   ![2](2.png)

   **Conclusion:**<br>
   Successfully count the number of rows and columns of the table, there's 150 rows and 5 columns.

3. Describe the number of samples for different plant species (1 points)<br>
   **code:**<br>
   ```R
   iris%>%group_by(Species)%>%summarise(count=n())
   ```

   **Screenshot:**

   ![3](3.png)

   **Conclusion:**<br>
   Successfully count the number of samples for different plant species, each species has 50 samples.

4. Median value of Sepal.Length in the table (1 points)<br>
   **code:**<br>
   ```R
   iris%>%summarise(Median_value=median(Sepal.Length))
   ```

   **Screenshot:**

   ![4](4.png)

   **Conclusion:**<br>
   The Median value of Sepal.Length is 5.8. 

5. Summarize the means of Sepal.Length, Sepal.Width, Petal.Length, Petal.Width for each species (1 point)<br>
   **code:**<br>
   ```R
   iris%>%group_by(Species)%>%summarise(mean(Sepal.Length),mean(Sepal.Width),mean(Petal.Length),mean(Petal.Width))
   ```

   **Screenshot:**

   ![5](5.png)

   **Conclusion:**<br>
Successfully obtain the means of Sepal.Length, Sepal.Width, Petal.Length, Petal.Width for each species.<br>

|Species|m.Sepal.L|m.Sepal.W|m.Petal.L|m.Petal.W|
|:---|:---|:---|:---|:---|
|setosa|5.01|3.43|1.46|0.246|
|versicolor|5.94|2.77|4.26|1.33|
|virginica|6.59|2.97|5.55|2.03|

---

Add a column to the table annotating the main origin of each species (Tip: use full_join)<br>
   code:<br>
   ```R
   Origin <- data.frame(
    Species = c("setosa", "versicolor", "virginica"),
    Annotation = factor(c("Asia and North America","North America","the United States"))
    )
    iris%>%full_join(Origin)
   ```

   Screenshot:<br>

   ![6](6.png)


----

1. Draw a boxplot to compare the Sepal.Width of different species (2 point)<br>
   **code:**<br>
   ```R
   p <- ggplot(data=iris,
            mapping=aes(
              x=Species,
              y=Sepal.Width)
    )+geom_boxplot()+theme_economist()
    ```

   **Screenshot:**

   ![7](7.png)

   ![8](8.png)

2. Draw a histogram to compare the Sepal.Width of different species (2 point)<br>
   **code:**<br>
   ```R
   ggplot(data = iris, aes(x = Sepal.Width, fill = Species)) +geom_histogram()+theme_classic()
    ```

   **Screenshot:**

   ![9](9.png)

   ![10](10.png)

3. Raise a scientific question about iris dataset (1 point) 

To what extent can we mathematically define a "species boundary" using only floral measurements