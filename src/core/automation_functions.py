import os
import webbrowser
import psutil
import subprocess
import platform
import shlex
import socket
from typing import Union, List, Dict

class AutomationFunctions:
    """Class encapsulating automation functions."""

    @staticmethod
    def open_chrome():
        """Opens Google Chrome to a default webpage."""
        webbrowser.open("https://www.google.com")

    @staticmethod
    def open_calculator():
        """Opens the system calculator."""
        if platform.system() == "Windows":
            os.system("calc")
        elif platform.system() == "Linux":
            os.system("gnome-calculator")

    @staticmethod
    def open_notepad():
        """Opens Notepad (Windows) or a text editor (Linux)."""
        if platform.system() == "Windows":
            os.system("notepad")
        elif platform.system() == "Linux":
            os.system("gedit")  # Change to preferred editor

    @staticmethod
    def get_cpu_usage():
        """Returns current CPU usage percentage."""
        return psutil.cpu_percent(interval=1)

    @staticmethod
    def get_ram_usage():
        """Returns current RAM usage percentage."""
        return psutil.virtual_memory().percent

    @staticmethod
    def run_shell_command(command: str) -> Union[str, None]:
        """Executes a shell command securely and returns the output."""
        try:
            result = subprocess.run(shlex.split(command), shell=False, capture_output=True, text=True)
            return result.stdout if result.stdout else result.stderr
        except Exception as e:
            return f"Error executing command: {str(e)}"

    @staticmethod
    def list_running_processes() -> List[Dict[str, str]]:
        """Lists currently running processes."""
        processes = []
        for proc in psutil.process_iter(['pid', 'name']):
            try:
                processes.append({"pid": str(proc.info['pid']), "name": proc.info['name']})
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        return processes

    @staticmethod
    def kill_process(process_name_or_pid: Union[str, int]) -> str:
        """Terminates a running process by name or PID."""
        try:
            if isinstance(process_name_or_pid, int):
                p = psutil.Process(process_name_or_pid)
                p.terminate()
                return f"Process {process_name_or_pid} terminated."
            else:
                for proc in psutil.process_iter(['pid', 'name']):
                    if proc.info['name'] == process_name_or_pid:
                        proc.terminate()
                        return f"Process {process_name_or_pid} terminated."
            return "Process not found."
        except Exception as e:
            return f"Error: {str(e)}"

    @staticmethod
    def get_ip_address() -> str:
        """Retrieves the system's IP address."""
        try:
            return socket.gethostbyname(socket.gethostname())
        except Exception as e:
            return f"Error: {str(e)}"

    @staticmethod
    def ping_host(host: str) -> str:
        """Pings a host and returns response time."""
        command = f"ping -c 4 {host}" if platform.system() == "Linux" else f"ping {host}"
        return subprocess.getoutput(command)

    @staticmethod
    def restart_system():
        """Restarts the computer."""
        os.system("shutdown -r now" if platform.system() == "Linux" else "shutdown /r /t 0")
        return "System is restarting..."

    @staticmethod
    def shutdown_system():
        """Shuts down the computer."""
        os.system("shutdown -h now" if platform.system() == "Linux" else "shutdown /s /t 0")
        return "System is shutting down..."

if __name__ == "__main__":
    af = AutomationFunctions()
    af.open_chrome()  # Test one function
