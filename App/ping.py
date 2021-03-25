from tabulate import tabulate
import subprocess


def host_ping(addr):
    return (
            subprocess.call(["ping", "-n", "1", str(addr)],
                            stdout=subprocess.DEVNULL,
                            stderr=subprocess.DEVNULL
                            ) == 0
    )


def host_range_ping(addrs):
    result = {}
    for addr in addrs:
        result[addr] = host_ping(addr)

    return result


def print_host_table(result):
    col = ['HOST', 'STATUS']
    data = [
        (host, "Reachable" if b else "Unreachable") for host, b in result.items()
    ]
    return tabulate(data, headers=col, tablefmt="grid")


if __name__ == '__main__':
    res = host_range_ping(["google.com", "mail.ru", "fooo"])
    print(print_host_table(res))
