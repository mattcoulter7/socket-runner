def parse_ports(port_str):
    ports = []
    for port_range in port_str.split(','):
        if '-' in port_range:
            start, end = map(int, port_range.split('-'))
            ports.extend(range(start, end+1))
        else:
            ports.append(int(port_range))
    return ports
