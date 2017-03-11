__author__ = 'wartortell'

import random
import logging
import argparse

from languages import encoder_classes


class MSHWeights:
    def __init__(self):

        self.logger = logging.getLogger("MSH Configuration")
        self.logger.setLevel(logging.INFO)

        self.weights = {"single_xor": 1,
                        "single_add": 1,
                        "single_sub": 1}

        self.opposites = {"single_xor": "single_xor",
                          "single_add": "single_sub",
                          "single_sub": "single_add"}

        # The list used by Obfusion when determining which code block will be used
        self.weighted_list = []
        self.weighted_lookup = []

        # The list of values used for random code type choice
        self.code_types = []

        # Initiate the lists
        self.create_weighted_list()
        self.create_code_types()

    def set_weight(self, name, weight):
        """
        Description:
            Set a code type's weight
        :param name: string
        :param weight: int
        :return: None
        """

        if not (name in self.weights.keys()):
            self.logger.error("The code type %s is not known/implemented!" % name)
            return

        if not (type(weight) == int):
            self.logger.error("Weight values must be provided as integers: %s" % str(weight))
            return

        self.weights[name] = weight

        self.create_weighted_list()
        self.create_code_types()

    def set_all_weights(self, new_weights):
        """
        Description:
            Set all the weights to new values, useful for using predefined weight lists

        :param new_weights: dict: string->int
        :return: None
        """

        self.weights = new_weights

        self.create_weighted_list()
        self.create_code_types()

    def create_weighted_list(self):
        """
        Description:
            Create the weighted list based on the current weights

        :return: None
        """

        self.weighted_list = self.weights.keys()
        self.weighted_lookup = []

        for i in range(len(self.weighted_list)):
            for j in range(self.weights[self.weighted_list[i]]):
                self.weighted_lookup.append(i)

    def create_code_types(self):
        """
        Description:
            Fill the code_types array with all code types that have any weight

        :return: None
        """

        self.code_types = []
        for key in self.weights.keys():
            if self.weights[key]:
                self.code_types.append(key)

    def show_weights(self):
        """
        Description:
            Prints the percentage weight of each code type

        :return: None
        """

        print("\nCurrent Weights:\n---------------------")
        for key in sorted(self.weights.keys()):
            print("%s: %2.2f%%" % (key, 100.0*float(self.weights[key])/float(len(self.weighted_lookup))))

    def choose_weighted(self):
        """
        Description:
            Select a weighted choice from the list of code types

        :return: string
        """
        return self.weighted_list[random.choice(self.weighted_lookup)]

    def choose_random(self):
        """
        Description:
            Choose a random code type (do not use weights)
            NOTE: code types with weight 0 will still be ignored by this function

        :return: string
        """

        return random.choice(self.code_types)

    def get_value(self, code_type):
        if code_type in ["single_xor", "single_add", "single_sub", "single_and", "single_or"]:
            return random.randint(0, 256)

    def get_opposite(self, code_type):
        return self.opposites[code_type]


class MSHConfig:
    def __init__(self, arch, language, complexity):
        self.weights = MSHWeights()
        self.arch = arch
        self.language = language
        self.complexity = complexity


class MSH:
    def __init__(self, arch, language, complexity):
        self.config = MSHConfig(arch, language, int(complexity))

        self.language_encoder = encoder_classes[language]()
        self.python_encoder = encoder_classes["python"]()

        self.encoder_struct, self.decoder_struct = self.create_encoder_decoder_structs()

        self.language_encoder.build_encoder(self.encoder_struct)
        self.language_encoder.build_decoder(self.decoder_struct)

        self.language_encoder.build_tests()

    def create_encoder_decoder_structs(self):
        enc = []
        dec = []

        for i in range(self.config.complexity):
            code_type = self.config.weights.choose_weighted()
            value = self.config.weights.get_value(code_type)
            opp_code_type = self.config.weights.get_opposite(code_type)

            enc.append({"type": code_type, "value": value})
            dec.insert(0, {"type": opp_code_type, "value": value})

        return enc, dec

    def create_decoder_struct(self):
        pass

    def encode(self, bytes):
        pass

    def decode(self, bytes):
        pass


def parse_arguments():
    parser = argparse.ArgumentParser(description="Create an obfuscated piece of code")
    parser.add_argument('-l', '--language', dest='language', default="cpp",
                        choices=['ansi_c', 'cpp', 'csharp', 'delphi', 'golang', 'python'],
                        help='the language you want to generate obfuscated code in')
    parser.add_argument('-a', '--arch', dest='arch', default="Win_x86",
                        choices=['Win_x86', 'Win_x64', 'POSIX_x86', 'POSIX_x64'], help='the architecture to target')
    parser.add_argument('-c', '--complexity', dest='complexity', default="10",
                        help='the complexity of the encoding algorithm to create')
    return parser.parse_args()


def main():

    args = parse_arguments()

    encoder = MSH(args.arch, args.language, args.complexity)


if __name__ == "__main__":
    main()