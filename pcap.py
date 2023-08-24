import pandas as pd
import pyshark
columns = ['id',
           'srcip',
           'sport',
           'dstip',
           'dsport',
           'proto',
           'state',
           'dur',
           'sbytes',
           'dbytes',
           'sttl',
           'dttl',
           'service',
           'sload',
           'dload',
           'Spkts',
           'Dpkts',
           'stcpb',
           'dtcpb',
           'smean',
           'dmean',
           'trans_depth',
           'sjit',
           'djit',
           'Stime',
           'Ltime',
           'sinpkt',
           'dinpkt',
           'tcprtt',
           'synack',
           'ackdat',
           'ct_state_ttl',
           'ct_flw_http_mthd',
           'ct_srv_src',
           'ct_srv_dst',
           'ct_dst_ltm',
           'ct_src_ltm']
packet_batch = pd.DataFrame(columns=columns)  # type: ignore


def packet_handler(packet):
    # Extract packet features
    global packet_batch
    features = {
        "id": 0,
        "srcip": packet.ip.src,
        "sport": packet["TCP"].srcport if "TCP" in packet else packet["UDP"].srcport if "UDP" in packet else 0,
        "dstip": packet.ip.dst,
        "dsport": packet["TCP"].dstport if "TCP" in packet else packet["UDP"].dstport if "UDP" in packet else 0,
        "proto": packet.layers[1].layer_name,
        "state": determine_state(packet["TCP"].flags) if "TCP" in packet else 0,
        "dur": float(packet.frame_info.time_epoch),
        "sbytes": packet.length,
        "dbytes": 0,
        "sttl": packet.ip.ttl if "IP" in packet else 0,
        "dttl": 0,
        "sloss": 0,
        "dloss": 0,
        "service": 0,
        "Sload": 0,
        "Dload": 0,
        "Spkts": 0,
        "Dpkts": 0,
        "swin": 0,
        "dwin": 0,
        "stcpb": 0,
        "dtcpb": 0,
        "smeansz": 0,
        "dmeansz": 0,
        "trans_depth": 0,
        "res_bdy_len": 0,
        "Sjit": 0,
        "Djit": 0,
        "Stime": 0,
        "Ltime": 0,
        "Sintpkt": 0,
        "Dintpkt": 0,
        "tcprtt": 0,
        "synack": 0,
        "ackdat": 0,
        "is_sm_ips_ports": 0,
        "ct_state_ttl": 0,
        "ct_flw_http_mthd": 0,
        "ct_ftp_cmd": 0,
        "ct_srv_src": 0,
        "ct_srv_dst": 0,
        "ct_dst_ltm": 0,
        "ct_src_ltm": 0,
    }
    packet_batch = packet_batch._append(
        features, ignore_index=True)  # type: ignore

    if len(packet_batch) == 100:
        print(packet_batch["dur"])
        df = process_batch(packet_batch)
        print(df["dur"])


def process_batch(batch):
    processd_batch = batch
    for index, row in batch.iterrows():
        if row["Stime"] == 0:
            row["Stime"] = calculate_duration(row)
            process_batch.at[index, "dur"] = row["dur"]
    return processd_batch


def calculate_duration(packet):
    # Calculate duration based on packet timestamps
    if "Stime" in packet and "Ltime" in packet:
        print(packet["Stime"])
        return 0

    return None


def determine_state(flags):
    return 0


capture = pyshark.LiveCapture()
capture.sniff(packet_count=100)
for packet in capture.sniff_continuously(packet_count=100):
    packet_handler(packet)
