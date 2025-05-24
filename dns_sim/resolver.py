dns_records = {"webcraft.local": "192.168.1.100"}

def resolve(domain):
    return dns_records.get(domain, "Domain not found.")
