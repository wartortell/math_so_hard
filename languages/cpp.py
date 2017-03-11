__author__ = 'wartortell'

import uuid

from encoder import LanguageEncoder


class EncoderCPP(LanguageEncoder):
    def __init__(self):
        self.code_encoder = ""
        self.code_decoder = ""

        self.code_encoder_name = "encoder_%s" % uuid.uuid4()
        self.code_decoder_name = "decoder_%s" % uuid.uuid4()

    def create_encoder(self, enc, name):
        meh = "char* %s(char* enc, int length) {\n" % name
        meh += "  for(int i = 0; i < length; i++) {\n"

        for i in range(len(enc)):
            print enc[i]
            if enc[i]["type"] == "single_xor":
                meh += "    enc[i] = (enc[i] ^ %d);\n" % (enc[i]["value"] & 0xFF)
            elif enc[i]["type"] == "single_add":
                meh += "    enc[i] = (enc[i] + %d) & 0xFF;\n" % (enc[i]["value"] & 0xFF)
            elif enc[i]["type"] == "single_sub":
                meh += "    enc[i] = (enc[i] - %d) & 0xFF;\n" % (enc[i]["value"] & 0xFF)

        meh += "  }\n"
        meh += "}\n\n"

        return meh

    def build_encoder(self, enc):
        self.code_encoder = self.create_encoder(enc, self.code_encoder_name)

    def build_decoder(self, dec):
        self.code_decoder = self.create_encoder(dec, self.code_decoder_name)

