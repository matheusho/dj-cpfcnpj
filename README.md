# BR CPFCNPJ Field
 A custom Django form field to BR CPF/CNPJ form field


### Example
 
```python
from django import forms
from br_cpfcnpj.forms import BRCPFCNPJField


class PersonForm(forms.Form):
    name = forms.CharField(label="Name", max_length=100)
    cpf_cnpj = forms.BRCPFCNPJField(label="CPF / CNPJ")
```
 
 
 Thanks.

Love and peace.
