import subprocess
import xml.etree.ElementTree as ET
from socket import getservbyport
# Command 1: argus command that writes data to stdout
cmd1 = ["sudo","argus", "-i", "wlo1", "-w", "-","|"]
# Command 2: ra command that analyzes data and writes as XML to stdout
cmd_string = "ra -s srcid,saddr,sport,daddr,dport,proto,state,dur,sbytes,dbytes,sttl,dttl,service,sload,dload,spkts,dpkts,stcpb,dtcpb,smeansz,dmeansz,trans,sjit,djit,stime,ltime,sintpkt,dintpkt,tcprtt,synack,ackdat -M xml -n"
cmd2 = cmd_string.split()
# Start the first command




def process_init():
    argus_capture = subprocess.Popen(cmd1, stdout=subprocess.PIPE, text=True)
    ra_analysis = subprocess.Popen(cmd2,stdin=argus_capture.stdout,text=True,stdout=subprocess.PIPE)
    return  ra_analysis 



def process_output(stdout):
    for line in stdout: 
        try:
            # Parse the XML line
            root = ET.fromstring(line.strip())
            if(root.tag == "ArgusFlowRecord"):
                print(root.attrib)
                flow_dict = process_flow(root)
                print(flow_dict)
                return flow_dict
            else:
                continue
        except ET.ParseError as e:
            print("Error parsing XML:", e)     





def process_terminate(process):
    process.terminate()
    return True








def process_flow(flow):
    
    service = 0
    try:
        if 'DstPort' in flow.attrib and flow.attrib['Proto']=='tcp' or flow.attrib['Proto']=='udp':
            service = getservbyport(int(flow.attrib['DstPort'],flow.attrib['Proto']))
    except:
        print("Error getting service")
    
    
    flow_dict = {
        'id': flow.attrib['SrcId'] if 'SrcId' in flow.attrib else 0,
        'srcip': flow.attrib['SrcAddr'] if 'SrcAddr' in flow.attrib else 0,
        'sport': flow.attrib['SrcPort'] if 'SrcPort' in flow.attrib else 0,
        'dstip': flow.attrib['DstAddr'] if 'DstAddr' in flow.attrib else 0,
        'dsport': flow.attrib['DstPort'] if 'DstPort' in flow.attrib else 0,
        'proto': flow.attrib['Proto'] if 'Proto' in flow.attrib else 0,
        'state': flow.attrib['State'] if 'State' in flow.attrib else 0,
        'dur': flow.attrib['Dur'] if 'Dur' in flow.attrib else 0,
        'sbytes': flow.attrib['SrcBytes'] if 'SrcBytes' in flow.attrib else 0,
        'dbytes': flow.attrib['DstBytes'] if 'DstBytes' in flow.attrib else 0,
        'sttl': flow.attrib['sTtl'] if 'sTtl' in flow.attrib else 0,
        'dttl': flow.attrib['dTtl'] if 'dTtl' in flow.attrib else 0,
        'service': service,
        'sload': flow.attrib['SrcLoad'] if 'SrcLoad' in flow.attrib else 0,
        'dload': flow.attrib['DstLoad'] if 'DstLoad' in flow.attrib else 0,
        'Spkts': flow.attrib['SrcPkts'] if 'SrcPkts' in flow.attrib else 0,
        'Dpkts': flow.attrib['DstPkts'] if 'DstPkts' in flow.attrib else 0,
        'stcpb': flow.attrib['SrcTCPBase'] if 'SrcTCPBase' in flow.attrib else 0,
        'dtcpb': flow.attrib['DstTCPBase'] if 'DstTCPBase' in flow.attrib else 0,
        'smean': flow.attrib['sMeanPktSz'] if 'sMeanPktSz' in flow.attrib else 0,
        'dmean': flow.attrib['dMeanPktSz'] if 'dMeanPktSz' in flow.attrib else 0,
        'trans_depth': flow.attrib['Trans'] if 'Trans' in flow.attrib else 0,
        'sjit': flow.attrib['SrcJitter'] if 'SrcJitter' in flow.attrib else 0,
        'djit': flow.attrib['DstJitter'] if 'DstJitter' in flow.attrib else 0,
        'Stime': flow.attrib['StartTime'] if 'StartTime' in flow.attrib else 0,
        'Ltime': flow.attrib['LastTime'] if 'LastTime' in flow.attrib else 0,
        'sinpkt': flow.attrib['SIntPkt'] if 'SIntPkt' in flow.attrib else 0,
        'dinpkt': flow.attrib['DIntPkt'] if 'DIntPkt' in flow.attrib else 0,
        'tcprtt': flow.attrib['TcpRtt'] if 'TcpRtt' in flow.attrib else 0,
        'synack': flow.attrib['SynAck'] if 'SynAck' in flow.attrib else 0,
        'ackdat': flow.attrib['AckDat'] if 'AckDat' in flow.attrib else 0,
        'ct_state_ttl': flow.attrib['ct_state_ttl'] if 'ct_state_ttl' in flow.attrib else 0,
        'ct_flw_http_mthd': flow.attrib['ct_flw_http_mthd'] if 'ct_flw_http_mthd' in flow.attrib else 0,
        'ct_srv_src': 0,
        'ct_srv_dst': 0,
        'ct_dst_ltm': 0,
        'ct_src_ltm': 0
    }
    return flow_dict




# Wait for the processes to finish


flow_attributes = ['SrcId', 'SrcAddr', 'Sport', 'DstAddr', 'Dport', 'Proto', 'State', 'Dur', 'SrcBytes', 'DstBytes', 'sTtl', 'dTtl', 'SrcLoad', 'DstLoad', 'SrcPkts', 'DstPkts', 'SrcTCPBase', 'DstTCPBase', 'sMeanPktSz', 'dMeanPktSz', 'Trans', 'SrcJitter', 'DstJitter', 'StartTime', 'LastTime', 'SIntPkt', 'DIntPkt', 'TcpRtt', 'SynAck', 'AckDat']

columns=[
    'id', 'srcip', 'sport', 'dstip', 'dsport', 'proto', 'state', 'dur', 'sbytes', 'dbytes',
    'sttl', 'dttl', 'service', 'sload', 'dload', 'Spkts', 'Dpkts', 'stcpb', 'dtcpb', 'smean',
    'dmean', 'trans_depth', 'sjit', 'djit', 'Stime', 'Ltime', 'sinpkt', 'dinpkt', 'tcprtt',
    'synack', 'ackdat'
]