import whois

try:
    domain = whois.whois("google.com")

    print("Registrar:", domain.registrar)
    print("Creation:", domain.creation_date)
    print("Expiration:", domain.expiration_date)

except Exception as e:
    print("ERROR:")
    print(e)