Dogespin
========

Install
-------

    pip install git+git://github.com/powhex/dogespin.git

Use
---

    import dogespin
    dogespin.secret_addr = 'your secret hash, found in url query string'
    dogespin.start_spinner()


Options for start_spinner():

```
play = 0: play with real money
play >= 0: play with play money (value of 'play' is your balance)

qt_loss = 0: play forever
qt_loss >= 0: play until total loss matches or exceeds value of 'qt_loss'

qt_win = 0: play forever
qt_win >= 0: play until total win matches or exceeds value of 'qt_win'

rs = 0: use randomized sleep time from 1 to 10 seconds
rs >= 0: use value of 'rs' as sleep time
rs = type list: use random list item as sleep time

col = "rand": bet on random color
col = 0: bet on black
col = 1: bet on red
```
