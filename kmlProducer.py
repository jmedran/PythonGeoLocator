import dpkt
import socket
import pygeoip

gi = pygeoip.GeoIP('GeoLiteCity.dat')


def retKML(ip):
    rec = gi.record_by_name(ip)
    try:
        longitude = rec['longitude']
        latitude = rec['latitude']
        kml = (
               '<Placemark>\n'
               '<name>%s</name>\n'
               '<Point>\n'
               '<coordinates>%6f,%6f</coordinates>\n'
               '</Point>\n'
               '</Placemark>\n'
               ) %(ip,longitude, latitude)
        return kml
    except:
        return ''


def plotIPs(pcap):
    kmlPts = ''
    for (ts, buf) in pcap:
        try:

            eth = dpkt.ethernet.Ethernet(buf)

            ip = eth.data

            src = socket.inet_ntoa(ip.src)

            srcKML = retKML(src)

            dst = socket.inet_ntoa(ip.dst)

            dstKML = retKML(dst)
            
            kmlPts = kmlPts + srcKML + dstKML
        except:
            pass
    return kmlPts

f = open('geotest.pcap')
pcap = dpkt.pcap.Reader(f)

kmlheader = '<?xml version="1.0" encoding="UTF-8"?>\
\n<kml xmlns="http://www.opengis.net/kml/2.2">\n<Document>\n'
kmlfooter = '</Document>\n</kml>\n'
kmldoc=kmlheader+plotIPs(pcap)+kmlfooter
f.close()
f = open('geotest.kml','w')
f.write(kmldoc)
f.close()