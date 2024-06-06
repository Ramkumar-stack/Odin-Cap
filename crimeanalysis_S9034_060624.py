import pymysql as pymys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

cursor=""
connection=""
df=""

try:
        # 2. Database Connection :
        # - Use PyMySQL to establish a connection to the database in Pycharm or VS code.
        # - Verify the successful import of data in pycharm.

        # Connect to  db crimeproject, fetch all data from crime_data table and use panda libraries to create dataframe array
        connection=pymys.Connection(host='localhost',port=3306,user='root',password='y2024',database='crimeproject')
        cursor=connection.cursor()
        sql="Select * from crime_data"
        cursor.execute(sql)
        result=cursor.fetchall()
        # Get column names
        column_names = [desc[0] for desc in cursor.description]  # Extract column names from description
        if cursor:
            cursor.close()
        if connection:
            connection.close()
        df = pd.DataFrame(result, columns=column_names)
        print(df.head())
        
        # 3. Data Exploration:
        # - Retrieve basic statistics on the dataset, such as the total number of records and unique values in specific columns.
        # - Identify the distinct crime codes and their descriptions.


        # Get Basic info about the data in data frame

        print("Getting Basic Info:") # uncomment
        print(df.info()) #ucomment
        print()
        print("Getting Basic Statistics:")

        print(df.describe()) #uncomment
        print()

        # Get unique values in a specific column (e.g., 'crmcd')
        unique_crime_codes = df.drop_duplicates(subset='crmcd')
       
        print(f"Distinct crime codes with Descirption: \n {unique_crime_codes[['crmcd','Crm_Cd_Desc']]}") #uncooment
        print()
 
        # 4. Temporal Analysis:
        # -  Analyze the temporal aspects of the data.
        # - Determine trends in crime occurrence over time.
        # Temporal anaylsis 

        # cast text date fields to datetime format.
        df['Date_Rptd'] = pd.to_datetime(df['Date_Rptd'], format='%m/%d/%Y')
        df['DATE_OCC'] = pd.to_datetime(df['DATE_OCC'], format='%m/%d/%Y')  

        # (year,crimecount)      
        yearly_crime_count=df['Date_Rptd'].dt.year.value_counts()
       
        print("Analysis crime frequency by Year ") 
        fig,axes=plt.subplots(nrows=1,ncols=3,figsize=(20,6))
        sns.barplot(x=yearly_crime_count.index,y=yearly_crime_count.values,color='r',ax=axes[0])
        for bar in axes[0].patches:
            height = bar.get_height()
            axes[0].text(bar.get_x() + bar.get_width() / 2, height + 0.1, round(height), ha='center', va='bottom', fontsize=10)  # Adjust offset and font size as needed
       
        axes[0].set_xlabel('Year')
        axes[0].set_ylabel('No. of Crimes')
        axes[0].set_title('Crime Frequency by Year')
             
        #" Analyze Crime Frequency by Month:"
        # Resample by month and count occurrences
        monthly_crime_count = df['Date_Rptd'].dt.month.value_counts()
        sns.lineplot(x=monthly_crime_count.index, y=monthly_crime_count.values,marker='D',color='r',ax=axes[1])
        #crime count on the plot.
        for i, (x, y) in enumerate(monthly_crime_count.items()):
            axes[1].text(x, y + 0.1, str(y), ha='center', va='bottom', fontsize=10)  # Adjust offset and font size
        axes[1].set_xlabel('Month')
        axes[1].set_ylabel('Number of Crimes')
        axes[1].set_title('Crime Frequency by Month')
       


        # Resample by day of week and count occurrences
        day_of_week_crime_count = df['Date_Rptd'].dt.weekday.value_counts()

        # Plot the time series data       
        sns.lineplot(x=day_of_week_crime_count.index, y=day_of_week_crime_count.values,marker='D',color='r',label='no of crimes',ax=axes[2])
        # Loop through data points and add text labels
        for i, (x, y) in enumerate(day_of_week_crime_count.items()):
            axes[2].text(x, y + 0.1, str(y), ha='center', va='bottom', fontsize=8)  # Adjust offset and font size
        axes[2].set_xlabel('Day of Week (0: Monday)')
        axes[2].set_ylabel('Number of Crimes')
        axes[2].set_title('Crime Frequency by Day of Week')
        fig.show()
        plt.show()

        # 5. Spatial Analysis:
        # - Utilize the geographical information (Latitude and Longitude) to perform spatial analysis.
        # - Visualize crime hotspots on a map.
        #Spatial analysis 
        plt.figure(figsize=(10,10))
        sns.scatterplot(x=df['LON'], y=df['LAT'], alpha=0.5,color='red', label='crime')
        plt.title('Crime Incidents -geographical information (Lat and Long)')
        plt.legend(loc='upper right')
        plt.xlabel('Longitude')
        plt.ylabel('Latitude')
        plt.show()

        #Time Series Animation on Map:

        '''import plotly.express as px

        fig = px.scatter_mapbox(df, lat="LAT", lon="LON", color="Crm_Cd_Desc",
                        animation_frame="DATE_OCC", size_max=15, zoom=10)
        fig.update_layout(mapbox_style="open-street-map")
        fig.show()'''

        # Heat map


        heatmap_data=df[['LAT','LON','Vict_age','crmcd']].corr()
        # Step 3: Plot the heatmap
        plt.figure(figsize=(10, 8))
        sns.heatmap(heatmap_data, cmap='YlOrRd',annot=True)
        plt.title('Crime Incidents Heatmap')
        plt.xlabel('Longitude Bin')
        plt.ylabel('Latitude Bin')
        plt.show()

        # Victim demographics
        # 6. Victim Demographics:
        # - Investigate the distribution of victim ages and genders.
        # - Identify common premises descriptions where crimes occur.

        fig, axes = plt.subplots(1, 3, figsize=(15, 11))

        # Distribution of Victim Ages - Histogram
        sns.histplot(df['Vict_age'], bins=20, kde=True, ax=axes[0])
        axes[0].set_title('Distribution of Victim Ages')
        axes[0].set_xlabel('Age')
        axes[0].set_ylabel('Frequency')

        # Distribution of Victim Ages - KDE
        sns.kdeplot(df['Vict_age'], shade=True, ax=axes[1])
        axes[1].set_title('KDE of Victim Ages')
        axes[1].set_xlabel('Age')

        # Distribution of Victim Genders - Bar Plot
        sns.countplot(x='Vict_sex', data=df, ax=axes[2])
        axes[2].set_title('Distribution of Victim Genders')
        axes[2].set_xlabel('Gender')
        axes[2].set_ylabel('Count')
        for p in axes[2].patches:
            height = p.get_height()
            axes[2].text(
            p.get_x() + p.get_width() / 2., 
            height + 3, 
            '{:1.0f}'.format(height), 
            ha="center", 
            va="center", 
            fontsize=8, 
            color="black", 
            fontweight="bold"
            )

        plt.tight_layout()
        fig.show()
        plt.show()
        

        plt.figure(figsize=(6, 25))
        premises_count = df['Premis_Desc'].value_counts()
        ax=sns.barplot(x=premises_count.index, y=premises_count.values)
      
        plt.title('Common Premises Descriptions')
        plt.xlabel('Premises Description')
        plt.ylabel('Count')
        # for bar in ax.patches:
            # height = bar.get_height()
            # plt.text(bar.get_x() + bar.get_width() / 2, height + 0.1, int(height), ha='center', va='bottom', fontsize=4) 

        ax.set_xticklabels(ax.get_xticklabels(), rotation=45,fontsize=5)
        plt.show()

        # 7. Status Analysis:
        # - Examine the status of reported crimes.
        # - Classify crimes based on their current status.
    
        fig, axes = plt.subplots(1, 2, figsize=(16, 6))

        # Plot Count Plot for Crime Statuses
        sns.countplot(x='Status1', data=df, palette='Set2', ax=axes[0])
        axes[0].set_title('Status of Reported Crimes')
        axes[0].set_xlabel('Status')
        axes[0].set_ylabel('Count')
        axes[0].tick_params(axis='x', rotation=45)  # Rotate x-tick labels for better readability

        # Calculate the count of each crime status
        status_counts = df['Status1'].value_counts()
        # Plot Pie Chart for Crime Statuses
        axes[1].pie(status_counts, labels=status_counts.index, autopct='%1.1f%%', startangle=140, colors=plt.cm.Set2.colors)
        axes[1].set_title('Distribution of Reported Crime Statuses')
        axes[1].axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

        plt.tight_layout()
        plt.show()
        

        #Questions       
        #Spatial Analysis: Where are the geographical hotspots for reported crimes?
        print("----Spatial Analysis:---")

        # Create a scatter plot with latitude and longitude
        plt.figure(figsize=(12, 8))
        sns.scatterplot(x=df['LON'], y=df['LAT'], alpha=0.5)

        # Add a heatmap layer
        sns.kdeplot(x=df['LON'], y=df['LAT'], cmap="Reds", shade=True, shade_lowest=False)

        # Add labels and title
        plt.title('Crime of Reported Crimes', fontsize=18)
        plt.xlabel('Longitude', fontsize=14)
        plt.ylabel('Latitude', fontsize=14)
        plt.show()

        print()
        print("Q: Where are the geographical hotspots for reported crimes?")
        print("A: Based on the heatmap visualization, the geographical hotspot for reported crimes appears to be around the longitude range -118.3 to -118.2. The heatmap shows a concentrated area with a deep red color, indicating a high density or clustering of crime incidents around that longitude value.\nWhile the latitude range covers values from around 34.0 to 34.1, the hotspot is quite prominently visible along the longitude of -118.4, spanning a smaller latitude range concentrated towards the center of the plot.")
        print()



        # Location Analysis: Where do most crimes occur based on the "Location" column?
        # To analyze the locations where most crimes occur, we can use the value_counts method and visualize the results:
        # pythonCopy codeimport matplotlib.pyplot as plt

        # Count the occurrences of each location
        location_counts = df['Location'].value_counts()
        max10locationcounts=location_counts.nlargest(6)

        # Visualize the top 10 locations
        plt.figure(figsize=(10, 6))
        sns.barplot(x=max10locationcounts.index,y=max10locationcounts.values)
        plt.title('Locations for Reported Crimes')
        plt.xlabel('Location')
        plt.ylabel('Count')
        plt.xticks(rotation=60 ,fontsize=8)
        plt.show()

        print("----Location Analysis:---")
        print("Q: Where do most crimes occur based on the Location column?")
        print("A: The location for reported barplot cleary shows that most of the crime occurs in '800 N Alameda street' with 14 crimes ")
        print()
      




        # Crime Code Analysis: What is the distribution of reported crimes based on Crime Code?
        # To analyze the distribution of reported crimes based on the Crime Code, we can use the value_counts method and visualize the results:
      
        # Count the occurrences of each crime code
        crime_code_counts = df['crmcd'].value_counts()

    
        # Create a bar plot using Seaborn
        plt.figure(figsize=(12, 6))
        ax1=sns.barplot(x=crime_code_counts.index, y=crime_code_counts.values)
        # Loop through bars and add text labels
        for bar in ax1.patches:
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width() / 2, height + 0.1, int(height), ha='center', va='bottom', fontsize=8)  # Adjust offset and font size as needed

        plt.title('Distribution of Reported Crimes by Crime Code', fontsize=16)
        plt.xlabel('Crime Code', fontsize=14)
        plt.ylabel('Count', fontsize=14)
        plt.xticks(rotation=90)
        plt.show()
        print("----CrimeCode analysis:---")
        print("Q: What is the distribution of reported crimes based on Crime Code?")
        print("A: The distribution of reported crimes by Crime Code is as follows:",end="\n ")
        print("Distribution Plot shows the top Crime Codes with the highest counts of reported crimes are:")

        print("Crime Code 330 (82 reported crimes) -BURGLARY FROM VEHICLE")
        print("Crime Code 624 (74 reported crimes) -BATTERY - SIMPLE ASSAULT");
        print("Crime Code 440 (44 reported crimes) -THEFT PLAIN - PETTY ($950 & UNDER)");
        print("Crime Code 442 (28 reported crimes) -SHOPLIFTING - PETTY THEFT ($950 & UNDER)")
        print("Crime Code 510 (28 reported crimes) -VEHICLE - STOLEN")
        print("Crime Code 341 (26 reported crimes) -THEFT-GRAND ($950.01 & OVER)EXCPT,GUNS,FOWL")
        print("Crime Code 230 (24 reported crimes) -ASSAULT WITH DEADLY WEAPON, AGGRAVATED ASSAULT")
        print("There are several other Crime Codes with lower but still notable counts, such as 480, 662, 740, 888, and 930.",end="")
        print("The majority of the Crime Codes have relatively low counts, with many codes having single-digit frequencies or close to zero.")
       
            
except Exception as e:
        print(e)
finally:
    pass
   

                 
                 