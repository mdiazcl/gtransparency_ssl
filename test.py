from fetcher import fetchData
import time

certificados, entidades = fetchData("mdiazlira.com", include_subdomains=True, include_expired=True)
for certificado in certificados:
	fr = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(certificado.valid_from/1000))
	to = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(certificado.valid_to/1000))
	print "- {0}\t| {3}\t| {1}\t| {2}\t".format(certificado.subject, fr, to, certificado.issuer)
