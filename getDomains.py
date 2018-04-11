from fetcher import fetchData
import time, sys

if len(sys.argv) != 2:
	print "Solo un argumento, el dominio"
	exit()

print '===================='
print ' Gathering for: {0}'.format(sys.argv[1])
print '===================='
print ''


certificados, entidades = fetchData(sys.argv[1], include_subdomains=True, include_expired=True)
for certificado in certificados:
	fr = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(certificado.valid_from/1000))
	to = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(certificado.valid_to/1000))
	print "- {0}\t| {3}\t| {1}\t| {2}\t".format(certificado.subject, fr, to, certificado.issuer)
