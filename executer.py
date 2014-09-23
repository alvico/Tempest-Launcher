import subprocess
import multiprocessing

def work(rounds=10):

    for x in xrange(rounds):
        proc = subprocess.Popen("nosetests -q test_network_advanced_inter_vmconnectivity test_network_basic_adminstateup test_network_basic_dhcp_disable"
                " test_network_basic_dhcp_lease test_network_basic_inter_vmconnectivity test_network_basic_metadata test_network_basic_multisubnet"
                " test_network_basic_vmconnectivity --logging-level=INFO", shell=True, stdout=subprocess.PIPE)
        for line in proc.stdout.readline():
            print line
            sys.stdout.flush()

if __name__ == '__main__':
    for i in xrange(10):
        p = multiprocessing.Process(target=work())
        p.start()
