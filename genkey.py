import bitcoin
import requests
import sys
import time

total = 2000000  # total number to reach
bar_length = 30  # should be less than 100
count = 0
i=1

print("Started search...")

def run():
    while True:
        for i in range(total+1):
            percent = 100.0*i/total
            sys.stdout.write('\r')
            sys.stdout.write("Completed: [{:{}}] {:>3}% - "
                             .format('='*int(percent/(100.0/bar_length)),
                                     bar_length, int(percent)))
            valid_private_key = False
            while not valid_private_key:
                private_key = bitcoin.random_key()
                decoded_private_key = bitcoin.decode_privkey(private_key, 'hex')
                valid_private_key = 0 < decoded_private_key < bitcoin.N
                wif_encoded_private_key = bitcoin.encode_privkey(decoded_private_key, 'wif')
                public_key = bitcoin.fast_multiply(bitcoin.G, decoded_private_key)
                r = requests.get("https://blockchain.info/q/getsentbyaddress/"+bitcoin.pubkey_to_address(public_key))
                count = i + 1
                print "Key",count, private_key
                #time.sleep(1.000)
               
                                  
                        

                

            if int(r.text) > 0:
                sys.stdout = open('privkeys.txt', 'w')
                print("Bitcoin Address is:", bitcoin.pubkey_to_address(public_key))
                print("Private Key is: ", wif_encoded_private_key)
                print("Balance is: ",r.text)
                break
                sys.stdout.close()
                sys.stdout.flush()
            

while True:
    try:
        run()
    except Exception as ex:
        print(ex)
