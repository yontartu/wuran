# Pollution & Politics	

Intro blah blah blah

## Set-Up Instructions

loren ipsum

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


