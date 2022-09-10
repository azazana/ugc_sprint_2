# MONGO
# QuickStart

Для запуска теста необходимо выполнить следующие команды:
```
docker-compose -f mongo/docker-compose.yaml up  --build
bash mongo/build.sh
pip install -r requirements.txt
python -m mongo.run_test_mongodb
```


# Результат

### Запись
По записи данных была получена следующая статистика:
Statistics for likedFilms batch_size=1: batch=0.013479900360107423 sec, item=0.013479900360107423 sec.
Statistics for likedFilms batch_size=10: batch=0.052527785301208496 sec, item=0.00525277853012085 sec.
Statistics for likedFilms batch_size=50: batch=0.2022796630859375 sec, item=0.00404559326171875 sec.
Statistics for likedFilms batch_size=100: batch=0.33747124671936035 sec, item=0.0033747124671936034 sec.
Statistics for likedFilms batch_size=200: batch=0.7114530324935913 sec, item=0.003557265162467956 sec.
Statistics for likedFilms batch_size=500: batch=1.7214728832244872 sec, item=0.0034429457664489744 sec.
Statistics for likedFilms batch_size=1000: batch=3.6413838863372803 sec, item=0.0036413838863372803 sec.
Statistics for likedFilms batch_size=2000: batch=7.022547769546509 sec, item=0.0035112738847732543 sec.
Statistics for likedFilms batch_size=5000: batch=23.775467944145202 sec, item=0.00475509358882904 sec.

Statistics for reviews batch_size=1: batch=0.0466902494430542 sec, item=0.0466902494430542 sec.
Statistics for reviews batch_size=10: batch=0.09635014533996582 sec, item=0.009635014533996582 sec.
Statistics for reviews batch_size=50: batch=0.3759873390197754 sec, item=0.007519746780395508 sec.
Statistics for reviews batch_size=100: batch=0.5351887464523315 sec, item=0.005351887464523315 sec.
Statistics for reviews batch_size=200: batch=0.9992843389511108 sec, item=0.004996421694755554 sec.
Statistics for reviews batch_size=500: batch=3.114255166053772 sec, item=0.006228510332107544 sec.
Statistics for reviews batch_size=1000: batch=5.287348914146423 sec, item=0.005287348914146423 sec.
Statistics for reviews batch_size=2000: batch=10.755072021484375 sec, item=0.005377536010742188 sec.
Statistics for reviews batch_size=5000: batch=26.47390511035919 sec, item=0.005294781022071838 sec.

Statistics for bookmarks batch_size=1: batch=0.015179729461669922 sec, item=0.015179729461669922 sec.
Statistics for bookmarks batch_size=10: batch=0.06812996864318847 sec, item=0.006812996864318847 sec.
Statistics for bookmarks batch_size=50: batch=0.2801589727401733 sec, item=0.005603179454803466 sec.
Statistics for bookmarks batch_size=100: batch=0.5132446527481079 sec, item=0.005132446527481079 sec.
Statistics for bookmarks batch_size=200: batch=0.9281452894210815 sec, item=0.004640726447105408 sec.
Statistics for bookmarks batch_size=500: batch=2.3516997575759886 sec, item=0.004703399515151977 sec.
Statistics for bookmarks batch_size=1000: batch=4.911527848243713 sec, item=0.004911527848243713 sec.
Statistics for bookmarks batch_size=2000: batch=10.182706379890442 sec, item=0.005091353189945221 sec.
Statistics for bookmarks batch_size=5000: batch=25.45936198234558 sec, item=0.005091872396469116 sec.


Установлен оптимальный размер батча для записи: 200 элементов.

### Чтение
Эксперимент на определение среднего времени чтения проводился по пользователям со средним числом записей 500:
Statistics read for likedFilms for ~500 records: 0.0862428069114685 sec.
Statistics read for reviews for ~500 records: 0.12841233015060424 sec
Statistics read for bookmarks for ~500 records: 0.08799453973770141 sec

# CLICKHOUSE
# QuickStart

Для запуска теста необходимо выполнить следующие команды:
```
docker-compose -f clickhouse/docker-compose.yml up --build
python -m clickhouse_research.run_test_clickhouse
```

# Результат

### Запись
По записи данных была получена следующая статистика:
Statistics for likedFilms batch_size=1: batch=0.004770874977111816 sec, item=0.004770874977111816 sec.
Statistics for likedFilms batch_size=10: batch=0.00287933349609375 sec, item=0.00028793334960937496 sec.
Statistics for likedFilms batch_size=50: batch=0.004152941703796387 sec, item=8.305883407592774e-05 sec.
Statistics for likedFilms batch_size=100: batch=0.00715789794921875 sec, item=7.15789794921875e-05 sec.
Statistics for likedFilms batch_size=200: batch=0.008411192893981933 sec, item=4.205596446990967e-05 sec.
Statistics for likedFilms batch_size=500: batch=0.015138792991638183 sec, item=3.0277585983276366e-05 sec.
Statistics for likedFilms batch_size=1000: batch=0.022112727165222168 sec, item=2.211272716522217e-05 sec.
Statistics for likedFilms batch_size=2000: batch=0.043812108039855954 sec, item=2.1906054019927976e-05 sec.
Statistics for likedFilms batch_size=5000: batch=0.09539484977722168 sec, item=1.9078969955444335e-05 sec.

Statistics for reviews batch_size=1: batch=0.0025986194610595702 sec, item=0.0025986194610595702 sec.
Statistics for reviews batch_size=10: batch=0.0029400348663330077 sec, item=0.00029400348663330075 sec.
Statistics for reviews batch_size=50: batch=0.004486966133117676 sec, item=8.973932266235352e-05 sec.
Statistics for reviews batch_size=100: batch=0.005170154571533203 sec, item=5.170154571533203e-05 sec.
Statistics for reviews batch_size=200: batch=0.007489728927612305 sec, item=3.744864463806152e-05 sec.
Statistics for reviews batch_size=500: batch=0.01506788730621338 sec, item=3.0135774612426758e-05 sec.
Statistics for reviews batch_size=1000: batch=0.025522661209106446 sec, item=2.5522661209106446e-05 sec.
Statistics for reviews batch_size=2000: batch=0.045387983322143555 sec, item=2.269399166107178e-05 sec.
Statistics for reviews batch_size=5000: batch=0.10190153121948242 sec, item=2.0380306243896485e-05 sec.

Statistics for bookmarks batch_size=1: batch=0.0026030778884887696 sec, item=0.0026030778884887696 sec.
Statistics for bookmarks batch_size=10: batch=0.0026664018630981447 sec, item=0.0002666401863098145 sec.
Statistics for bookmarks batch_size=50: batch=0.005412793159484864 sec, item=0.00010825586318969728 sec.
Statistics for bookmarks batch_size=100: batch=0.005208992958068847 sec, item=5.2089929580688475e-05 sec.
Statistics for bookmarks batch_size=200: batch=0.010235905647277832 sec, item=5.117952823638916e-05 sec.
Statistics for bookmarks batch_size=500: batch=0.015186595916748046 sec, item=3.037319183349609e-05 sec.
Statistics for bookmarks batch_size=1000: batch=0.023259353637695313 sec, item=2.3259353637695315e-05 sec.
Statistics for bookmarks batch_size=2000: batch=0.03979260921478271 sec, item=1.9896304607391357e-05 sec.
Statistics for bookmarks batch_size=5000: batch=0.0913726806640625 sec, item=1.82745361328125e-05 sec.

### Чтение
Эксперимент на определение среднего времени чтения проводился по пользователям со средним числом записей 500:
Statistics read for likedFilms for ~500 records: 0.01486828327178955 sec
Statistics read for reviews for ~500 records: 0.030370545387268067 sec
Statistics read for bookmarks for ~500 records: 0.018959081172943114 sec


