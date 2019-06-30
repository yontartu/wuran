# Blue Skies for Allies? Quantifying China’s Foreign Relations Using Air Pollution Readings

There is ample anecdotal evidence that Chinese authorities are able to exert control over urban air pollution, at least to some extent. For example, prior to the 2008 Beijing Olympics, it was widely understood that the Chinese government regulated factory output and the number of cars on the road in order to reduce air pollution in Beijing prior to the Opening Ceremony. The reasoning behind such an action was to improve the image of China in the eyes of the international community, especially as the Olympics was going to draw special attention to Beijing. This raises the question of whether Chinese authorities have sought to control the level of air pollution during other politically important events. Official visits to China from representatives of foreign governments could be one type of such events. For instance, in November 2017 President Xi Jinping hosted President Donald Trump for an official visit between the two heads of state in Beijing. Winter months in Beijing are known to have elevated levels of air pollution, typically averaging upwards of an Air Quality Index (AQI) score of 100, but for the three days prior to Trump’s visit, Beijing enjoyed blue skies. The fact that Trump’s visit was greeted with unpolluted air—particularly since other elements of Trump’s visit, such as the lavish state dinner held in the Forbidden City, were designed to impress the US president—may suggest that the Chinese government at certain times intervenes in order to “turn down” the level of pollution ahead of visits from heads of state from other countries. 

I seek to probe this question by developing a novel approach to quantify China’s bilateral relationships through air pollution. My project can be seen as an attempt to develop an index of political importance using AQI data—how strategically important China views each of its relationships with other countries through a pollution “score.” Air pollution data comes from the US State Department (particulate matter readings taken from the US Embassy in Beijing that are then converted into AQI values) and data on visits to Beijing by foreign government representatives comes from China Vitae (a Carnegie Endowment for International Peace project that tracks the appearances and travel of leading Chinese officials). 

![alt text](https://github.com/yontartu/wuran/blob/master/img/pollution/7_trump_visit_aqi.png)

![alt text](https://github.com/yontartu/wuran/blob/master/img/analysis/16_top_21_estimates.png)

## Set-Up Instructions

##### 1. Download pollution data from the [State Department](https://airnow.gov/index.cfm?action=airnow.global_summary#China$Beijing) and weather data from [NOAA](https://www.ncdc.noaa.gov/isd).

```
$ bash download_pollution_data.sh
$ python download_noaa_data.py
```

##### 2. Scrape state visit data from [China Vitae](http://chinavitae.com/) using [Scrapy](https://docs.scrapy.org/en/latest/#).

```
$ scrapy start project chvitae 
$ scrapy crawl activity -o activity_data.json -L WARN
$ python scrape_officials_titles.py
$ python extract_countries.py
```

##### 3. Analysis: Merge pollution data with state visit data and weather data

```
$ jupyter notebook beijing_aqi_analysis.ipynb
```

Results from my statistical analysis can be found [here](https://github.com/yontartu/wuran/tree/master/img/analysis), as well as [robustness checks](https://github.com/yontartu/wuran/tree/master/img/robustness_checks) I perform. I've also built some data visualizations exploring the [pollution](https://github.com/yontartu/wuran/tree/master/img/pollution), [state visit](https://github.com/yontartu/wuran/tree/master/img/chinavitae) and [weather](https://github.com/yontartu/wuran/tree/master/img/weather) data.

##### Other helpful resources

A [country-nationality crosswalk](https://github.com/Dinu/country-nationality-list/blob/master/countries.csv) compiled by `Dinu` was super helpful. Another useful reference was this [country list](https://github.com/umpirsky/country-list/) from `umpirsky`. I've made some modifications for my use case; see `cleaning_countries.ipynb` for details. 
