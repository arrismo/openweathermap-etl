# openweathermap-etl
This ETL (Extract, Transform, Load) pipeline is designed to retrieve weather data from OpenWeatherMap API, process it, and create a comprehensive weather data analysis solution.


# Prerequisites

1. Python 3.8+
2. Apache Airflow
3. OpenWeatherMap API Key
4. AWS S3 Bucket
5. MySQL Database
6. Power BI Desktop



# Architecture Diagram
1. `OpenWeather API`: Primary data source for weather information
1. `Airflow`: Scheduling and orchestration of data pipeline workflows
2. `Amazon S3`: Data lake for storing raw, unprocessed weather data
3. `MySQL`: Data warehouse for structured and transformed weather data
4. `Power BI`: Data visualization and dashboard creation

![Screenshot](diagram.png)

# Dashboard Insights
![Screenshot](weather-dashboard.png)

1. Date Slider: The date slider allows you to view weather data for different dates, which is a useful feature for tracking changes over time.
2. Avg Temp By Humidity: This chart shows the relationship between average temperature and humidity levels. The fluctuations in the line graph indicate how these two factors vary together.
3. Sunrise and Sunset Local Times: Displaying the local sunrise and sunset times is helpful for understanding the daylight hours.
4. Avg Wind Speed by Month: This bar chart compares the average wind speeds between November and December, providing insight into seasonal wind patterns.
5. Actual Temp (F) vs Feels Like (F): The scatter plot visualizes the relationship between the actual temperature and the "feels like" temperature, which takes into account factors like wind and humidity.


# Future Enhancements

1. Machine learning weather prediction models
2. Real-time alerting for extreme weather conditions
3. Expand geographical coverage
4. Implement more advanced data visualization techniques