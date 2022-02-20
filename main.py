import requests
import json


def generatewireguardconf(adress: str, privkey: str, dns: str, pubkey: str, allowdip: str, endpoint: str, output: str):
    file = "[Interface] \n" \
           "Address = %s \n" \
           "PrivateKey = %s \n" \
           "DNS = %s \n" \
           "[Peer] \n" \
           "PublicKey = %s \n" \
           "AllowedIPs = %s \n" \
           "Endpoint = %s"
    file = file % (adress, privkey, dns, pubkey, allowdip, endpoint)
    f = open(output + endpoint.split(".")[0] + "nordvpnwireguard.conf", "a")
    f.write(file)
    f.close()


def checktechnology(technologies):
    for t in technologies:
        if t["identifier"] == "wireguard_udp":
            return t["metadata"][0]["value"]

    return False


def downloadnord(url: str, privkey: str, allowdip: str, addr: str, outputdir: str):
    myfile = requests.get(url)
    jsonstring = myfile.content.decode("utf-8")
    data = json.loads(jsonstring)
    for datapoint in data:
        wg = checktechnology(datapoint["technologies"])
        if not wg:
            continue
        generatewireguardconf(addr, privkey, datapoint["station"],
                              wg, allowdip, datapoint["hostname"]+":51820", outputdir)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    f = open('config.json')
    data = json.load(f)
    downloadnord(data["url"]+data["limit"],
                 data["privatekey"], data["allowedip"], data["adress"], data["outputdir"])

