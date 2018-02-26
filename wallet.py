#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb 18 15:37:09 2018

@author: woradanue nakdee, 6020411004
"""

from datetime import datetime
import requests
import sqlite3

class Wallet:
    '''
    simulate digital wallet: send/receive, transaction record, exchange rate, currency conversion
    '''
    def __init__(self, filename = '', tag = '', amount = ''):
        self._filename = filename
        self._tag = tag
        self._amount = amount
    
    #main menu
    def show_menu(self):
        while True:
            print('\nMain Menu')
            print('1: Get current exchange rate')
            print('2: Send and receive currency')
            print('3: Get transaction record')
            print('4: Currency conversion')
            choice_in = input('Enter an option: ')
            try:
                choice = int(choice_in)
                if choice == 1:
                    self.current()
                elif choice == 2:
                    self.transaction()
                elif choice == 3:
                    self.record()
                elif choice == 4:
                    self.convert()
                else:
                    print('Invalid input. Please enter a provided number.')
                    self.show_menu()
                break
            except:
                print('Invalid input. Please enter a provided number.')
                continue
    
    # at end of each sub-menu. get back to main menu
    def back_to_menu(self):
        choice1 = input('Back to main menu? (Y/N): ')
        if choice1 == 'Y' or choice1 == 'y':
            self.show_menu()
    
    # 1 sub-menu for current currency rate
    def current(self):
        print('\nCurrent exchange rate in USD')
        call = requests.get('https://min-api.cryptocompare.com/data/pricemulti?fsyms=BTC,ETH&tsyms=USD') #request api
        call2 = requests.get('https://free.currencyconverterapi.com/api/v5/convert?q=THB_USD&compact=ultra')
        print(datetime.now())
        api_data = call.json() #parsing json
        api_data2 = call2.json()
        btc_print = api_data['BTC']['USD'] 
        eth_print = api_data['ETH']['USD']
        thb_print = api_data2['THB_USD']
        print('1 BTC = \t$', btc_print, '\n1 ETH = \t$', eth_print, '\n1 THB = \t$', thb_print)
        self.back_to_menu()
    
    # 2 sub-menu for send/ receive currency
    def transaction(self):
        while True:
            try:
                print('\nTransaction\nUSD\tTHB\tBTC\tETH')
                choice2 = input('Select currency: ')
                if choice2 == 'USD' or choice2 == 'usd':
                    self.usd_wallet()
                elif choice2 == 'BTC' or choice2 == 'btc':
                    self.btc_wallet()
                elif choice2 == 'ETH' or choice2 == 'eth':
                    self.eth_wallet()
                elif choice2 == 'THB' or choice2 == 'thb':
                    self.thb_wallet()
                else:
                    print('Invalid input. Please enter a provided symbol.')
                    self.transaction()
                break
            except:
                print('Invalid input. Please enter a provided symbol.')
                self.transaction()
 
    # sub-sub-menu send/ receive USD, write to file
    def usd_wallet(self, tag = '', amount = ''):
        print('USD Wallet')
        conn = sqlite3.connect('usdwallet.db')
        c = conn.cursor()
        date = datetime.now()
        tag = input('Send or Receive: ')
        amount = float(input('Amount USD: '))
        if tag == 'send' or tag == 'Send':
            amount = amount * -1
        c.execute('INSERT INTO currency Values (?, ?, ?)', (date, tag, amount))
        conn.commit()
        self.usd_record() 
        
    def btc_wallet(self, tag = '', amount = ''):
        print('BTC Wallet')
        conn = sqlite3.connect('btcwallet.db')
        c = conn.cursor()
        date = datetime.now()
        tag = input('Send or Receive: ')
        amount = float(input('Amount BTC: '))
        if tag == 'send' or tag == 'Send':
            amount = amount * -1
        c.execute('INSERT INTO currency Values (?, ?, ?)', (date, tag, amount))
        conn.commit()
        self.btc_record()
        
    def eth_wallet(self, tag = '', amount = ''):
        print('ETH Wallet')
        conn = sqlite3.connect('ethwallet.db')
        c = conn.cursor()
        date = datetime.now()
        tag = input('Send or Receive: ')
        amount = float(input('Amount ETH: '))
        if tag == 'send' or tag == 'Send':
            amount = amount * -1
        c.execute('INSERT INTO currency Values (?, ?, ?)', (date, tag, amount))
        conn.commit()
        self.eth_record() 
        
    def thb_wallet(self, tag = '', amount = ''):
        print('THB Wallet')
        conn = sqlite3.connect('thbwallet.db')
        c = conn.cursor()
        date = datetime.now()
        tag = input('Send or Receive: ')
        amount = float(input('Amount THB: '))
        if tag == 'send' or tag == 'Send':
            amount = amount * -1
        c.execute('INSERT INTO currency Values (?, ?, ?)', (date, tag, amount))
        conn.commit()
        self.thb_record()
    
    # 3 sub-menu for transaction record
    def record(self):
        while True:
            try:
                print('\nWallets\nUSD\tBTC\tETH\tTHB')
                choice3 = input('Select currency: ')
                if choice3 == 'USD' or choice3 == 'usd':
                    self.usd_record()
                elif choice3 == 'BTC' or choice3 == 'btc':
                    self.btc_record()
                elif choice3 == 'ETH' or choice3 == 'eth':
                    self.eth_record()
                elif choice3 == 'THB' or choice3 == 'thb':
                    self.thb_record()
                else:
                    print('Invalid input. Please enter a provided symbol.')
                    return self.record()
                break
            except:
                print('Invalid input. Please enter a provided symbol.')
                return self.record()
    
    # sub-sub-menu USD transaction record, read from file, show send/ receive records
    def usd_record(self):
        conn = sqlite3.connect('usdwallet.db')
        c = conn.cursor()
        print('\nUSD transaction record')
        for row in c.execute('SELECT * FROM currency ORDER BY DATE'):
            print(row)
        c.execute('SELECT total(amount) FROM currency') #sum total amount from table
        print('USD Total: ', c.fetchone()[0])
        conn.close()
        self.back_to_menu()
    
    def btc_record(self):
        conn = sqlite3.connect('btcwallet.db')
        c = conn.cursor()
        print('\nBTC transaction record')
        for row in c.execute('SELECT * FROM currency ORDER BY DATE'):
            print(row)
        c.execute('SELECT total(amount) FROM currency')
        print('BTC Total: ', c.fetchone()[0])
        conn.close()
        self.back_to_menu()
    
    def eth_record(self):
        conn = sqlite3.connect('ethwallet.db')
        c = conn.cursor()
        print('\nETH transaction record')
        for row in c.execute('SELECT * FROM currency ORDER BY DATE'):
            print(row)
        c.execute('SELECT total(amount) FROM currency')
        print('ETH Total: ', c.fetchone()[0])
        conn.close()
        self.back_to_menu()
        
    def thb_record(self):
        conn = sqlite3.connect('thbwallet.db')
        c = conn.cursor()
        print('\nTHB transaction record')
        for row in c.execute('SELECT * FROM currency ORDER BY DATE'):
            print(row)
        c.execute('SELECT total(amount) FROM currency')
        print('THB Total: ', c.fetchone()[0])
        conn.close()
        self.back_to_menu()
            
    # sub-menu for currency conversion
    def convert(self):
        while True:
            try:
                print('\nCurrency conversion')
                self.usd_amount = input('Enter USD amount: ')
                print('\nConvert to? \nBTC\tETH\tTHB')
                choice4 = input('Select currency:  ')
                if choice4 == 'BTC' or choice4 == 'btc':
                    self.btc_convert()
                elif choice4 == 'ETH' or choice4 == 'eth':
                    self.eth_convert()
                elif choice4 == 'THB' or choice4 == 'thb':
                    self.thb_convert()
                else:
                    print('Invalid input. Please enter a provided symbol.')
                    return self.convert()
                break
            except:
                print('Invalid input. Please enter a provided symbol.')
                return self.convert()
    
    # sub-sub-menu convert from USD to BTC
    def btc_convert(self):
        btc_call = requests.get('https://min-api.cryptocompare.com/data/price?fsym=USD&tsyms=BTC')
        btc_data = btc_call.json()
        btc_usd = float(self.usd_amount) * btc_data['BTC']
        print(f'{self.usd_amount} USD equlas {btc_usd:.8f} BTC') # 0.00000001 BTC, one satoshi, decimal place, 10^-8
        self.convert_again()
    
    def eth_convert(self):
        eth_call = requests.get('https://min-api.cryptocompare.com/data/price?fsym=USD&tsyms=ETH')
        eth_data = eth_call.json()
        eth_usd = float(self.usd_amount) * eth_data['ETH']
        print(f'{self.usd_amount} USD equals {eth_usd:.8f} ETH')
        self.convert_again()
    
    def thb_convert(self):
        thb_call = requests.get('https://free.currencyconverterapi.com/api/v5/convert?q=USD_THB&compact=ultra')
        thb_data = thb_call.json()
        thb_usd = float(self.usd_amount) * thb_data['USD_THB']
        print(f'{self.usd_amount} USD equals {thb_usd:.2f} THB')
        self.convert_again()
    
    def convert_again(self):
        ask3 = input('Convert currency again? (Y/N): ')
        if ask3 == 'Y' or ask3 == 'y':
            self.convert()
        else:
            self.back_to_menu()
    
    #create db file with table
    def create_table(self, filename = ''):
        conn = sqlite3.connect(filename)
        c = conn.cursor()
        c.execute('''CREATE TABLE currency (date, tag, amount) ''')
        conn.commit()
        conn.close()


wallet1 = Wallet()
wallet1.show_menu()
#wallet1.create_table('thbwallet.db')




