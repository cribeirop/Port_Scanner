import optparse
from socket import *
from threading import *

screenLock = Semaphore(value=1)

well_known_ports = {
    21: "FTP",
    22: "SSH",
    23: "Telnet",
    25: "SMTP",
    53: "DNS",
    80: "HTTP",
    88: "Kerberos",
    110: "POP",
    113: "AUTH",
    123: "NTP",
    143: "IMAP",
    389: "LDAP",
    443: "HTTPS"
}

def connScan(tgtHost, tgtPort):
    service = None
    try:
        connSkt = socket(AF_INET, SOCK_STREAM)
        service = well_known_ports.get(tgtPort, "unknown")
        connSkt.connect((tgtHost, tgtPort))
        print('[+] %-10s %-9s open' % (service,str(tgtPort)+'/tcp'))
        screenLock.acquire()
    except:
        if service != "unknown":
            print('[-] %-10s %-9s closed' % (service, str(tgtPort)+'/tcp'))
        screenLock.acquire()
    finally:
        screenLock.release()
        connSkt.close()

def portScan(tgtHost, startPort, endPort):
    try:
        tgtIP = gethostbyname(tgtHost)
    except:
        print("[-] Cannot resolve '%s': Unknown host"%tgtHost)
        return
    try:
        tgtName = gethostbyaddr(tgtIP)
        print('\n[+] Scan Results for: ' + tgtName[0])
    except:
        print('\n[+] Scan Results for: ' + tgtIP)
    setdefaulttimeout(1.25)
    for tgtPort in range(int(startPort), int(endPort) + 1):
        t = Thread(target=connScan, args=(tgtHost, tgtPort))
        t.start()

def main():
    parser = optparse.OptionParser('usage %prog -H <host alvo> -p <porta_inicio>-<porta_final>')
    parser.add_option('-H', dest='tgtHost', type='string', help='Especificar o host')
    parser.add_option('-p', dest='tgtPort', type='string', help="Especificar, sem espaçamento, o range de portas, separado por '-'")

    (options, args) = parser.parse_args()

    tgtHost = options.tgtHost
    tgtPorts = options.tgtPort
    tgtPorts = tgtPorts.split('-')

    if (tgtHost == None) | (tgtPorts[0] == None):
        print(parser.usage)
        exit(0)
    portScan(tgtHost, tgtPorts[0], tgtPorts[1])

if __name__ == '__main__':
    main()