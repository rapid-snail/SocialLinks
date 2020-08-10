class Profile:

    def __init__(self, name=None, email=None, country=None, phone_code=None, phone=None, business=None):
        self.name = name
        self.email = email
        self.country = country
        self.phone_code = phone_code
        self.phone = phone
        self.business = business

    def __repr__(self):
        s = "{name=%s, email=%s, country=%s, phone_code=%s, phone=%s, business=%s}" % (
            self.name, self.email, self.country, self.phone_code, self.phone, self.business
        )
        return s
