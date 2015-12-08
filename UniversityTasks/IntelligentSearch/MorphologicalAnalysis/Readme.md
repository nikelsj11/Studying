

```
абака | сущ неод ед жен им | 144753
  абаки | сущ неод ед жен род | 312978
  абаке | сущ неод ед жен дат | 312979
  абаку | сущ неод ед жен вин | 312980
  абакою | сущ неод ед жен тв | 312983
  абакой | сущ неод ед жен тв | 312981
  абаке | сущ неод ед жен пр | 312982
абаки | сущ неод мн им | 4144167
  абак | сущ неод мн род | 4144168
  абакам | сущ неод мн дат | 4144169
  абаки | сущ неод мн вин | 4144172
  абаками | сущ неод мн тв | 4144170
  абаках | сущ неод мн пр | 4144171

*якающие | прл мн им | 1023417
  *якающих | прл мн род | 1023418
  *якающим | прл мн дат | 1023419
  *якающие | прл мн вин неод | 1023420
  *якающих | прл мн вин одуш | 1023423
  *якающими | прл мн тв | 1023421
  *якающих | прл мн пр | 1023422
```

```bash
home-work > mongo
MongoDB shell version: 2.2.4
connecting to: test
> db.test.find()
{ "_id" : 144753, "is_archaic" : false, "word" : "абака", "details" : "сущ неод ед жен им" }
{ "_id" : 312978, "prior" : 144753, "is_archaic" : false, "word" : "абаки", "details" : "сущ неод ед жен род" }
{ "_id" : 312979, "prior" : 144753, "is_archaic" : false, "word" : "абаке", "details" : "сущ неод ед жен дат" }
{ "_id" : 312980, "prior" : 144753, "is_archaic" : false, "word" : "абаку", "details" : "сущ неод ед жен вин" }
{ "_id" : 312983, "prior" : 144753, "is_archaic" : false, "word" : "абакою", "details" : "сущ неод ед жен тв" }
{ "_id" : 312981, "prior" : 144753, "is_archaic" : false, "word" : "абакой", "details" : "сущ неод ед жен тв" }
{ "_id" : 312982, "prior" : 144753, "is_archaic" : false, "word" : "абаке", "details" : "сущ неод ед жен пр" }
{ "_id" : 4144167, "is_archaic" : false, "word" : "абаки", "details" : "сущ неод мн им" }
{ "_id" : 4144168, "prior" : 4144167, "is_archaic" : false, "word" : "абак", "details" : "сущ неод мн род" }
{ "_id" : 4144169, "prior" : 4144167, "is_archaic" : false, "word" : "абакам", "details" : "сущ неод мн дат" }
{ "_id" : 4144172, "prior" : 4144167, "is_archaic" : false, "word" : "абаки", "details" : "сущ неод мн вин" }
{ "_id" : 4144170, "prior" : 4144167, "is_archaic" : false, "word" : "абаками", "details" : "сущ неод мн тв" }
{ "_id" : 4144171, "prior" : 4144167, "is_archaic" : false, "word" : "абаках", "details" : "сущ неод мн пр" }
{ "_id" : 1023417, "is_archaic" : true, "word" : "якающие", "details" : "прл мн им" }
{ "_id" : 1023418, "prior" : 1023417, "is_archaic" : true, "word" : "якающих", "details" : "прл мн род" }
{ "_id" : 1023419, "prior" : 1023417, "is_archaic" : true, "word" : "якающим", "details" : "прл мн дат" }
{ "_id" : 1023420, "prior" : 1023417, "is_archaic" : true, "word" : "якающие", "details" : "прл мн вин неод" }
{ "_id" : 1023423, "prior" : 1023417, "is_archaic" : true, "word" : "якающих", "details" : "прл мн вин одуш" }
{ "_id" : 1023421, "prior" : 1023417, "is_archaic" : true, "word" : "якающими", "details" : "прл мн тв" }
{ "_id" : 1023422, "prior" : 1023417, "is_archaic" : true, "word" : "якающих", "details" : "прл мн пр" }
```

```js
> db.test.getIndexes()
[
	{
		"v" : 1,
		"key" : {
			"_id" : 1
		},
		"ns" : "test.test",
		"name" : "_id_"
	},
	{
		"v" : 1,
		"key" : {
			"word" : 1
		},
		"ns" : "test.test",
		"name" : "word_1"
	}
]
```

```python2.7
DB_NAME = 'morph-dicts'
DB_COLLECTION = 'speakrus'
```


```js
> db.speakrus.count()
4159394
```

```
Словарь содержит  4 159 394 словоформ для 142 792  лемм.
```

```js
> db.speakrus.find({word: "мама"})
{ "_id" : 9557, "is_archaic" : false, "word" : "мама", "details" : "сущ одуш ед жен им" }
> db.speakrus.find({word: "мыла"})
{ "_id" : 425963, "prior" : 170154, "is_archaic" : false, "word" : "мыла", "details" : "сущ неод ед ср род" }
{ "_id" : 1533761, "is_archaic" : false, "word" : "мыла", "details" : "сущ неод мн им" }
{ "_id" : 1533764, "prior" : 1533761, "is_archaic" : false, "word" : "мыла", "details" : "сущ неод мн вин" }
{ "_id" : 78129, "prior" : 78128, "is_archaic" : false, "word" : "мыла", "details" : "гл несов перех прош ед жен" }
> db.speakrus.find({word: "раму"})
{ "_id" : 16656, "prior" : 16653, "is_archaic" : false, "word" : "раму", "details" : "сущ неод ед жен вин" }
> db.speakrus.find({word: "грыполутрамоном"})
>
```

```bash
home-work > recode CP1251..UTF8 War_and_Peace.txt
```
