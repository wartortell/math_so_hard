__author__ = 'wartortell'

import uuid


class LanguageEncoder:
    def __init__(self):
        self.code_encoder = ""
        self.code_decoder = ""

        self.code_encoder_name = "encoder_%s" % str(uuid.uuid4()).replace("-", "_")
        self.code_decoder_name = "decoder_%s" % str(uuid.uuid4()).replace("-", "_")

    def build_encoder(self, enc):
        print "Build Encoder not implemented for this language!"

    def build_decoder(self, dec):
        print "Build Decoder not implemented for this language!"

    def build_tests(self):
        print "Build Tests not implemented for this language!"
