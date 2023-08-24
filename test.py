from scapy.all import sniff

sniff( prn=lambda x : print(x["Stime"]) if "Stime" in x  else print("no"),count= 100)