__author__ = 'wartortell'

import uuid

from encoder import LanguageEncoder


class EncoderPython(LanguageEncoder):
    def create_encoder(self, enc, name):
        meh = "def %s(enc, length):\n" % name
        meh += "    dec = map(ord, enc)\n"
        meh += "    for i in range(length):\n"

        for i in range(len(enc)):
            if enc[i]["type"] == "single_xor":
                meh += "        dec[i] ^= %d\n" % (enc[i]["value"] & 0xFF)
            elif enc[i]["type"] == "single_add":
                meh += "        dec[i] = (dec[i] + %d) & 0xFF\n" % (enc[i]["value"] & 0xFF)
            elif enc[i]["type"] == "single_sub":
                meh += "        dec[i] = (dec[i] - %d) & 0xFF\n" % (enc[i]["value"] & 0xFF)

        meh += "    return \"\".join(map(chr, dec))\n\n\n"

        return meh

    def build_encoder(self, enc):
        self.code_encoder = self.create_encoder(enc, self.code_encoder_name)

    def build_decoder(self, dec):
        self.code_decoder = self.create_encoder(dec, self.code_decoder_name)

    def build_tests(self):
        with open("evil_python.py", "w") as f:

            f.write(self.code_encoder)
            f.write(self.code_decoder)

            f.write("def test_shit(pt1):\n")
            f.write("    ct1 = %s(pt1, len(pt1))\n" % self.code_encoder_name)
            f.write("    dt1 = %s(ct1, len(pt1))\n" % self.code_decoder_name)
            f.write("    if not (pt1 == dt1):\n")
            f.write("        print \"Your math done goofed: %s\" % pt1\n\n")
            f.write("    else:\n")
            f.write("        print \"Test passed: %s\" % pt1\n\n\n")

            f.write("def main():\n")
            f.write("    test_shit(\"ballsnstuff\")\n")
            f.write("    test_shit(\"asdn1234567890~!@#$%^&*()\")\n\n")

            f.write("main()\n")




