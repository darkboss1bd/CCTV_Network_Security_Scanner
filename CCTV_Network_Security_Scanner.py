#!/usr/bin/env python3
"""
DarkBoss1BD CCTV Network Security Scanner
A professional-grade Python application for ethical security assessment of CCTV devices
"""

import os
import sys
import socket
import threading
import ipaddress
import subprocess
import time
from datetime import datetime
import json

class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'

class CCTVScanner:
    def __init__(self):
        self.scan_results = []
        self.found_devices = []
        self.running = False
        self.banner = f"""
{Colors.CYAN}{Colors.BOLD}
╔════════════════════════════════════════════════════════════════╗
║                                                                ║
║    ██████╗  █████╗ ██████╗ ██╗  ██╗██████╗  ██████╗ ███████╗  ║
║    ██╔══██╗██╔══██╗██╔══██╗██║ ██╔╝██╔══██╗██╔════╝ ██╔════╝  ║
║    ██║  ██║███████║██████╔╝█████╔╝ ██████╔╝██║  ███╗███████╗  ║
║    ██║  ██║██╔══██║██╔══██╗██╔═██╗ ██╔══██╗██║   ██║╚════██║  ║
║    ██████╔╝██║  ██║██║  ██║██║  ██╗██████╔╝╚██████╔╝███████║  ║
║    ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚═════╝  ╚═════╝ ╚══════╝  ║
║                                                                ║
║              CCTV NETWORK SECURITY SCANNER v2.0               ║
║                  Developed by: {Colors.RED}darkboss1bd{Colors.CYAN}                  ║
║                      Secure • Fast • Reliable                 ║
║                                                                ║
╚════════════════════════════════════════════════════════════════╝
{Colors.END}
"""

    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def print_banner(self):
        self.clear_screen()
        print(self.banner)
        print(f"{Colors.YELLOW}{Colors.BOLD}[INFO]{Colors.END} Telegram: {Colors.CYAN}https://t.me/darkvaiadmin{Colors.END}")
        print(f"{Colors.YELLOW}{Colors.BOLD}[INFO]{Colors.END} Channel: {Colors.CYAN}https://t.me/windowspremiumkey{Colors.END}")
        print(f"{Colors.YELLOW}{Colors.BOLD}[INFO]{Colors.END} Website: {Colors.CYAN}https://crackyworld.com/{Colors.END}")
        print(f"{Colors.YELLOW}{Colors.BOLD}[INFO]{Colors.END} Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("-" * 80)

    def get_network_interfaces(self):
        """Get available network interfaces"""
        interfaces = []
        try:
            if os.name == 'nt':  # Windows
                result = subprocess.run(['ipconfig'], capture_output=True, text=True)
                lines = result.stdout.split('\n')
                for line in lines:
                    if 'Ethernet adapter' in line or 'Wireless LAN adapter' in line:
                        interfaces.append(line.split(':')[0].strip())
            else:  # Linux/Mac
                result = subprocess.run(['ifconfig'], capture_output=True, text=True)
                lines = result.stdout.split('\n')
                for line in lines:
                    if 'flags=' in line and 'LO' not in line:
                        interface = line.split(':')[0]
                        if interface and interface not in interfaces:
                            interfaces.append(interface)
        except:
            interfaces = ["eth0", "wlan0", "en0", "en1"]
        
        return interfaces if interfaces else ["eth0", "wlan0"]

    def validate_ip_range(self, ip_range):
        """Validate IP range input"""
        try:
            network = ipaddress.ip_network(ip_range, strict=False)
            return True, network
        except ValueError:
            return False, None

    def port_scan(self, ip, ports=[80, 443, 554, 8000, 8080]):
        """Scan for open ports on target IP"""
        open_ports = []
        for port in ports:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(1)
                result = sock.connect_ex((str(ip), port))
                if result == 0:
                    open_ports.append(port)
                sock.close()
            except:
                pass
        return open_ports

    def detect_cctv_service(self, ip, port):
        """Attempt to detect CCTV service on port"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(2)
            sock.connect((str(ip), port))
            
            if port == 80 or port == 443:
                sock.send(b"GET / HTTP/1.0\r\n\r\n")
                response = sock.recv(1024).decode('utf-8', errors='ignore')
                
                # Check for common CCTV manufacturers
                manufacturers = {
                    'Hikvision': ['Hikvision', 'ISAPI'],
                    'Dahua': ['Dahua', 'DHI-HCVR'],
                    'Axis': ['Axis', 'AXIS'],
                    'Vivotek': ['Vivotek'],
                    'Foscam': ['Foscam'],
                    'Bosch': ['Bosch'],
                    'Samsung': ['Samsung', 'SNS-']
                }
                
                for manufacturer, keywords in manufacturers.items():
                    if any(keyword in response for keyword in keywords):
                        return manufacturer
                        
            return "Unknown CCTV Device"
        except:
            return "Unknown"
        finally:
            sock.close()

    def check_default_credentials(self, ip, port):
        """Simulate default credential check (ethical use only)"""
        # This is a simulation - in real tool, implement proper authentication checks
        common_credentials = [
            ('admin', 'admin'),
            ('admin', '12345'),
            ('admin', 'password'),
            ('admin', ''),
            ('root', 'root')
        ]
        
        # Simulate check (replace with actual HTTP auth attempts in real tool)
        return "Not implemented in demo"

    def scan_ip(self, ip):
        """Scan single IP address"""
        try:
            open_ports = self.port_scan(ip)
            if open_ports:
                device_info = {
                    'ip': str(ip),
                    'open_ports': open_ports,
                    'services': [],
                    'manufacturer': 'Unknown',
                    'status': 'Active'
                }
                
                for port in open_ports:
                    service = self.detect_cctv_service(ip, port)
                    if service != "Unknown":
                        device_info['manufacturer'] = service
                        device_info['services'].append(f"{service} (Port {port})")
                
                if device_info['services']:
                    self.found_devices.append(device_info)
                    print(f"{Colors.GREEN}[FOUND]{Colors.END} {ip} - {device_info['manufacturer']} - Ports: {open_ports}")
                
        except Exception as e:
            pass

    def network_scan(self, network_range):
        """Perform network scan"""
        print(f"\n{Colors.CYAN}[SCANNING]{Colors.END} Starting network scan: {network_range}")
        print(f"{Colors.YELLOW}[INFO]{Colors.END} Scanning for CCTV devices...\n")
        
        try:
            network = ipaddress.ip_network(network_range, strict=False)
            total_ips = network.num_addresses
            scanned = 0
            
            # Use threading for faster scanning
            threads = []
            max_threads = 50
            
            for ip in network.hosts():
                if not self.running:
                    break
                    
                while threading.active_count() > max_threads:
                    time.sleep(0.1)
                
                thread = threading.Thread(target=self.scan_ip, args=(ip,))
                thread.daemon = True
                thread.start()
                threads.append(thread)
                
                scanned += 1
                if scanned % 10 == 0:
                    progress = (scanned / total_ips) * 100
                    print(f"{Colors.BLUE}[PROGRESS]{Colors.END} Scanned {scanned}/{total_ips} IPs ({progress:.1f}%)", end='\r')
            
            # Wait for all threads to complete
            for thread in threads:
                thread.join()
                
        except KeyboardInterrupt:
            print(f"\n{Colors.RED}[INTERRUPT]{Colors.END} Scan interrupted by user")
            self.running = False
        except Exception as e:
            print(f"{Colors.RED}[ERROR]{Colors.END} Scan error: {e}")

    def generate_report(self):
        """Generate scan report"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"cctv_scan_report_{timestamp}.txt"
        
        report = [
            "DARKBOSS1BD CCTV SECURITY SCAN REPORT",
            "=" * 50,
            f"Scan Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"Devices Found: {len(self.found_devices)}",
            "",
            "DETECTED DEVICES:",
            "-" * 30
        ]
        
        for i, device in enumerate(self.found_devices, 1):
            report.extend([
                f"Device {i}:",
                f"  IP Address: {device['ip']}",
                f"  Manufacturer: {device['manufacturer']}",
                f"  Open Ports: {device['open_ports']}",
                f"  Services: {', '.join(device['services'])}",
                f"  Status: {device['status']}",
                ""
            ])
        
        report.extend([
            "SECURITY RECOMMENDATIONS:",
            "-" * 30,
            "1. Change default credentials immediately",
            "2. Update firmware to latest version",
            "3. Restrict network access to necessary ports only",
            "4. Use strong, unique passwords",
            "5. Enable encryption where available",
            "6. Regular security audits recommended",
            "",
            f"Report generated by DarkBoss1BD CCTV Scanner",
            f"Contact: https://t.me/darkvaiadmin"
        ])
        
        try:
            with open(filename, 'w') as f:
                f.write('\n'.join(report))
            print(f"{Colors.GREEN}[REPORT]{Colors.END} Scan report saved: {filename}")
        except Exception as e:
            print(f"{Colors.RED}[ERROR]{Colors.END} Could not save report: {e}")

    def show_results(self):
        """Display scan results"""
        print(f"\n{Colors.CYAN}{Colors.BOLD}SCAN RESULTS{Colors.END}")
        print("=" * 60)
        
        if not self.found_devices:
            print(f"{Colors.RED}[RESULT]{Colors.END} No CCTV devices found on the network")
            return
        
        print(f"{Colors.GREEN}[RESULT]{Colors.END} Found {len(self.found_devices)} potential CCTV devices\n")
        
        for i, device in enumerate(self.found_devices, 1):
            print(f"{Colors.YELLOW}Device #{i}{Colors.END}")
            print(f"  {Colors.WHITE}IP:{Colors.END} {device['ip']}")
            print(f"  {Colors.WHITE}Manufacturer:{Colors.END} {device['manufacturer']}")
            print(f"  {Colors.WHITE}Open Ports:{Colors.END} {device['open_ports']}")
            print(f"  {Colors.WHITE}Services:{Colors.END} {', '.join(device['services'])}")
            print(f"  {Colors.WHITE}Status:{Colors.END} {device['status']}")
            print()

    def main_menu(self):
        """Main menu interface"""
        while True:
            self.print_banner()
            
            print(f"{Colors.CYAN}{Colors.BOLD}MAIN MENU{Colors.END}")
            print(f"{Colors.GREEN}[1]{Colors.END} Start Network Scan")
            print(f"{Colors.GREEN}[2]{Colors.END} View Scan Results")
            print(f"{Colors.GREEN}[3]{Colors.END} Generate Report")
            print(f"{Colors.GREEN}[4]{Colors.END} Network Information")
            print(f"{Colors.RED}[5]{Colors.END} Exit")
            
            choice = input(f"\n{Colors.YELLOW}[CHOICE]{Colors.END} Select option (1-5): ").strip()
            
            if choice == '1':
                self.start_scan()
            elif choice == '2':
                self.show_results()
                input(f"\n{Colors.YELLOW}[PRESS ENTER]{Colors.END} to continue...")
            elif choice == '3':
                if self.found_devices:
                    self.generate_report()
                else:
                    print(f"{Colors.RED}[ERROR]{Colors.END} No scan results available")
                input(f"\n{Colors.YELLOW}[PRESS ENTER]{Colors.END} to continue...")
            elif choice == '4':
                self.show_network_info()
            elif choice == '5':
                print(f"\n{Colors.CYAN}[EXIT]{Colors.END} Thank you for using DarkBoss1BD CCTV Scanner!")
                break
            else:
                print(f"{Colors.RED}[ERROR]{Colors.END} Invalid choice!")

    def show_network_info(self):
        """Show network interface information"""
        self.print_banner()
        print(f"{Colors.CYAN}{Colors.BOLD}NETWORK INFORMATION{Colors.END}")
        print("=" * 60)
        
        interfaces = self.get_network_interfaces()
        print(f"{Colors.YELLOW}[INFO]{Colors.END} Available interfaces: {', '.join(interfaces)}")
        
        try:
            hostname = socket.gethostname()
            local_ip = socket.gethostbyname(hostname)
            print(f"{Colors.YELLOW}[INFO]{Colors.END} Hostname: {hostname}")
            print(f"{Colors.YELLOW}[INFO]{Colors.END} Local IP: {local_ip}")
        except:
            print(f"{Colors.YELLOW}[INFO]{Colors.END} Could not determine local IP")
        
        print(f"\n{Colors.YELLOW}[TIPS]{Colors.END} Common network ranges:")
        print("  - 192.168.0.0/24")
        print("  - 192.168.1.0/24") 
        print("  - 10.0.0.0/24")
        print("  - 172.16.0.0/24")
        
        input(f"\n{Colors.YELLOW}[PRESS ENTER]{Colors.END} to continue...")

    def start_scan(self):
        """Start the network scanning process"""
        self.print_banner()
        
        print(f"{Colors.RED}{Colors.BOLD}WARNING: ETHICAL USE ONLY{Colors.END}")
        print("Only scan networks you own or have explicit permission to test!")
        print("Unauthorized scanning may be illegal in your jurisdiction.\n")
        
        auth = input(f"{Colors.YELLOW}[AUTH]{Colors.END} Do you have authorization to scan? (yes/no): ").strip().lower()
        if auth not in ['yes', 'y']:
            print(f"{Colors.RED}[EXIT]{Colors.END} Authorization required for scanning.")
            time.sleep(2)
            return
        
        print(f"\n{Colors.YELLOW}[INFO]{Colors.END} Available network interfaces:")
        interfaces = self.get_network_interfaces()
        for i, interface in enumerate(interfaces, 1):
            print(f"  {i}. {interface}")
        
        print(f"\n{Colors.CYAN}[INPUT]{Colors.END} Enter network range to scan")
        print(f"{Colors.YELLOW}[EXAMPLE]{Colors.END} 192.168.1.0/24, 10.0.0.0/24")
        
        while True:
            network_range = input(f"\n{Colors.YELLOW}[RANGE]{Colors.END} Network range: ").strip()
            valid, network = self.validate_ip_range(network_range)
            
            if valid:
                break
            else:
                print(f"{Colors.RED}[ERROR]{Colors.END} Invalid network range format")
        
        self.found_devices = []
        self.running = True
        
        # Start scanning
        self.network_scan(network_range)
        self.running = False
        
        print(f"\n{Colors.GREEN}[COMPLETE]{Colors.END} Network scan completed!")
        self.show_results()
        
        if self.found_devices:
            save = input(f"\n{Colors.YELLOW}[SAVE]{Colors.END} Save report? (yes/no): ").strip().lower()
            if save in ['yes', 'y']:
                self.generate_report()
        
        input(f"\n{Colors.YELLOW}[PRESS ENTER]{Colors.END} to continue...")

def main():
    """Main function"""
    try:
        scanner = CCTVScanner()
        scanner.main_menu()
    except KeyboardInterrupt:
        print(f"\n{Colors.RED}[INTERRUPT]{Colors.END} Program terminated by user")
    except Exception as e:
        print(f"{Colors.RED}[ERROR]{Colors.END} Fatal error: {e}")

if __name__ == "__main__":
    main()
