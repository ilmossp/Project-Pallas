from xml.etree import ElementTree as ET

xml = '<ArgusFlowRecord  StartTime = "2023-08-25T00:00:25.212310" Flags = "e" Proto = "tcp" SrcAddr = "192.168.1.106" SrcPort = "35366" Dir" DstAddr = "66.102.1.188" DstPort = "hpvroom" Pkts = "2" Bytes = "132" State = "CON"></ArgusFlowRecord>'

root = ET.fromstring("f'<root>{xml}</root>'")
print(root.attrib["StartTime"])