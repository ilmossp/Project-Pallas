from scapy.all import sniff
from scapy.layers.inet import TCP, UDP
import pandas as pd

columns = [
    "srcip", "sport", "dstip", "dsport", "proto", "state", "dur", "sbytes",
    "dbytes", "sttl", "dttl", "sloss", "dloss", "service", "Sload", "Dload",
    "Spkts", "Dpkts", "swin", "dwin", "stcpb", "dtcpb", "smeansz", "dmeansz",
    "trans_depth", "res_bdy_len", "Sjit", "Djit", "Stime", "Ltime", "Sintpkt",
    "Dintpkt", "tcprtt", "synack", "ackdat", "is_sm_ips_ports", "ct_state_ttl",
    "ct_flw_http_mthd", "is_ftp_login", "ct_ftp_cmd", "ct_srv_src", "ct_srv_dst",
    "ct_dst_ltm", "ct_src_ltm", "ct_src_dport_ltm", "ct_dst_sport_ltm",
    "ct_dst_src_ltm"
]

packet_batch = pd.DataFrame(columns=columns) # type: ignore


def packet_handler(packet):
    global packet_batch
    features = {
        "srcip": packet["IP"].src,
        "sport": packet["TCP"].sport if TCP in packet else packet["UDP"].sport if UDP in packet else 0,
        "dstip": packet["IP"].dst,
        "dsport": packet["TCP"].dport if TCP in packet else packet["UDP"].dport if UDP in packet else 0,
        "proto": packet["IP"].proto,
        "state": "unprocessed",
        "dur": "unprocessed",
        "sbytes": packet["IP"].len,
        "dbytes": "unprocessed",
        "sttl": "unprocessed",
        "dttl": "unprocessed",
        "sloss": "unprocessed",
        "dloss": "unprocessed",
        "service": "unprocessed",
        "Sload": "unprocessed",
        "Dload": "unprocessed",
        "Spkts": "unprocessed",
        "Dpkts": "unprocessed",
        "swin": packet["TCP"].window if TCP in packet else 0,
        "dwin": packet["TCP"].window if TCP in packet else 0,
        "stcpb": "unprocessed",
        "dtcpb": "unprocessed",
        "smeansz": "unprocessed",
        "dmeansz": "unprocessed",
        "trans_depth": "unprocessed",
        "res_bdy_len": "unprocessed",
        "Sjit": "unprocessed",
        "Djit": "unprocessed",
        "Stime": "unprocessed",
        "Ltime": "unprocessed",
        "Sintpkt": "unprocessed",
        "Dintpkt": "unprocessed",
        "tcprtt": "unprocessed",
        "synack": "unprocessed",
        "ackdat": "unprocessed",
        "is_sm_ips_ports": "unprocessed",
        "ct_state_ttl": "unprocessed",
        "ct_flw_http_mthd": "unprocessed",
        "is_ftp_login": "unprocessed",
        "ct_ftp_cmd": "unprocessed",
        "ct_srv_src": "unprocessed",
        "ct_srv_dst": "unprocessed",
        "ct_dst_ltm": "unprocessed",
        "ct_src_ltm": "unprocessed",
        "ct_src_dport_ltm": "unprocessed",
        "ct_dst_sport_ltm": "unprocessed",
        "ct_dst_src_ltm": "unprocessed"
    }
    packet_batch = packet_batch._append(features,ignore_index=True) #type: ignore

    if len(packet_batch) == 100:
        print(packet_batch)

sniff(filter="ip", prn=packet_handler, count=100)
