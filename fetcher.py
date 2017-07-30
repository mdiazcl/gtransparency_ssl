import requests, json
from models import Certificate, Issuer

def __getGoogleData__(domain, include_expired=False, include_subdomains=False, next_line=None):
    if next_line is None:
        url = "https://www.google.com/transparencyreport/api/v3/httpsreport/ct/certsearch?include_expired={0}&include_subdomains={1}&domain={2}".format(include_expired, include_subdomains, domain)
    else:
        url = "https://www.google.com/transparencyreport/api/v3/httpsreport/ct/certsearch/page?include_expired={0}&include_subdomains={1}&domain={2}&p={3}".format(include_expired, include_subdomains, domain, next_line)

    data = requests.get(url)
    return data.status_code, data.content


def __dataLineToCertificate__(dataline):
    certificate = Certificate()

    certificate.fingerprint = dataline[0]
    certificate.subject = dataline[1]
    certificate.issuer = dataline[2]
    certificate.valid_from = dataline[3]
    certificate.valid_to = dataline[4]
    certificate.google_id = dataline[5]
    #certificate.ct_logs = dataline[6]
    #ignoreit = dataline[7]  # I dont know what this data representes
    #certificate.dnsnames = dataline[8]

    return certificate

def __dataLineToIssuer__(dataline):
    issuer = Issuer()

    issuer.issuer_uid = dataline[0]
    issuer.google_id = dataline[1]
    issuer.path = dataline[2]
    issuer.certs_issued = dataline[3]

    return issuer

def __parseData__(data):
    # Separate them line by line
    buffer = data
    buffer = buffer[7:]  # Delete some garbage at the beggining
    buffer = buffer[:-1] # delete more garbage at the end

    # Returned Data
    certificate_list = []
    issuer_list = []
    next_line = None

    data = json.loads(buffer)
    json_certs = data[1]
    json_issuers = data[2]
    json_page = data[3]

    for dataline in json_certs:
        cert = __dataLineToCertificate__(dataline)
        certificate_list.append(cert)

    for dataline in json_issuers:
        issuer = __dataLineToIssuer__(dataline)
        issuer_list.append(issuer)

    next_line = json_page[1]

    return certificate_list,issuer_list,next_line

def fetchData(domain, include_expired=False, include_subdomains=False):
    cert_list = []
    issuer_list = []

    # Get data from Google Transparency
    code, data = __getGoogleData__(domain, include_expired=include_expired, include_subdomains=include_subdomains)
    if code == 200:
        certificates, issuers, next_line = __parseData__(data)

        # Append results
        if certificates is not None:
            cert_list += certificates
        if issuers is not None:
            issuer_list += issuers

    else:
        print "TODO: error"

    # There is more data?
    while next_line is not None:
        code, data = __getGoogleData__(domain, include_expired=include_expired, include_subdomains=include_subdomains, next_line=next_line)
        if code == 200:
            certificates, ignore, next_line = __parseData__(data)

            # Append results
            if certificates is not None:
                cert_list += certificates

    # Return results
    return cert_list, issuer_list

