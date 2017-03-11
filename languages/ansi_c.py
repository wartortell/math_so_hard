__author__ = 'wartortell'

from encoder import LanguageEncoder


class EncoderAnsiC(LanguageEncoder):

    def create_encoder(self, enc, name):
        meh = "char* %s(char* enc, int length) {\n" % name
        meh += "  printf(\"Encoding %s\\n\", enc);\n"
        meh += "  char* retme = (char*) malloc(length);\n"
        meh += "  if (retme == NULL)\n"
        meh += "    return NULL;\n\n"
        meh += "  for(int i = 0; i < length; i++)\n"
        meh += "    retme[i] = enc[i];\n\n"
        meh += "  for(int i = 0; i < length; i++) {\n"

        for i in range(len(enc)):
            if enc[i]["type"] == "single_xor":
                meh += "    retme[i] = (retme[i] ^ %d);\n" % (enc[i]["value"] & 0xFF)
            elif enc[i]["type"] == "single_add":
                meh += "    retme[i] = (retme[i] + %d) & 0xFF;\n" % (enc[i]["value"] & 0xFF)
            elif enc[i]["type"] == "single_sub":
                meh += "    retme[i] = (retme[i] - %d) & 0xFF;\n" % (enc[i]["value"] & 0xFF)

        meh += "  }\n"
        meh += "  return retme;\n"
        meh += "}\n\n"

        return meh

    def build_encoder(self, enc):
        self.code_encoder = self.create_encoder(enc, self.code_encoder_name)

    def build_decoder(self, dec):
        self.code_decoder = self.create_encoder(dec, self.code_decoder_name)

    def build_tests(self):
        with open("evil_ansi.c", "w") as f:

            f.write("#include <windows.h>\n\n")
            #f.write("#include <unistd.h>\n\n")
            f.write("#include <string.h>\n\n")

            f.write(self.code_encoder)
            f.write(self.code_decoder)

            f.write("void print_as_hex(char* enc_me, int x) {\n")
            f.write("  int i;\n")
            f.write("  for (i = 0; i < x; i++) {\n")
            f.write("      if (i > 0) printf(\":\");\n")
            f.write("      printf(\"%2X\", enc_me[i]);\n")
            f.write("  }\n")
            f.write("  printf(\"\\n\");\n}\n\n")

            f.write("void ansi_c_tests() {\n")
            f.write("  char* pt1 = \"crap\";\n")
            f.write("  int l1 = strlen(pt1);\n")

            f.write("  char* pt2 = \"1234567890!@##$%^&*()\";\n")
            f.write("  int l2 = strlen(pt2);\n")

            f.write("  char* pt3 = \"OMGLOB Lumpy Space Princes is #1 all the way across the sky!\";\n")
            f.write("  int l3 = strlen(pt3);\n")

            #f.write("  char ct1[9];\n")
            #f.write("  char ct2[21];\n")
            #f.write("  char ct3[26];\n")
#
            #f.write("  char dt1[9];\n")
            #f.write("  char dt2[21];\n")
            #f.write("  char dt3[26];\n")

            f.write("  char* ct1 = %s(pt1, l1);\n" % self.code_encoder_name)
            f.write("  char* ct2 = %s(pt2, l2);\n" % self.code_encoder_name)
            f.write("  char* ct3 = %s(pt3, l3);\n" % self.code_encoder_name)

            f.write("  char* dt1 = %s(ct1, l1);\n" % self.code_decoder_name)
            f.write("  char* dt2 = %s(ct2, l2);\n" % self.code_decoder_name)
            f.write("  char* dt3 = %s(ct3, l3);\n" % self.code_decoder_name)

            f.write("  printf(\"Plain Text 1: %s\\n\", pt1);\n")
            f.write("  printf(\"Plain Text 2: %s\\n\", pt2);\n")
            f.write("  printf(\"Plain Text 3: %s\\n\", pt3);\n")

            f.write("  printf(\"Cipher Text 1: %s\\n\", ct1);\n")# print_as_hex(ct1, l1); printf(\"\\n\");\n")
            f.write("  printf(\"Cipher Text 2: %s\\n\", ct2);\n")# print_as_hex(ct2, l2); printf(\"\\n\");\n")
            f.write("  printf(\"Cipher Text 3: %s\\n\", ct3);\n")# print_as_hex(ct3, l3); printf(\"\\n\");\n")

            f.write("  printf(\"Decoded Text 1: %s\\n\", dt1);\n")
            f.write("  printf(\"Decoded Text 2: %s\\n\", dt2);\n")
            f.write("  printf(\"Decoded Text 3: %s\\n\", dt3);\n")

            f.write("}\n\n")

            f.write("int main() {\n  ansi_c_tests();\n}\n\n")

