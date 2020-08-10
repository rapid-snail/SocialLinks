from model.profile import Profile
import os.path
import string
import random


f = "data\\profile.py"


def gen_name(prefix, max_len):
    symbols = string.ascii_letters + string.digits + "_"*3
    return prefix + "".join([random.choice(symbols) for _ in range(random.randrange(max_len))])


def test_data_generator(app):
    file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", f)

    countries = app.profile.get_country_name_with_dial_code_list()
    businesses = app.profile.get_business_list()

    with open(file, "w") as out:
        out.write("from model.profile import Profile\n\ntest_data = [\n")
        for i in range(len(countries)):
            if i > 0:
                out.write(",\n")
            bus_idx = random.randrange(len(businesses))
            s = "\tProfile(name=\"%s\", phone=\"49564284\", country=\"%s\", business=\"%s\")" %\
                (gen_name("nam", 77), countries[i]['name'], businesses[bus_idx])
            out.write(s)
        out.write("\n]")
