import requests
from csv import reader
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
    certificate.ct_logs = dataline[6]
    # ignoreit = dataline[7]  # I dont know what this data representes
    certificate.dnsnames = dataline[8]

    return certificate

def __dataLineToIssuer__(dataline):
    issuer = Issuer()

    issuer.issuer_uid = dataline[0]
    issuer.google_id = dataline[2]
    issuer.path = dataline[4]
    issuer.certs_issued = dataline[6]

    return issuer

def __parseData__(data):
    # Separate them line by line
    buffer = data.split('\n')
    buffer = buffer[2:]  # Delete some garbage at the beggining
    buffer = buffer[:-2] # delete more garbage at the end

    if len(buffer) < 3:
        return None, None, None

    # Returned Data
    certificate_list = []
    issuer_list = []
    next_line = None

    # Get data (first half are Certificates, second half are Issuers)
    # The first line requires special treatment, because Google's JSON hates me
    first = False
    certificates_done = False
    issuers_done = False

    for line in buffer:
        if first is False:
            line = line.split('[[')
            line = "\"" + line[2][1:]
            dataline = line[:-1].split(",")
            certificate = __dataLineToCertificate__(dataline)
            certificate_list.append(certificate)

            first = True
        elif certificates_done is False:
            if line == "]":
                certificates_done = True
            else:
                # Process Certificate
                line = line[2:-1]
                dataline = line.split(',')
                certificate = __dataLineToCertificate__(dataline)
                certificate_list.append(certificate)

        elif issuers_done is False:
            if line == "]":
                issuers_done = True
            else:
                # Process Issuers
                if "[[" in line:
                    line = line[3:-1]
                else:
                    line = line[2:-1]

                dataline = [x for x in reader(line)]
                issuer = __dataLineToIssuer__(dataline)
                issuer_list.append(issuer)

        else:
            line = line[2:-1]
            dataline = line.split(',')
            next_line = dataline[1][1:-1]
            if next_line == "ul":
                next_line = None

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

