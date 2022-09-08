# QuickStart

Для запуска теста необходимо выполнить следующие команды:
```
docker-compose up --build
bash build.sh
pip install -r requirements.txt
python test.pys
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
