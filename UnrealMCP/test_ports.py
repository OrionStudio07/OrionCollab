import urllib.request
import json

def test():
    ports = [30010, 30014]
    payload = {"command": "LiveCoding.Compile"}
    
    for port in ports:
        url = f"http://127.0.0.1:{port}/remote/exec"
        req = urllib.request.Request(url, data=json.dumps(payload).encode("utf-8"), headers={"Content-Type": "application/json"}, method="PUT")
        try:
            with urllib.request.urlopen(req, timeout=2.0) as resp:
                print(f"PORT {port} SUCCESS: {resp.read().decode('utf-8')}")
                return
        except Exception as e:
            print(f"PORT {port} FAILED: {e}")

if __name__ == "__main__":
    test()
