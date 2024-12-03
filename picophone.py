import machine
import utime as time
import note_utils

probe_pin = 26
speaker_pin = 2
probe = machine.ADC(probe_pin)
speaker = machine.PWM(machine.Pin(speaker_pin))

min_probe_val = 1000
e_minor = [[8000, "E4"], [13000, "G4"], [19000, "A4"], [30000, "B4"], [66000,"D5"]]
diatonic = [[2500,"C4"], [3000,"C#4"], [3600,"D4"]]
twelve = [[3400, "C4"], [4700, "C#4"], [5600, "D4"], [6500, "D#4"], 
          [7500, "E4"], [8600, "F4"], [10500, "F#4"], [12500, "G4"],
          [16000, "G#4"], [21400, "A4"], [32000, "A#4"], [66000, "B4"]]

def update_tone(probe_limit_freq_list, debug = False):
    probe_value = (probe.read_u16())
    if debug:
        time.sleep(0.5)
        print(probe_value)
        
    if probe_value < min_probe_val:
           speaker.duty_u16(0)
           return
        
    for probe_limit_freq_pair in probe_limit_freq_list:
        if probe_value < probe_limit_freq_pair[0]:
            speaker.duty_u16(int(65535/64))
            speaker.freq(probe_limit_freq_pair[1])
            return
        
def note_to_freq_list(probe_limit_note_list):
    probe_limit_freq_list = []
    for probe_limit_note_pair in probe_limit_note_list:
        temp_pair = []
        temp_pair.append(probe_limit_note_pair[0])
        temp_pair.append(note_utils.note_to_freq(probe_limit_note_pair[1],True))
        probe_limit_freq_list.append(temp_pair)
    return probe_limit_freq_list

loaded_list = note_to_freq_list(twelve)
print(loaded_list)

while True:
    update_tone(loaded_list,False)
