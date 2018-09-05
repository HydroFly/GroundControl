class Rocket:
    def __init__(self):
        self.launched = False

        self.x = 0  # North South distance - accel - ft
        self.y = 0  # East West distance - accel - ft
        self.z = 0 # Height - ultrasound - ft
        self.vz = 1 # dz/dt - ultrasound - ft/sec
        self.vx = 0 # dx/dt - accel - ft/sec
        self.vy = 0 # dy/dt - accel - ft/sec
        self.t = 7  # time elapsed - sec
        
        # Other data will record water output, etc.

    def abort_launch():
        self.launched = False