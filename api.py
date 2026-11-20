from flask import Flask, render_template, request
from netmiko import ConnectHandler

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    results = {}
    error = None
    router_device = {
        'device_type': 'cisco_ios_telnet',
        'ip' : '192.168.10.28',
        'port': 32770,
        'username': 'admin',
        'password': 'eve123',
        'secret': 'eve123',
    }

    if request.method == "POST":
        commands_to_run = [
            "show version",
            "show ip interface brief",
            "show running-config"
        ]
        net_connect = None

        try:
            net_connect = ConnectHandler(**router_device)
            net_connect.enable()

            for command in commands_to_run:
                results[command] = net_connect.send_command(command)

        except Exception as e:
            error = f"Router operation failed: {e}"
        finally:
            if net_connect is not None:
                try:
                    net_connect.disconnect()
                except Exception as e:
                    disconnect_error = f"Disconnect failed: {e}"
                    error = f"{error}; {disconnect_error}" if error else disconnect_error

    return render_template(
        "index.html",
        results=results,
        error=error,
        device=router_device,
    )

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)