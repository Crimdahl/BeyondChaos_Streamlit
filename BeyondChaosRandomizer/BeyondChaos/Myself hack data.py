from typing import BinaryIO
from shutil import copyfile

FF3_ROM_PATH = ""
OUTPUT_DIRECTORY = ""


class Substitution:
    location = None
    bytestring = None

    @property
    def size(self) -> int:
        return len(self.bytestring)

    def set_location(self, location: int):
        self.location = location

    def write(self, fout: BinaryIO):
        fout.seek(self.location)
        fout.write(bytes(self.bytestring))


with open(copyfile(FF3_ROM_PATH, OUTPUT_DIRECTORY), "wb") as outfile:
    display_sub = Substitution()
    # PATCH_ITEM_DESC, 0xc38706, 4, [ byte data; ]
    display_sub.set_location(0x38706)
    display_sub.bytestring = bytes([0x22, 0x03, 0x00, 0xF0])
    display_sub.write(outfile)

    # PATCH_ITEM_DESC, 0xc389e6, 4, [ byte data; ]
    display_sub.set_location(0x389E6)
    display_sub.bytestring = bytes([0x22, 0x2C, 0x00, 0xF0])
    display_sub.write(outfile)

    names_sub = Substitution()
    # PATCH_ORIGINAL_NAME, 0xc33311, 5, [ byte data; ]
    names_sub.set_location(0x33311)
    names_sub.bytestring = bytes([0x22, 0x35, 0x07, 0xF0, 0xEA])
    names_sub.write(outfile)

    # PATCH_ORIGINAL_NAME, 0xc3335d, 5, [ byte data; ]
    names_sub.set_location(0x3335D)
    names_sub.bytestring = bytes([0x22, 0x43, 0x07, 0xF0, 0xEA])
    names_sub.write(outfile)

    # PATCH_ORIGINAL_NAME, 0xc333a9, 5, [ byte data; ]
    names_sub.set_location(0x333A9)
    names_sub.bytestring = bytes([0x22, 0x51, 0x07, 0xF0, 0xEA])
    names_sub.write(outfile)

    # PATCH_ORIGINAL_NAME, 0xc333f5, 5, [ byte data; ]
    names_sub.set_location(0x333F5)
    names_sub.bytestring = bytes([0x22, 0x5F, 0x07, 0xF0, 0xEA])
    names_sub.write(outfile)

    # PATCH_ORIGINAL_NAME, 0xc37973, 4, [ byte data; ]
    names_sub.set_location(0x37973)
    names_sub.bytestring = bytes([0x22, 0x6D, 0x07, 0xF0])
    names_sub.write(outfile)

    natmag_learn_sub = Substitution()
    # PATCH_NATURAL_MAGIC, 0xc261b6, 0, [ byte data; ]
    natmag_learn_sub.set_location(0x261b6)
    natmag_learn_sub.bytestring = bytes([0x22, 0x4B, 0x08, 0xF0] + [0xEA] * 10)
    natmag_learn_sub.write(outfile)

    # PATCH_NATURAL_MAGIC, 0xc0a182, 0, [ byte data; ]
    natmag_learn_sub.set_location(0xa182)
    natmag_learn_sub.bytestring = bytes([0x22, 0x73, 0x08, 0xF0] + [0xEA] * 4)
    natmag_learn_sub.write(outfile)

    status_sub = Substitution()
    # PATCH_STATUS_MENU, 0xc35ead, 4, [ byte data; ]
    status_sub.set_location(0x35EAD)
    status_sub.bytestring = bytes([0x22, 0x60, 0x0A, 0xF0]) # StatusMenu__FixOverflow
    status_sub.write(outfile)

    # PATCH_STATUS_MENU, 0xc35e91, 4, [ byte data; ]
    status_sub.set_location(0x35E91)
    status_sub.bytestring = bytes([0x22, 0x6B, 0x0A, 0xF0]) # StatusMenu__FixWindowSize
    status_sub.write(outfile)

    # PATCH_STATUS_MENU, 0xc363ba, 4, [ byte data; ]
    status_sub.set_location(0x363BA)
    status_sub.bytestring = bytes([0x22, 0x76, 0x0A, 0xF0]) # StatusMenu__FixSelection
    status_sub.write(outfile)

    # PATCH_STATUS_MENU, 0xc322a3, 4, [ byte data; ]
    status_sub.set_location(0x322A3)
    status_sub.bytestring = bytes([0x22, 0x88, 0x0A, 0xF0]) # StatusMenu__FixScrollReset
    status_sub.write(outfile)

    # PATCH_STATUS_MENU, 0xc3640c, 5, [ byte data; ]
    status_sub.set_location(0x3640C)
    status_sub.bytestring = bytes([0x22, 0x98, 0x0A, 0xF0, 0x60]) # StatusMenu__Main
    status_sub.write(outfile)

    rage_sub = Substitution()
    # PATCH_RAGE_DESC, 0xc321d9, 4, [ byte data; ]
    rage_sub.set_location(0x321D9)
    rage_sub.bytestring = bytes([0x22, 0xD9, 0x0C, 0xF0])
    rage_sub.write(outfile)

    # PATCH_RAGE_DESC, 0xc328ba, 7, [ byte data; ]
    rage_sub.set_location(0x328BA)
    rage_sub.bytestring = bytes([0x22, 0x1D, 0x0D, 0xF0, 0xF0, 0x01, 0x60])
    rage_sub.write(outfile)