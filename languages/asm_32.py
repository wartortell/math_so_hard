__author__ = 'wartortell'

from encoder import LanguageEncoder


class EncoderAsm32(LanguageEncoder):

    def create_encoder(self, enc, name):
        meh = ""
        return meh

    def build_encoder(self, enc):
        self.code_encoder = self.create_encoder(enc, self.code_encoder_name)

    def build_decoder(self, dec):
        self.code_decoder = self.create_encoder(dec, self.code_decoder_name)

    def build_tests(self):
        with open("evil_asm32.asm", "w") as f:

            f.write("")


