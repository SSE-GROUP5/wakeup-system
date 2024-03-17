import os
from dotenv import load_dotenv


class Constants:
    def __init__(self, envFilename):
        self.file_name = envFilename
        self.env_vars = {
            "CLOSED_EYES_FRAME": 10,
            "BLINKING_RATIO": 7,
            "TIMEOUT_SEC": 3,
            "WAKEUP_SERVER_URL": None,
            "ID": None,
            "ZMQ_SERVER": None
        }
        
        if not os.path.exists(envFilename):
            raise Exception("No env_trigger.txt file, please generate one")
        
        self.updateConfig()

        if self.env_vars["WAKEUP_SERVER_URL"] is None:
            raise Exception("WAKEUP_SERVER_URL not found in .env")
        if self.env_vars["ID"] is None:
            raise Exception("ID not found in env_trigger.txt")
        if self.env_vars["ZMQ_SERVER"] is None:
            raise Exception("ZMQ_SERVER not found in env_trigger.txt")

    def updateConfig(self):
        load_dotenv(self.file_name)
        with open(self.file_name, "r") as file:
            for line in file:
                key, value = line.split("=")
                self.env_vars[key] = value.strip()
                
                
        
    def get_current_env_vars(self):
        return self.env_vars


    def updateEnvFile(self, new_env_vars):
        current_env_vars = self.get_current_env_vars()
            
        with open(self.file_name, "w") as file:
            for key, value in new_env_vars.items():
                file.write(f"{key}={value}\n")
            for key, value in current_env_vars.items():
                if key not in new_env_vars:
                    file.write(f"{key}={value}\n")

        # Load the new env file
        self.updateConfig()



# face bounder indices 
FACE_OVAL=[ 10, 338, 297, 332, 284, 251, 389, 356, 454, 323, 361, 288, 397, 365, 379, 378, 400, 377, 152, 148, 176, 149, 150, 136, 172, 58, 132, 93, 234, 127, 162, 21, 54, 103,67, 109]

# lips indices for Landmarks
LIPS=[ 61, 146, 91, 181, 84, 17, 314, 405, 321, 375,291, 308, 324, 318, 402, 317, 14, 87, 178, 88, 95,185, 40, 39, 37,0 ,267 ,269 ,270 ,409, 415, 310, 311, 312, 13, 82, 81, 42, 183, 78 ]
LOWER_LIPS =[61, 146, 91, 181, 84, 17, 314, 405, 321, 375, 291, 308, 324, 318, 402, 317, 14, 87, 178, 88, 95]
UPPER_LIPS=[ 185, 40, 39, 37,0 ,267 ,269 ,270 ,409, 415, 310, 311, 312, 13, 82, 81, 42, 183, 78] 
# Left eyes indices 
LEFT_EYE =[ 362, 382, 381, 380, 374, 373, 390, 249, 263, 466, 388, 387, 386, 385,384, 398 ]
LEFT_EYEBROW =[ 336, 296, 334, 293, 300, 276, 283, 282, 295, 285 ]

# right eyes indices
RIGHT_EYE=[ 33, 7, 163, 144, 145, 153, 154, 155, 133, 173, 157, 158, 159, 160, 161 , 246 ]  
RIGHT_EYEBROW=[ 70, 63, 105, 66, 107, 55, 65, 52, 53, 46 ]



if __name__ == "__main__":
    const = Constants()

    print(const.CLOSED_EYES_FRAME)
    print(const.BLINKING_RATIO)
    print(const.TIMEOUT_SEC)