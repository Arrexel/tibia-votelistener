import socket, sys, configparser, os, pymysql

os.system('cls||clear')

config = configparser.ConfigParser()

if not os.path.isfile('./VoteListener.ini'):
    config['LANGUAGE'] = {'lang': 'en'}
    config['VOTE LISTENER'] = {'ip': '127.0.0.1', 'port': 7272, 'key': 'YOUR_KEY_HERE'}
    config['TIBIA DATABASE'] = {'ip': '127.0.0.1', 'port': 3306, 'username': 'root', 'password': 'toor', 'database': 'tibia', 'table_prefix': ''}

    with open('VoteListener.ini', 'w') as configfile:
        config.write(configfile)
        print ('')
        print ('A config file named VoteListener.ini has been generated. Please edit it and re-launch the vote listener.')
        print ('For English, set lang = en (default)')
        print ('')
        raw_input('Press enter to exit...\n')
        sys.exit()

config.read('VoteListener.ini')
lang = config['LANGUAGE']['lang']
voteConfig = config['VOTE LISTENER']
dbConfig = config['TIBIA DATABASE']
tableName = dbConfig['table_prefix'] + "player_votes"

conn = pymysql.connect(host=dbConfig['ip'], port=int(dbConfig['port']), user=dbConfig['username'], password=dbConfig['password'], db=dbConfig['database'])
cur = conn.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS " + tableName + " (name varchar(255) CHARACTER SET utf8 NOT NULL, votes int(11) NOT NULL)")
cur.close()
conn.close()

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = (voteConfig['ip'], int(voteConfig['port']))
print >>sys.stderr, 'Starting vote listener on %s port %s' % server_address
sock.bind(server_address)
sock.listen(1)

while True:
    connection, client_address = sock.accept()
    output = ''
    try:
        
        while True:
            data = connection.recv(4096)
            output += data
            if not data:
                print (output)
                break
            
    finally:
        connection.close()
