from fetcher import fetchData

certificados, entidades = fetchData("e-sign.cl", include_subdomains=True, include_expired=True)
for certificado in certificados:
    print "{0} \t\t\t|{1}\t\t|{2}".format(certificado.subject, certificado.valid_from, certificado.valid_to)
