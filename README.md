Dogespin
========

dogespin.l8.lv auto roulette bot

Install
-------

    pip install git+git://github.com/powhex/dogespin.git

Use
---

    import dogespin
    dogespin.start_spinner('your secret hash')


Options for start_spinner():

```
secret: your secret hash, found in url query string on dogespin.l8.lv

starting_bet: your starting bet (default = 1)
max_bet: will double no further, resetting current bid to 'starting_bet' (default = 64)

play = 0: play with real money (this is the default)
play > 0: play with play money (value of 'play' is your balance)

qt_loss = 0: play forever
qt_loss > 0: play until total loss matches or exceeds value of 'qt_loss' (default = 100)

qt_win = 0: play forever
qt_win > 0: play until total win matches or exceeds value of 'qt_win' (default = 1000)

rs = 0: use randomized sleep time from 1 to 10 seconds (this is the default)
rs > 0: use value of 'rs' as sleep time
rs = type list: use random list item as sleep time

col = "rand": bet on random color (this is the default)
col = 0: bet on black
col = 1: bet on red
```

Contributing
------------

If you'd like to contribute code, make a pull request

Also accepting donations in dogecoins, naturally :)

    DNuU16DfQSf7r9JfyM8VZKU1qb567PDAC6
