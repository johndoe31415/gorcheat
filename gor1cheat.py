#!/usr/bin/python3
#
#	gorcheat - Game of Robot cheat utility
#	Copyright (C) 2017-2017 Johannes Bauer
#
#	This file is part of gorcheat.
#
#	gorcheat is free software; you can redistribute it and/or modify
#	it under the terms of the GNU General Public License as published by
#	the Free Software Foundation; this program is ONLY licensed under
#	version 3 of the License, later versions are explicitly excluded.
#
#	gorcheat is distributed in the hope that it will be useful,
#	but WITHOUT ANY WARRANTY; without even the implied warranty of
#	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#	GNU General Public License for more details.
#
#	You should have received a copy of the GNU General Public License
#	along with gorcheat; if not, write to the Free Software
#	Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#
#	Johannes Bauer <JohannesBauer@gmx.de>

import sys
import subprocess
import collections
import time
from HexDump import HexDump
from FriendlyArgumentParser import FriendlyArgumentParser
from BackpackItem import BackpackItem
from SceneData import SceneData

parser = FriendlyArgumentParser(add_help = False)
parser.add_argument("-s", "--save_clock", action = "count", default = 0, help = "Add a clock used for saving the game. Can be specified multiple times.")
parser.add_argument("-a", "--add_item", metavar = "item_name", action = "append", type = str, default = [ ], help = "Add the specified item name to the inventory. Can be specified multiple times.")
parser.add_argument("-h", "--hexedit", action = "store_true", help = "Open a hexeditor to edit the raw save game")
parser.add_argument("-v", "--verbose", action = "store_true", help = "Be more verbose")
parser.add_argument("infile", metavar = "infile", type = str, help = "Input savegame")
parser.add_argument("outfile", nargs = "?", metavar = "outfile", type = str, help = "Output savegame. If equal to input, input file will be overwritten (not recommended).")
args = parser.parse_args(sys.argv[1:])

class Robot1Cheat(object):
	_Position = collections.namedtuple("Position", [ "x", "y", "scene", "prev_scene" ])
	_XOR_PATTERN = bytes.fromhex("1c d5 59 d6 5c 51 b2 c6 0c 3f 88 ca ed 8e 1c fd 25 04 c1 56 26 1b 66 a9 dd")
	_OFFSETS = {
		"backpack":			0x6,
		"lives":			0xba,
		"gold":				0xbb,
		"score":			0xa2,
		"player_name":		0xbf,
		"pos_x":			0xb6,
		"pos_y":			0xb7,
		"current_scene":	0xa6,
		"previous_scene":	0xa0,
		"scene_data":		0x126,
#		"scene_data":		0x472,
	}
	_BACKPACK_ITEM_SIZE = 2
	_MAX_BACKPACK_ITEMS = 50

	def __init__(self, infile):
		with open(infile, "rb") as f:
			data = f.read()
		self._data = self._encode_decode(data)

	@classmethod
	def _encode_decode(cls, indata):
		return bytearray(inbyte ^ cls._XOR_PATTERN[i % len(cls._XOR_PATTERN)] for (i, inbyte) in enumerate(indata))

	def write(self, outfile):
		encoded_data = self._encode_decode(self._data)
		with open(outfile, "wb") as f:
			f.write(encoded_data)

	def _get_uint_n(self, offset, length):
		return sum(self._data[offset + i] << (8 * i) for i in range(length))

	def _get_uint32(self, offset):
		return self._get_uint_n(offset, 4)

	def _get_zstring(self, offset, maxlength = 1024):
		string = bytearray()
		for i in range(offset, offset + maxlength):
			if self._data[i] == 0:
				break
			string.append(self._data[i])
		return string.decode("ibm850")

	@property
	def player_pos(self):
		return self._Position(x = self._data[self._OFFSETS["pos_x"]], y = self._data[self._OFFSETS["pos_y"]], scene = self._data[self._OFFSETS["current_scene"]], prev_scene = self._data[self._OFFSETS["previous_scene"]])

	@property
	def player_name(self):
		return self._get_zstring(self._OFFSETS["player_name"], 16)

	@property
	def lives(self):
		return self._data[self._OFFSETS["lives"]]

	@property
	def gold(self):
		return self._data[self._OFFSETS["gold"]]

	@property
	def score(self):
		return self._get_uint32(self._OFFSETS["score"])

	def next_empty_backpack_index(self):
		backpack = self.get_backpack()
		for (index, item) in enumerate(backpack):
			if item.is_empty:
				return index

	def get_backpack(self):
		backpack_data = self._data[self._OFFSETS["backpack"] : self._OFFSETS["backpack"] + (self._BACKPACK_ITEM_SIZE * self._MAX_BACKPACK_ITEMS)]
		backpack_data = [ BackpackItem(backpack_data[i], backpack_data[i + 1]) for i in range(0, len(backpack_data), self._BACKPACK_ITEM_SIZE) ]
		return backpack_data

	def put_backpack(self, index, item):
		offset = self._OFFSETS["backpack"] + (index * self._BACKPACK_ITEM_SIZE)
		self._data[offset + 0] = item.main_id
		self._data[offset + 1] = item.sub_id

	def add_item(self, item_name):
		index = self.next_empty_backpack_index()
		if index is None:
			raise Exception("No more room in backpack.")
		self.put_backpack(index, BackpackItem.new_by_name(item_name))

	def scene_data(self):
		scene_offset = self._OFFSETS["scene_data"]
		scene_data = SceneData(self._data[scene_offset : ], base_offset = scene_offset)

	def hexedit(self, background_write_filename = None):
		with open("tempfile.tmp", "wb") as f:
			f.write(self._data)

		hexedit_proc = subprocess.Popen([ "hexedit", "tempfile.tmp" ])
		if background_write_filename is None:
			hexedit_proc.wait_pid()
		else:
			while True:
				try:
					hexedit_proc.wait(timeout = 0.5)
				except subprocess.TimeoutExpired:
					# hexedit still alive
					with open("tempfile.tmp", "rb") as f:
						self._data = f.read()
					self.write(background_write_filename)
				else:
					break

	def dump(self):
		HexDump().dump(self._data)

savefile = Robot1Cheat(args.infile)
for i in range(args.save_clock):
	savefile.add_item("save_clock")
for item_name in args.add_item:
	savefile.add_item(item_name)
if args.hexedit:
	savefile.hexedit(args.outfile or args.infile)
if args.verbose:
	print("Player  : %s" % (savefile.player_name))
	print("Position: %s" % (str(savefile.player_pos)))
	print("Lives   : %d" % (savefile.lives))
	print("Gold    : %d" % (savefile.gold))
	print("Score   : %d" % (savefile.score))
	print(savefile.get_backpack())
	savefile.scene_data()
savefile.write(args.outfile or args.infile)

