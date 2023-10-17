import subprocess
import xml.etree.ElementTree as ET
from socket import getservbyport
import datetime


# Command 1: argus command that writes data to stdout
cmd1 = ["sudo", "argus", "-i", "wlo1", "-w", "-", "|"]
# Command 2: ra command that analyzes data and writes as XML to stdout
cmd_string = "ra -s srcid,saddr,sport,daddr,dport,proto,state,dur,sbytes,dbytes,sttl,dttl,service,sload,dload,spkts,dpkts,stcpb,dtcpb,smeansz,dmeansz,trans,sjit,djit,stime,ltime,sintpkt,dintpkt,tcprtt,synack,ackdat -M xml -n"
cmd2 = cmd_string.split()
# Start the first command


# flow_attributes = ['SrcId', 'SrcAddr', 'Sport', 'DstAddr', 'Dport', 'Proto', 'State', 'Dur', 'SrcBytes', 'DstBytes', 'sTtl', 'dTtl', 'SrcLoad', 'DstLoad', 'SrcPkts', 'DstPkts', 'SrcTCPBase', 'DstTCPBase', 'sMeanPktSz', 'dMeanPktSz', 'Trans', 'SrcJitter', 'DstJitter', 'StartTime', 'LastTime', 'SIntPkt', 'DIntPkt', 'TcpRtt', 'SynAck', 'AckDat']

# columns=[
#     'id', 'srcip', 'sport', 'dstip', 'dsport', 'proto', 'state', 'dur', 'sbytes', 'dbytes',
#     'sttl', 'dttl', 'service', 'sload', 'dload', 'Spkts', 'Dpkts', 'stcpb', 'dtcpb', 'smean',
#     'dmean', 'trans_depth', 'sjit', 'djit', 'Stime', 'Ltime', 'sinpkt', 'dinpkt', 'tcprtt',
#     'synack', 'ackdat'
# ]


class LiveCapture:
    queue: list = []
    process: subprocess.Popen = None  # type: ignore

    def start_Capture(self):
        # Start the first command
        argus_capture = subprocess.Popen(cmd1, stdout=subprocess.PIPE, text=True)
        ra_analysis = subprocess.Popen(
            cmd2, stdin=argus_capture.stdout, text=True, stdout=subprocess.PIPE
        )
        print("Started Capture")
        self.process = ra_analysis

    def stop_Capture(self):
        self.process.terminate()
        return True

    def fill_queue(self):
        while True:
            line = self.process.stdout.readline()  # type: ignore
            if not line:
                break
            flow = self.process_output(line)
            if flow:
                if len(self.queue) >= 100:
                    self.queue.pop(0)

                # print(flow)
                self.queue.append(flow)

    def process_flow(self, flow):
        ct_state_ttl = 0
        ct_flw_http_mthd = 0
        ct_srv_src = 0
        ct_srv_dst = 0
        ct_dst_ltm = 0
        ct_src_ltm = 0

        service = 0
        try:
            if "DstPort" in flow.attrib:
                if (
                    flow.attrib["Proto"].lower() == "tcp"
                    or flow.attrib["Proto"].lower() == "udp"
                ):
                    service = getservbyport(
                        int(flow.attrib["DstPort"]), flow.attrib["Proto"].lower()
                    )
        except:
            service = 0

        stime = datetime.datetime.fromisoformat(flow.attrib["StartTime"]).timestamp()
        ltime = datetime.datetime.fromisoformat(flow.attrib["LastTime"]).timestamp()

        for item in self.queue:
            if item["service"] == service:
                if item["srcip"] == flow.attrib["SrcAddr"]:
                    ct_srv_src += 1
                    ct_src_ltm += 1
                if item["dstip"] == flow.attrib["DstAddr"]:
                    ct_srv_dst += 1
                    ct_dst_ltm += 1
            if item["service"] == "http" or item["service"] == "https":
                ct_flw_http_mthd += 1

        flow_dict = {
            "id": flow.attrib["SrcId"] if "SrcId" in flow.attrib else 0,
            "srcip": flow.attrib["SrcAddr"] if "SrcAddr" in flow.attrib else 0,
            "sport": int(flow.attrib["SrcPort"]) if "SrcPort" in flow.attrib else 0,
            "dstip": flow.attrib["DstAddr"] if "DstAddr" in flow.attrib else 0,
            "dsport": int(flow.attrib["DstPort"]) if "DstPort" in flow.attrib else 0,
            "proto": flow.attrib["Proto"] if "Proto" in flow.attrib else 0,
            "state": flow.attrib["State"] if "State" in flow.attrib else 0,
            "dur": flow.attrib["Dur"] if "Dur" in flow.attrib else 0,
            "sbytes": int(flow.attrib["SrcBytes"]) if "SrcBytes" in flow.attrib else 0,
            "dbytes": int(flow.attrib["DstBytes"]) if "DstBytes" in flow.attrib else 0,
            "sttl": flow.attrib["sTtl"] if "sTtl" in flow.attrib else 0,
            "dttl": flow.attrib["dTtl"] if "dTtl" in flow.attrib else 0,
            "service": service,
            "sload": float(flow.attrib["SrcLoad"]) if "SrcLoad" in flow.attrib else 0,
            "dload": float(flow.attrib["DstLoad"]) if "DstLoad" in flow.attrib else 0,
            "Spkts": int(flow.attrib["SrcPkts"]) if "SrcPkts" in flow.attrib else 0,
            "Dpkts": int(flow.attrib["DstPkts"]) if "DstPkts" in flow.attrib else 0,
            "stcpb": flow.attrib["SrcTCPBase"] if "SrcTCPBase" in flow.attrib else 0,
            "dtcpb": flow.attrib["DstTCPBase"] if "DstTCPBase" in flow.attrib else 0,
            "smean": flow.attrib["sMeanPktSz"] if "sMeanPktSz" in flow.attrib else 0,
            "dmean": flow.attrib["dMeanPktSz"] if "dMeanPktSz" in flow.attrib else 0,
            "trans_depth": int(flow.attrib["Trans"]) if "Trans" in flow.attrib else 0,
            "sjit": float(flow.attrib["SrcJitter"])
            if "SrcJitter" in flow.attrib
            else 0,
            "djit": float(flow.attrib["DstJitter"])
            if "DstJitter" in flow.attrib
            else 0,
            "Stime": stime,
            "Ltime": ltime,
            "Sintpkt": flow.attrib["SIntPkt"] if "SIntPkt" in flow.attrib else 0,
            "Dintpkt": flow.attrib["DIntPkt"] if "DIntPkt" in flow.attrib else 0,
            "tcprtt": flow.attrib["TcpRtt"] if "TcpRtt" in flow.attrib else 0,
            "synack": flow.attrib["SynAck"] if "SynAck" in flow.attrib else 0,
            "ackdat": flow.attrib["AckDat"] if "AckDat" in flow.attrib else 0,
            "ct_state_ttl": ct_state_ttl,
            "ct_flw_http_mthd": 0,
            "ct_srv_src": 0,
            "ct_srv_dst": 0,
            "ct_dst_ltm": 0,
            "ct_src_ltm": 0,
        }
        return flow_dict

    def process_output(self, line):
        try:
            # Parse the XML line
            root = ET.fromstring(line.strip())
            if root.tag == "ArgusFlowRecord":
                flow_dict = self.process_flow(root)
                return flow_dict
        except ET.ParseError as e:
            print("Error parsing XML:", e)
