from kmk.kmk_keyboard import KMKKeyboard
from kmk.keys import KC
import json
import board 
from kmk.extensions.rgb import RGB, AnimationModes
from kmk.modules.encoder import EncoderHandler
import busio
from kmk.extensions.display import Display
from kmk.extensions.display.ssd1306 import SSD1306
from kmk.extensions.display.display import OledData

keyboard = KMKKeyboard()
encoder_handler = EncoderHandler()

i2c_bus = busio.I2C(board.D5,board.D4)
oled_driver = SSD1306(i2c=i2c_bus, device_address=0x3C)
oled = Display(display=oled_driver, width=128, height=32)

gif_animation = OledData(
    image="animation.pbm",   
    corner=(0, 0),        
)

# Pos1 -> D9, Pos2 -> D8, Pos3 -> D3, 
# Pos4 -> D10, Pos5 -> D0, Pos6 -> D2
keyboard.pins = [board.D9,
        board.D8,
        board.D3,
        board.D10,
        board.D0,
        board.D2]

encoder_handler.pins = ((board.D6, board.D7,(None,False)),) 

encoder_handler.map = [((KC.AUDIO_VOL_UP, KC.AUDIO_VOL_DOWN),)]

def load_commands():
    try:
        with open('commands.json','r') as f:
            commands = json.load(f)
        return commands 
    except OSError:
        default_commands = {
            "pos_1": "COPY",
            "pos_2": "PASTE",
            "pos_3": "UNDO",
            "pos_4": "MUTE",
            "pos_5": "ENTER",
            "pos_6": "PLAY_PAUSE"}
        with open('commands.json','w') as f:
            json.dump(default_commands, f, indent=4)
        return default_commands
    
commands = load_commands()

KEY_MAP = {
    "COPY": KC.LCTRL(KC.C),
    "PASTE": KC.LCTRL(KC.V),
    "UNDO": KC.LCTRL(KC.Z),
    "MUTE": KC.AUDIO_MUTE,
    "VOL_UP": KC.AUDIO_VOL_UP,
    "VOL_DOWN": KC.AUDIO_VOL_DOWN,
    "ENTER": KC.ENTER,
    "SPACE": KC.SPACE,
    "ESCAPE": KC.ESC,
    "PLAY_PAUSE": KC.AUDIO_PLAY_PAUSE,
    "MEDIA_NEXT": KC.AUDIO_MEDIA_NEXT,
    "SAVE": KC.LCTRL(KC.S),           
    "SELECT_ALL": KC.LCTRL(KC.A),      
    "CLOSE_TAB": KC.LCTRL(KC.W),       
    "TASK_MANAGER": KC.LCTRL(KC.LSHIFT(KC.ESC))
}

kmk_commands = []
for i in range(1,7):
    name = f'pos_{i}'
    action = KEY_MAP.get(commands[name], KC.NO)
    kmk_commands.append(action)

keyboard.keymap = [kmk_commands]

rgb = RGB(
    pixel_pin= board.D1,
    num_pixels=7,
    animation_mode=AnimationModes.BREATHING, 
    val_default=100    
)

keyboard.extensions.append(rgb)
keyboard.modules.append(encoder_handler)
keyboard.extensions.append(oled)
oled.entries.append(gif_animation)

if __name__=='__main__':
    keyboard.go()
