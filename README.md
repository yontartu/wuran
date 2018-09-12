# Pollution & Politics	

There is ample anecdotal evidence that Chinese authorities are able to exert control over urban air pollution, at least to some extent. For example, prior to the 2008 Beijing Olympics, it was widely understood that the Chinese government regulated factory output and the number of cars on the road in order to reduce air pollution in Beijing prior to the Opening Ceremony. The reasoning behind such an action was to improve the image of China in the eyes of the international community, especially as the Olympics was going to draw special attention to Beijing. This raises the question of whether Chinese authorities have sought to control the level of air pollution during other politically important events. Official visits to China from representatives of foreign governments could be one type of such events. For instance, in November 2017 President Xi Jinping hosted President Donald Trump for an official visit between the two heads of state in Beijing. Winter months in Beijing are known to have elevated levels of air pollution, typically averaging upwards of an Air Quality Index (AQI) score of 100, but for the three days prior to Trump’s visit, Beijing enjoyed blue skies. The fact that Trump’s visit was greeted with unpolluted air—particularly since other elements of Trump’s visit, such as the lavish state dinner held in the Forbidden City, were designed to impress the US president—may suggest that the Chinese government at certain times intervenes in order to “turn down” the level of pollution ahead of visits from heads of state from other countries. 

I seek to probe this question by developing a novel approach to quantify China’s bilateral relationships through air pollution. My project can be seen as an attempt to develop an index of political importance using AQI data—how strategically important China views each of its relationships with other countries through a pollution “score.” I plan to collect daily air pollution data from the US State Department (particulate matter readings taken from the US Embassy in Beijing that are then converted into AQI values) and match them with data on visits to Beijing by foreign government representatives, taken from aggregated news reports collected by China Vitae (a project of the Carnegie Endowment for International Peace that tracks the appearances and travel of leading Chinese officials). While I expect to find that days with lower levels of pollution coincide with visits from powerful Western powers (such as the United States) and countries with closer ties (such as Russia), I hypothesize that officials’ visits from countries with historically poor relations or those with antagonistic relations (such as Japan) will be held on days with higher levels of air pollution. This phenomenon would suggest that there are certain instances in which Beijing is attempting to create a positive impression on foreign dignitaries, and in other cases it isn’t. I also hope to extend my analysis beyond creating a “pollution index” by trying to convert my findings into economics terms, in other words to compute a sort of “price tag” associated with each state visit. For instance, if each marginal reduction in AQI can be translated into a certain number of factory closures, an associated reduction in economic output can be computed for each state visit. 

## Set-Up Instructions

##### 1. Download raw pollution data from the State Department

```
$ bash download_data.sh
```

##### 2. Clean pollution data of unrecognizable characters (in "unit" column)

```
$ bash clean_datafiles.sh
```

##### 3. Scrape official visit activity data from [China Vitae](http://chinavitae.com/) (helpful directions from the [Scrapy tutorial](https://doc.scrapy.org/en/1.5/intro/tutorial.html))

```
$ scrapy start project chvitae # start a new scrapy project
$ scrapy crawl activity -0 activity_20180320.json

```

##### 4. Analysis - merge pollution data with China Vitae activity data

```
$ jupyter notebook
```

## To Do

* regex city name out of raw datafile for new cleaned filename
* 


