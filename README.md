# gtransparency_ssl
Bunch of modules to work with Google Transparency Report
Well it's not a bunch, it's just one, but anyway....

## Usage
### How to use?
Import the module fetchData from fetcher file. That's it!

### API
fetchData - Fetch certificate data from Google Transparency Project
#### Usage
```python
(certificate_list, issuer_list) fetchData(string domain, include_subdomains=False, include_expired=False)
```
#### Params
* **domain:** Name of the domain that you want to get info from. *(ej: example.org)*
* `(opt)` **include_subdomains:** Include subdomains from domain name (might take a while)
* `(opt)` **include_expired:** Include expired domains (might take a while)


### Example
```python
from fetcher import fetchData
import time

certificados, entidades = fetchData("mdiazlira.com", include_subdomains=True, include_expired=True)
for certificado in certificados:
	fr = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(certificado.valid_from/1000))
	to = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(certificado.valid_to/1000))
	print "- {0}\t| {3}\t| {1}\t| {2}\t".format(certificado.subject, fr, to, certificado.issuer)
```