import json
from pathlib import Path

def generate_default_metadata(output_path: str = "data/function_metadata.json") -> None:
    """Generate and save default function metadata for RAG-based function execution."""
    default_functions = [
        # Application Control
        {
            "name": "open_chrome",
            "description": "Opens Google Chrome to a default webpage.",
            "module": "automation_functions",
            "class": "AutomationFunctions",
            "params": [],
            "category": "Application Control",
            "platform": ["Windows", "Linux"]
        },
        {
            "name": "open_calculator",
            "description": "Opens the system calculator application.",
            "module": "automation_functions",
            "class": "AutomationFunctions",
            "params": [],
            "category": "Application Control",
            "platform": ["Windows", "Linux"]
        },
        # System Monitoring
        {
            "name": "get_cpu_usage",
            "description": "Returns the current CPU usage as a percentage.",
            "module": "system_monitor",
            "class": "SystemMonitor",
            "params": [],
            "category": "System Monitoring",
            "platform": ["Windows", "Linux"]
        },
        {
            "name": "get_ram_usage",
            "description": "Returns the current RAM usage as a percentage.",
            "module": "system_monitor",
            "class": "SystemMonitor",
            "params": [],
            "category": "System Monitoring",
            "platform": ["Windows", "Linux"]
        },
        # Command Execution
        {
            "name": "run_shell_command",
            "description": "Executes a shell command and returns its output.",
            "module": "command_executor",
            "class": "CommandExecutor",
            "params": ["command"],
            "category": "Command Execution",
            "platform": ["Windows", "Linux"]
        },
        # File Management
        {
            "name": "create_text_file",
            "description": "Creates a new text file with given content.",
            "module": "file_operations",
            "class": "FileOperations",
            "params": ["file_name", "content"],
            "category": "File Management",
            "platform": ["Windows", "Linux"]
        },
        {
            "name": "delete_file",
            "description": "Deletes a specified file.",
            "module": "file_operations",
            "class": "FileOperations",
            "params": ["file_name"],
            "category": "File Management",
            "platform": ["Windows", "Linux"]
        },
        {
            "name": "list_files_in_directory",
            "description": "Lists all files in a specified directory.",
            "module": "file_operations",
            "class": "FileOperations",
            "params": ["directory"],
            "category": "File Management",
            "platform": ["Windows", "Linux"]
        },
        # Process Management
        {
            "name": "kill_process",
            "description": "Terminates a running process by name or PID.",
            "module": "process_manager",
            "class": "ProcessManager",
            "params": ["process_name_or_pid"],
            "category": "Process Management",
            "platform": ["Windows", "Linux"]
        },
        {
            "name": "list_running_processes",
            "description": "Lists currently running processes.",
            "module": "process_manager",
            "class": "ProcessManager",
            "params": [],
            "category": "Process Management",
            "platform": ["Windows", "Linux"]
        },
        # Network Utilities
        {
            "name": "get_ip_address",
            "description": "Retrieves the system's IP address.",
            "module": "network_utils",
            "class": "NetworkUtils",
            "params": [],
            "category": "Network Utilities",
            "platform": ["Windows", "Linux"]
        },
        {
            "name": "ping_host",
            "description": "Pings a host and returns response time.",
            "module": "network_utils",
            "class": "NetworkUtils",
            "params": ["host"],
            "category": "Network Utilities",
            "platform": ["Windows", "Linux"]
        },
        # System Actions
        {
            "name": "restart_system",
            "description": "Restarts the computer.",
            "module": "system_actions",
            "class": "SystemActions",
            "params": [],
            "category": "System Actions",
            "platform": ["Windows", "Linux"]
        },
        {
            "name": "shutdown_system",
            "description": "Shuts down the computer.",
            "module": "system_actions",
            "class": "SystemActions",
            "params": [],
            "category": "System Actions",
            "platform": ["Windows", "Linux"]
        }
    ]
    
    # Ensure the data directory exists
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    
    # Write to JSON file
    with open(output_path, 'w') as f:
        json.dump(default_functions, f, indent=4)
    
    print(f"Default metadata generated at {output_path}")

if __name__ == "__main__":
    generate_default_metadata()
