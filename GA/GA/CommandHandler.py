import ctypes, time
class Flags_bits_motor( ctypes.LittleEndianStructure ):
    _fields_ = [
                ("speed", ctypes.c_uint8, 7 ),  # asByte & 2-8
                ("direction",     ctypes.c_uint8, 1 ),  # asByte & 1
               ]
class Flags_motor( ctypes.Union ):
    _fields_ = [
                ("b",      Flags_bits_motor ),
                ("asByte", ctypes.c_uint8    )
               ]
    _anonymous_ = ("b")
class Flags_bits_steering( ctypes.LittleEndianStructure ):
    _fields_ = [
                ("position", ctypes.c_uint8, 7 ),  # asByte & 2-8
                ("direction",     ctypes.c_uint8, 1 ),  # asByte & 1
               ]
class Flags_steering( ctypes.Union ):
    _fields_ = [
                ("b",      Flags_bits_steering ),
                ("asByte", ctypes.c_uint8    )
               ]
    _anonymous_ = ("b")
class Flags_bits_misc( ctypes.LittleEndianStructure ):
    _fields_ = [
                ("misc", ctypes.c_uint8, 8 ),  # tbc...
                ]
class Flags_misc( ctypes.Union ):
    _fields_ = [
                ("b",      Flags_bits_misc ),
                ("asByte", ctypes.c_uint8    )
               ]
    _anonymous_ = ("b")
def getAsDictStr(Byte_Commands):
    #temporary solution:
    #will use forloops later
    if (Byte_Commands.__len__() < 3):
        print("wrong size of command[], the size is %i" % Byte_Commands.__len__())
        #should throw exception of some sort.
    motor = Flags_motor()
    motor.asByte = Byte_Commands[0] 
    steering = Flags_steering()
    steering.asByte = Byte_Commands[1]
    misc = Flags_misc()
    misc.asByte = Byte_Commands[2]
    dict = {
        "motor_direction" : motor.direction ,
        "motor_speed" : motor.speed,
        "steering_direction" : steering.direction,
        "steering_position" : steering.position,
        "misc" : "unused",
        "time" : int(time.time())
        }
    return dict
def getAsDict(Byte_Commands):
    #can use forloop someway
    if (Byte_Commands.__len__() < 3):
        print("wrong size of command[], the size is %i" % Byte_Commands.__len__())
        #should throw exception of some sort.
        raise("faulty dict")
    motor = Flags_motor()
    motor.asByte = Byte_Commands[0] 
    steering = Flags_steering()
    steering.asByte = Byte_Commands[1]
    misc = Flags_misc()
    misc.asByte = Byte_Commands[2]
    dict = {
        "motor_direction" : motor.direction ,
        "motor_speed" : motor.speed,
        "steering_direction" : steering.direction,
        "steering_position" : steering.position,
        "misc" : "unused",
        "time" : int(time.time())
        }
    return dict
def getAsByteArray(dict):
    motor = Flags_motor()
    steering = Flags_steering()
    motor.direction = dict["motor_direction"]
    motor.speed = dict["motor_speed"]
    steering.direction = dict["steering_direction"]
    steering.position = dict["steering_position"]
    misc = Flags_misc()
    misc.asByte = 0
    cmd = [motor.asByte,steering.asByte,misc.asByte]
    return cmd
def blankDict():
    dict = {
        "motor_direction" : 0,
        "motor_speed" : 0,
        "steering_direction" : 0,
        "steering_position" : 0,
        "misc" : "unused",
        "time" : int(time.time())
        }
    return dict
def validDict(dict):
    if((-128 < dict["motor_speed"] < 128) and ((dict["motor_direction"]  and dict["steering_direction"])in range(0,2)) and -128 < dict["steering_position"] < 128):
        return True
    return False


