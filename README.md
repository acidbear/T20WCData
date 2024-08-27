# Women's ICC T20 World Cups Data (2014-2023) 

 The ICC Women's T20 World Cup is a (generally) bi-annual international cricket tournament. This repo stores the files used in making some data visulisations for the tournaments taking place in 2014, 2016, 2018, 2020 and 2023, where I compared various statisics and trends across tournaments. I did this in two different ways, first by using general match overview data and then by using ball by ball data. 

## File Structure
**'Finished Notebooks'** -> The final versions of the notebooks containing all the code to generate the charts can be found in here, as well as a pdf version of each notebook.

**'CSV files'** -> These contain csv exports of all the pandas dataframes which were used to create the charts. These contained the cleaned, raw data taken from cricsheets. 

**'Cleaning Scipts'** -> These contain the scripts used to create the dataframes, taking the hundreds of json files of original data and formatting it into a useable dataframe, with some useful additional columns.

**'icc_.._json'** -> The original downloads of the json files.

## Sources and external links
The original data was downloaded from :  https://cricsheet.org/matches/

The data for a couple of missing matches was taken from : https://www.espncricinfo.com/
***
All of the datsets stored in 'csv files' have also been uploaded to kaggle and can be found at:
https://www.kaggle.com/datasets/acidbear55/icc-womens-t20-world-cups-2014-2023

Copies of the notebook can also be found on kaggle (with code cells hidden):
 - Overview : https://www.kaggle.com/code/acidbear55/women-s-t20-world-cups-data-visualisation
 - Ball by Ball : https://www.kaggle.com/code/acidbear55/women-s-icc-t20-world-cup-ball-by-ball
