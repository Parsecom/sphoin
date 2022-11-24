
# <img  src="https://a.sphoin.app/logo"  alt="drawing"  width="100"/>

<img  src="https://img.shields.io/pypi/v/sphoin.svg"/><img  src="https://img.shields.io/pypi/pyversions/sphoin.svg"/> 



Connect via [apiv1](https://api.sphoin.app/api/v1) to [sphoin.app](https://www.sphoin.app) Pro Slots.

<img  src="https://a.sphoin.app/clie"  alt="drawing" width="100%" />

# Installation

### Stable release
To install sphoin, run this command in your terminal:

```
pip install sphoin
```

This is the preferred method to install sphoin, as it will always install the most recent stable release.

### From sources

The sources for sphoin can be downloaded from the `Github repo`_.
You can either clone the public repository:
```
git clone https://github.com/Parsecom/sphoin
```
Once you have a copy of the source, you can install it with:
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

<img  src="https://a.sphoin.app/clih"  alt="drawing" width="100%" />
