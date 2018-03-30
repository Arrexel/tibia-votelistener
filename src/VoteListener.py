import socket, sys, configparser, os, pymysql

lang = None
bindIP = None
bindPort = None
key = None
dbUser = None
dbPass = None
dbIP = None
dbPort = None
dbDatabase = None
tableName = None

def clearTerminal():
    os.system('cls||clear')

def loadConfig():
    config = configparser.ConfigParser()
    if not os.path.isfile('./VoteListener.ini'):
        config['LANGUAGE'] = {'lang': 'en'}
        config['VOTE LISTENER'] = {'ip': '127.0.0.1', 'port': 7272, 'key': 'YOUR_KEY_HERE'}
        config['TIBIA DATABASE'] = {'ip': '127.0.0.1', 'port': 3306, 'username': 'root', 'password': 'toor', 'database': 'tibia', 'table_prefix': ''}
        with open('VoteListener.ini', 'w') as configfile:
            config.write(configfile)
            print ('')
            print ('A config file named VoteListener.ini has been generated. Please edit it and re-launch the vote listener.')
            print ('For English, set lang = en')
            print ('')
            print ('Um arquivo chamado VoteListener.ini foi gerado. Edite e renecie o arquivo votelistener.ini.')
            print ('Para Português, configure lang = pr')
            print ('')
            raw_input('Press enter to exit...\nAperte enter para fechar...\n')
            sys.exit()
    config.read('VoteListener.ini')
    lang = config['LANGUAGE']['lang']
    bindIP = config['VOTE LISTENER']['ip']
    bindPort = int(config['VOTE LISTENER']['port'])
    key = config['VOTE LISTENER']['key']
    dbUser = config['TIBIA DATABASE']['username']
    dbPass = config['TIBIA DATABASE']['password']
    dbIP = config['TIBIA DATABASE']['ip']
    dbPort = int(config['TIBIA DATABASE']['port'])
    dbDatabase = config['TIBIA DATABASE']['database']
    tableName = config['TIBIA DATABASE']['table_prefix'] + "player_votes"

def setupDatabase():
    conn = pymysql.connect(host=dbIP, port=dbPort, user=dbUser, password=dbPass, db=dbDatabase)
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS " + tableName + " (name varchar(255) CHARACTER SET utf8 NOT NULL, votes int(11) NOT NULL)")
    cur.close()
    conn.close()

def startVoteListener():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = (bindIP, bindPort)
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

if __name__ == "__main__":
    loadConfig()
    setupDatabase()
    startVoteListener()