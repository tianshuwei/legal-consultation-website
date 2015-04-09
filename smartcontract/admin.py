from django.contrib import admin
from smartcontract.models import SmartContractCategory, SmartContract, SmartContractInstance

admin.site.register(SmartContractCategory)
admin.site.register(SmartContract)
admin.site.register(SmartContractInstance)
