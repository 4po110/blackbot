
def readEmails():
    with open('database/emails.txt', 'r') as f:
        data = f.read()
    data = data.split('\n')
    emails = list()
    passwords = list()

    for line in data:
        emails.append(line.split(',')[0])
        passwords.append(line.split(',')[1])
    
    return emails, passwords

def readProxies():
    with open('database/proxies.txt', 'r') as f:
        data = f.read()
    data = data.split('\n')
    proxies = list()

    for line in data:
        [ip, port, user, pwd] = line.split(':')
        proxies.append(f'{user}:{pwd}@{ip}:{port}')

    return proxies