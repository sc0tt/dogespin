import hashlib
import requests
import re
import time
import random


secret_addr = ''
spin_url = 'http://dogespin.l8.lv/ajax-spin.php'
root_url = 'http://dogespin.l8.lv/'
hash_re = re.compile(r'spinHash=\'([0-9abcdef]+)\'')
colors = ['black','red']

def get_next_hash(url=root_url):
    r = requests.get(url)
    hash = hash_re.findall(r.text)
    return hash[0] if hash else None

def spin(color, bet, hash=get_next_hash, balance=0, spin_url=spin_url, secret=secret_addr):

    if callable(hash):
        hash = hash()

    if color not in colors:
        raise ValueError("invalid color '%s'" % color)

    bet = int(bet)

    if not bet:
        raise ValueError("invalid bet '%s'")

    data = {
        'mode': 'realmoney',
        'spinHash': hash,
        'secretURL': secret,
        'bet': 'cell-%s:%s;' % (color, bet)
    }
    if balance:
        data['balance'] = balance
        data['mode'] = 'playmoney'
        del data['secretURL']

    response = requests.post(spin_url, data)
    if response and not response.text == "ERROR":
        response_values = response.text.split(':')
        (result,balance,bet_value,payout,
         change,game_hash,hash_data,next_spin_hash) = response_values[0:8]

        return [result, balance, bet_value, change, next_spin_hash, payout, hash_data, game_hash]

    else:
        print "Got error. Trying again..."
        return spin(color, bet, hash=hash, balance=balance, secret=secret)
        #return response.text, response

def rsleep(rs):
    rnd = (random.random())
    if rs and not isinstance(rs, list):
        secs = rs
    elif isinstance(rs, list) and len(rs) > 0:
        secs = random.sample(rs, 1)[0]
    else:
        secs = random.randint(1,10)

    print "sleeping %ss" % secs
    time.sleep(secs)

def get_color(col):
    return colors[random.randint(0,1) if col == 'rand' else col]

def start_spinner(secret, starting_bet=1, max_bet=64, play=0, qt_loss=100, qt_win=1000, rs=0, col='rand'):
    """
    Start spinner
    """
    next_color = get_color(col)
    next_bet = starting_bet
    next_hash = get_next_hash()
    rsleep(rs)
    total_payout = 0
    roll = 0

    print " "
    try:
        while True:
            try:
                roll += 1
                print "Roll #%s" % roll
                print "Now betting %s DOGE on %s. [spinHash: %s]" % (next_bet, next_color, next_hash)
                result = spin(next_color, next_bet, next_hash, play, secret=secret)
                if result[0]=="ERROR":
                    return result
            except requests.HTTPError:
                print "HTTP error"
            else:
                rolled = result[0]
                balance = int(result[1])
                bet = int(result[2])
                change = int(result[3])
                hash_data = result[6]

                total_payout += change

                if play:
                    play = balance

                if not next_hash == hashlib.sha256(hash_data).hexdigest():
                    print "HASH MISMATCH: %s" % [result]
                    raise KeyboardInterrupt

                next_hash = result[4]


                print "rolled %s" % rolled
                print "Change:      %s DOGE" % change
                print "Balance:     %s DOGE" % balance
                print "Totals:      %s DOGE" % total_payout
                print "----------------------"

                next_color = get_color(col)

                if change < 0 and bet <= max_bet:
                    next_bet = bet*2
                    if next_bet > balance:
                        balance = next_bet
                        print "\nBetting remaining balance\n"
                    else:
                        print "\nDoubling\n"
                else:
                    print "\nResetting bet\n"
                    next_bet = starting_bet

                if qt_loss and total_payout <= qt_loss * -1:
                    print "Significant loss"
                    raise KeyboardInterrupt

                if qt_win and total_payout >= qt_win:
                    print "Significant win"
                    raise KeyboardInterrupt

            finally:
                rsleep(rs)
    except KeyboardInterrupt:
        print "Stopping..."
        print "%s: %s DOGE" % ("Totals:", total_payout)
