

# <img  src="https://api.sphoin.app/logo"  alt="drawing"  width="100"/>

<img  src="https://img.shields.io/pypi/v/sphoin.svg"/><img  src="https://img.shields.io/pypi/pyversions/sphoin.svg"/> 



Connect to [sphoin.app](https://www.sphoin.app) Pro Slots.

<img  src="https://firebasestorage.googleapis.com/v0/b/sphoin-545ba.appspot.com/o/cli.png?alt=media&token=e3c578f1-1cb5-4907-b57c-4037bba45c26"  alt="drawing" width="100%" />

# Installation

### Stable release
To install sphoin, run this command in your terminal:

```
pip install sphoin
```

This is the preferred method to install sphoin, as it will always install the most recent stable release.

### From sources

The sources for sphoin can be downloaded from the `Github repo`.
* clone the public repository
```
git clone https://github.com/Parsecom/sphoin
```
* install from source
```
python setup.py install
```
# Usage
### example.json configuration file template
```yaml
---
uid: 111YOURUID111
api-key: 111YOURAPIKEY111
api-secret: 111YOURSECRET111
show:
  - line
  - signals
  - studies
```

### To use sphoin CLI:
```
sphoin --help
```
View example
```
sphoin --example
```

### To use sphoin in a python project:

Import package:
```python
from sphoin.app import Slot
```
Init Slot with token and secret:
```python
my_slot = Slot(uid="111YOURUID111",api_key="111YOURAPIKEY111",api_secret="111YOURSECRET111")
print(my_slot.json())
```