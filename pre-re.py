import yum

from conf import config


def is_installed(name):
    base = yum.YumBase()
    installed = [x.name for x in base.rpmdb.returnPackages()]
    is_notin = name not in installed
    return is_notin


def main():
    yb = yum.YumBase()
    packages = config['packages']
    searchlist = ['name']
    matching = yb.searchGenerator(searchlist, packages)
    po_list = [po for po, _ in matching
               if po.name in packages and po.arch == 'x86_64']
    for po in po_list:
        if is_installed(po.name):
            print('Processing package {0}'.format(po.name))
            try:
                yb.install(po)
                yb.resolveDeps()
                yb.buildTransaction()
                yb.processTransaction()
            except Exception as e:
                if 'is already installed' in str(e):
                    pass


if __name__ == '__main__':
    main()
