""" list of commands used by Rigol DS1000 oscilloscope

    Those commandes are unused in this project ()
    based on
    http://sdpha2.ucsd.edu/Lab_Equip_Manuals/Rigol_DS1000_Progr_Manu.pdf

    Post Tenebras Lab the geneva(Hackerspace)
"""

__author__ = 'Sebastien Chassot'
__author_email__ = 'sebastien@sinux.net'

__version__ = "1.0.1"
__copyright__ = ""
__licence__ = "GPL"


class rigol_1000_cmd():
    def __init__(self):
        self._system_cmd = {
            'name': "*IDN?",
            'run': ":RUN",
            'stop': ":STOP",
            'auto': ":AUTO",
            'force': ":FORCetrig",
            'trig': ":Trig%50",
            'hardcpy': ":HARDcopy",
            'info': ":INFO:LANGuage",
            'counter': ":COUNter:ENABle",
            'beep_en': ":BEEP:ENABle",
            'beep': ":BEEP:ACTion",
        }

        self._keybord_cmd = {
            'lock': ":KEY:LOCK",
            'run': ":KEY:RUN",
            'auto': ":KEY:AUTO",
            'chan_1': ":KEY:CHANnel1",
            'chan_2': ":KEY:CHANnel2",
            'math': ":KEY:MATH",
            'ref': ":KEY:REF",
            'f1': ":KEY:F1",
            'f2': ":KEY:F2",
            'f3': ":KEY:F3",
            'f4': ":KEY:F4",
            'f5': ":KEY:F5",
            'menu_off': ":KEY:MNUoff",
            'measure': ":KEY:MEASure",
            'cursor': ":KEY:CURSor",
            'acquire': ":KEY:ACQuire",
            'min_funct': ":KEY:-FUNCtion",
            'storage': ":KEY:STORage",
            'util': ":KEY:UTILity",
            'menu_time': ":KEY:MNUTIME",
            'menu_trig': ":KEY:MNUTRIG",
            'trig_50': ":KEY:Trig%50",
            'force': ":KEY:FORCe",
            'v_pos_inc': ":KEY:V_POS_INC",
            'v_pos_dec': ":KEY:V_POS_DEC",
            'v_scale_inc': ":KEY:V_SCALE_INC",
            'v_scale_dec': ":KEY:V_SCALE_DEC",
            'h_scale_inc': ":KEY:H_SCALE_INC",
            'h_scale_dec': ":KEY:H_SCALE_DEC",
            'trig_level_inc': ":KEY:TRIG_LVL_INC",
            'trig_level_dec': ":KEY:TRIG_LVL_DEC",
            'h_pos_inc': ":KEY:H_POS_INC",
            'h_pos_dec': ":KEY:H_POS_DEC",
            'prompt_v': ":KEY:PROMPT_V",
            'prompt_h': ":KEY:PROMPT_H",
            'function': ":KEY:FUNCtion",
            'plus_funct': ":KEY:+FUNCtion",
            'display': ":KEY:DISPlay",
            'prompt_v_pos': ":KEY:PROMPT_V_POS",
            'prompt_h_pos': ":KEY:PROMPT_H_POS",
            'prompt_trig_level': ":KEY:PROMPT_TRIG_LVL",
            'key_off': ":KEY:OFF",
        }

        self._measure_cmd = {
            'clear': ":MEASure:CLEar",
            'vpp':":MEASure:VPP?",
            'vmax': ":MEASure:VMAX?",
            'vmin': ":MEASure:VMIN?",
            'vamp': ":MEASure:VAMPlitude?",
            'vtop': ":MEASure:VTOP?",
            'vbase': ":MEASure:VBASe?",
            'vaverage': ":MEASure:VAVerage?",
            'vrms': ":MEASure:VRMS?",
            'overshoot': ":MEASure:OVERshoot?",
            'preshoot': ":MEASure:PREShoot?",
            'freq': ":MEASure:FREQuency?",
            'rise': ":MEASure:RISetime?",
            'fall': ":MEASure:FALLtime?",
            'period': ":MEASure:PERiod?",
            'pwidth': ":MEASure:PWIDth?",
            'nwidth': ":MEASure:NWIDth?",
            'pdutycycle': ":MEASure:PDUTycycle?",
            'ndutycycle': ":MEASure:NDUTycycle?",
            'pdelay': ":MEASure:PDELay?",
            'ndelay': ":MEASure:NDELay?",
            'tot': ":MEASure:TOTal",
            'src': ":MEASure:SOURce"}

        self._acquire_cmd = {
            'type': ":ACQuire:TYPE",
            'mode': ":ACQuire:MODE",
            'average':  ":ACQuire:AVERages",
            'sample': ":ACQuire:SAMPlingrate?"
        }

        self._display_cmd = {
            'type': ":DISPlay:TYPE",
            'grid': ":DISPlay:GRID",
            'persist': ":DISPlay:PERSist",
            'menu': ":DISPlay:MNUDisplay",
            'status': ":DISPlay:MNUStatus",
            'clear': ":DISPlay:CLEar",
            'screen': ":DISPlay:SCReen",
            'brightness': ":DISPlay:BRIGhtness",
            'intenity': ":DISPlay:INTensity"
        }

        self._vertical_cmd = {
            'bw_limit': ":CHANnel<n>:BWLimit",
            'coupling': ":CHANnel<n>:COUPling",
            'disp': ":CHANnel<n>:DISPlay",
            'invert': ":CHANnel<n>:INVert",
            'offset': ":CHANnel<n>:OFFSet",
            'probe': ":CHANnel<n>:PROBe",
            'scale': ":CHANnel<n>:SCALe",
            'filter': ":CHANnel<n>:FILTer",
            'mem_depth': ":CHANnel<n>:MEMoryDepth?",
            'vernier': ":CHANnel<n>:VERNier"
        }

        self._horizontal_cmd = {
            'mode': ":TIMebase:MODE",
            'offset': ":TIMebase[:DELayed]:OFFSet",
            'scale': ":TIMebase[:DELayed]:SCALe",
            'format': ":TIMebase:FORMat",
        }

        self._trigger_cmd = {
            'mode': ":TRIGger:MODE",
            'src': ":TRIGger<mode>:SOURce",
            'level': ":TRIGger<mode>:LEVel",
            'sweep': ":TRIGger<mode>:SWEep",
            'coupl': ":TRIGger<mode>:COUPling",
            'hold_off': ":TRIGger:HOLDoff",
            'status': ":TRIGger:STATus?"
        }

        self._trigger_mode = {
            'slope': ":TRIGger:EDGE:SLOPe",
            'mode': ":TRIGger:PULSe:MODE",
            'width': ":TRIGger:PULSe:WIDTh",
            'time': ":TRIGger:SLOPe:TIME",
            'slope_mode': ":TRIGger:SLOPe:MODE",
            'window': ":TRIGger:SLOPe:WINDow",
            'level_a': ":TRIGger:SLOPe:LEVelA",
            'level_b': ":TRIGger:SLOPe:LEVelB",
            'video_mode': ":TRIGger:VIDEO:MODE",
            'video_pol': ":TRIGger:VIDEO:POLarity",
            'video_stand': ":TRIGger:VIDEO:STANdard",
            'video_line': ":TRIGger:VIDEO:LINE",
            'alt_src': ":TRIGger:ALTernation:SOURce",
            'alt_type': ":TRIGger:ALTernation:TYPE",
            'alt_time_scale': ":TRIGger:ALTernation:TimeSCALe",
            'alt_off': ":TRIGger:ALTernation:TimeOFFSet",
            'alt_level': ":TRIGger:ALTernation<mode>:LEVel",
            'alt_edg_slope': ":TRIGger:ALTernation:EDGE:SLOPe",
            'alt_mode': ":TRIGger:ALTernation<mode>:MODE",
            'alt_time': ":TRIGger:ALTernation<mode>:TIME",
            'alt_video_pol': ":TRIGger:ALTernation:VIDEO:POLarity",
            'alt_video_stand': ":TRIGger:ALTernation:VIDEO:STANdard",
            'alt_video_line': ":TRIGger:ALTernation:VIDEO:LINE",
            'alt_slope_win': ":TRIGger:ALTernation:SLOPe:WINDow",
            'alt_slope_lev_a': ":TRIGger:ALTernation:SLOPe:LEVelA",
            'alt_slope_lev_b': ":TRIGger:ALTernation:SLOPe:LEVelB",
            'alt_couping': ":TRIGger:ALTernation<mode>:COUPling"
        }

        self._math_cmd = {
            'math_disp': ":MATH:DISPlay",
            'fft_disp': ":FFT:DISPlay"
        }

        self.menu = {
            'system': self._system_cmd,
            'keybord': self._keybord_cmd,
            'measure': self._measure_cmd,
            'acquire': self._acquire_cmd,
            'display': self._display_cmd,
            'vertical': self._vertical_cmd,
            'horizontal': self._horizontal_cmd,
            'trigger_cmd': self._trigger_cmd,
            'trigger_mode': self._trigger_mode,
            'math': self._math_cmd
        }


    def __system(self, cmd):
        return self._system_cmd[cmd]

    def __measure(self, cmd):
        return self._measure_cmd[cmd]

    def __acquire(self, cmd):
        return self._acquire_cmd[cmd]

    def cmd(self, lst, c):
        return self.menu[lst][c]

    def list_cmd(self, lst):
        print(list(self.menu[lst]))

    def list_all(self):
        for m in self.menu:
            print("Menu "+m+" : ")
            self.list_cmd(m)

