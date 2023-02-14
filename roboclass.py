from PCA9685 import PCA9685
import time
import logging
import paramiko
import threading


class MotorDriver():
    def __init__(self):
        self.Dir = [
            'forward',
            'backward', ]
        self.pwm = PCA9685(0x40, debug=False)
        self.pwm.setPWMFreq(200)
        self.PWMA = 0
        self.AIN1 = 1
        self.AIN2 = 2
        self.PWMB = 5
        self.BIN1 = 3
        self.BIN2 = 4
        # self.thread_KeepAlive = threading.Thread(target=self.KeepAlive, args=())
        # self.thread_KeepAlive.start()

    def MotorRun(self, motor, index, speed):
        #motor setup don't touch
        if speed > 100:
            return
        if (motor == 0):
            self.pwm.setDutycycle(self.PWMA, speed)
            if (index == self.Dir[0]):
                print("1")
                self.pwm.setLevel(self.AIN1, 0)
                self.pwm.setLevel(self.AIN2, 1)
            else:
                print("2")
                self.pwm.setLevel(self.AIN1, 1)
                self.pwm.setLevel(self.AIN2, 0)
        else:
            self.pwm.setDutycycle(self.PWMB, speed)
            if (index == self.Dir[0]):
                print("3")
                self.pwm.setLevel(self.BIN1, 0)
                self.pwm.setLevel(self.BIN2, 1)
            else:
                print("4")
                self.pwm.setLevel(self.BIN1, 1)
                self.pwm.setLevel(self.BIN2, 0)

    def MotorStop(self, motor):
        #stops motor by setting pwm cycle to 0, therefore stopping pings to robot.
        if (motor == 0):
            self.pwm.setDutycycle(self.PWMA, 0)
        else:
            self.pwm.setDutycycle(self.PWMB, 0)

    def MotorForward(self, inchesCount):
        #makes robot go forward at certain speed (like 41.5, 39) for a certain time using a paramter called inches count. Every .18*3 seconds (subject to change)
        #it makes the robot go 3 inches forward
            Motor = MotorDriver()
            Motor.MotorRun(0, 'forward', 39) #left
            Motor.MotorRun(1, 'forward', 39) #right
            time.sleep(inchesCount * (.18 * 3))
            Motor.MotorStop(0)
            Motor.MotorStop(1)

    def MotorReverse(self, inchesCount):
        #makes robot go reverse at certain speed (like 41.5, 39) for a certain time using a paramter called inches count. Every .18*3 seconds (subject to change)
        #it makes the robot go 3 inches reverse
            Motor = MotorDriver()
            Motor.MotorRun(0, 'backward', 39) #left
            Motor.MotorRun(1, 'backward', 39) #right
            time.sleep(inchesCount * (.18 * 3))
            Motor.MotorStop(0)
            Motor.MotorStop(1)

    def MotorLeft(self, turnCount):
        #makes the robot go left by reversing the left wheel at a slower speed than the right and moving the right forward, in order to make it turn in place.
        Motor = MotorDriver()
        Motor.MotorRun(0, 'backward', 39)
        Motor.MotorRun(1, 'forward', 39)
        time.sleep(
            0.69 * turnCount)  ##time needed for the robot to make a 90 degree turn to the left times the amount of times wanted to make the turn (e.g. 0.35 * angleCount)
        Motor.MotorStop(1)
        Motor.MotorStop(0)

    def MotorRight(self, turnCount):
        #makes the robot go right by reversing the right wheel at a slower speed than the left and moving the left forward, in order to make it turn in place.
        Motor = MotorDriver()
        Motor.MotorRun(0, 'forward', 39)
        Motor.MotorRun(1, 'backward', 39)
        time.sleep(
            0.69 * turnCount)  ##time needed for the robot to make a 90 degree turn to the left times the amount of times wanted to make the turn (e.g. 0.35 * angleCount)
        Motor.MotorStop(1)
        Motor.MotorStop(0)
    
    # def KeepAlive():
    #     KeepAliveValue = True
    #     # ssh = paramiko.SSHClient()
    #     # ssh.connect('192.168.1.15', username='teamsalsa', password='salsa')
    #     while KeepAliveValue:
    #         ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command('ls')
    #         print(ssh_stdout + '\n'+ ssh_stderr)
    #         time.sleep(1)
        
