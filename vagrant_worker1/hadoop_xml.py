import os
from jinja2 import Environment, FileSystemLoader

env = Environment(loader=FileSystemLoader('/'))
path = '/home/vagrant/hadoop-2.7.3/etc/hadoop/'
files = os.listdir(path)
for fil in files:

    template = env.get_template(path + fil)

    data = {
        "ADDRESS": '192.168.1.23',
    }
    conf = template.render(**data)

    open(path + fil, "w").write(conf)
    print fil
