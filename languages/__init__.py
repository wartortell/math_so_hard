__author__ = 'wartortell'

from ansi_c import EncoderAnsiC
from asm_32 import EncoderAsm32
from asm_64 import EncoderAsm64
from cpp import EncoderCPP
from delphi import EncoderDelphi
from golang import EncoderGolang
from python import EncoderPython

encoder_classes = {"ansi_c": EncoderAnsiC,
                   "asm_32": EncoderAsm32,
                   "asm_64": EncoderAsm64,
                   "cpp": EncoderCPP,
                   "delphi": EncoderDelphi,
                   "golang": EncoderGolang,
                   "python": EncoderPython}