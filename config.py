'''
centralized configuration
'''

import configparser

config = {
    'db_url' : 'mysql+mysqlconnector://ths:ths@127.0.0.1:3306/quant'
}

_config = None

def get_config() :
    global _config
    if _config is None :
        _config = configparser.ConfigParser()
        _config.read("config.ini")
        pass

    return _config


def get_login(index) :
    conf = get_config()
    users = conf['login']['users'].split()
    passwords = conf['login']['passwords'].split()
    return (users[index], passwords[index])

if __name__ == "__main__" :
    conf = get_config()
    print("config : %r"%conf)
    for s in conf.sections() :
        print("section %s : %r"%(s,conf[s]))
        for i in conf[s] :
            print("  item %r : %s"%(i, conf[s][i]))

    for i in range(4) :
        (user, password) = get_login(i)
        print("login %d , user %s, password %s"%(i, user, password))
    pass
