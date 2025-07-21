import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

''' This script is for communication with jetson and computer via udp'''
import config 
import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

JETSON_IP = config.JETSON_IP
JETSON_PORT = config.JETSON_PORT

def send_command_pwm(MOTOR_NUMBER, MOTOR_PWM):
    msg = f"m{MOTOR_NUMBER}_{MOTOR_PWM}"
    sock.sendto(msg.encode(), (JETSON_IP, JETSON_PORT))
    print(f"[CLIENT] Gönderildi: {msg}")
    
