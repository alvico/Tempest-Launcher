import yum


def is_installed(name):
    base = yum.YumBase()
    installed = [x.name for x in base.rpmdb.returnPackages()]
    is_notin = name not in installed
    return is_notin


def main():
    yb = yum.YumBase()
    packages = [
        'python-devel',
        'gcc',
        'libgcc',
        'glibc',
        'libffi-devel',
        'libxml2-devel',
        'libxslt-devel',
        'zlib-devel',
        'bzip2-devel',
        'openssl-devel',
        'mysql-devel',
        'ncurses-devel',
        'sqlite-devel',
        'readline-devel',
        'tk-devel',
        'gdbm-devel',
        'db4-devel',
        'ibpcap-devel',
        'xz-devel',
        'wget']

    searchlist = ['name']
    matching = yb.searchGenerator(searchlist, packages)
    po_list = [po for po, _ in matching
               if po.name in packages and po.arch == 'x86_64']
    for po in po_list:
        if is_installed(po.name):
            import ipdb; ipdb.set_trace()
            print('Processing package {0}'.format(po.name))
            yb.install(po)
            yb.resolveDeps()
            yb.buildTransaction()
            yb.processTransaction()


if __name__ == '__main__':
    main()
