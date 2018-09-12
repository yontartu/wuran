for filename in `ls ~/projects/aqi/data/B*` 
do year=`echo $filename | grep -Eo '_[[:digit:]]{4}'` 
  file="beijing"$year
  #file=`echo $
  echo $file
  touch $file
  cut -d, -f1-8,10-11 $filename >> $file
  mv $file data/$file
done