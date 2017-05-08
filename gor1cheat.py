#!/usr/bin/python3
#
#	gotcheat - Game of Robot cheat utility
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

parser = FriendlyArgumentParser(add_help = False)
parser.add_argument("-s", "--save_clock", action = "count", default = 0, help = "Add a clock used for saving the game. Can be specified multiple times.")
parser.add_argument("-a", "--add_item", metavar = "item_name", action = "append", type = str, default = [ ], help = "Add the specified item name to the inventory. Can be specified multiple times.")
parser.add_argument("-h", "--hexedit", action = "store_true", help = "Open a hexeditor to edit the raw save game")
parser.add_argument("-v", "--verbose", action = "store_true", help = "Be more verbose")
parser.add_argument("infile", metavar = "infile", type = str, help = "Input savegame")
parser.add_argument("outfile", nargs = "?", metavar = "outfile", type = str, help = "Output savegame. If equal to input, input file will be overwritten (not recommended).")
args = parser.parse_args(sys.argv[1:])

class BackpackItem(object):
	_ITEM_IDS = {
			(0x00, 0x00):	"empty",
			# 0x01..0x05 cause crash
			(0x06, 0x00):	"brick_wall",
			(0x07, 0x00):	"electric_fence",
			(0x08, 0x00):	"computer",
			(0x09, 0x00):	"isolator",
			(0x0a, 0x00):	"gold_bar",
			(0x0b, 0x00):	"xmas_tree",
			(0x0c, 0x00):	"doppelganger_heart",
			(0x0d, 0x00):	"explosion",
			(0x0e, 0x00):	"red_button",
			(0x0f, 0x00):	"robot_switch",
			(0x10, 0x00):	"exit",
			(0x11, 0x00):	"question_mark",
			(0x12, 0x00):	"water_top_left",
			(0x13, 0x00):	"bomb",
			(0x14, 0x00):	"bank",
			(0x15, 0x00):	"key_generic_black (0)",
			(0x15, 0x01):	"key_yellow (1)",
			(0x15, 0x02):	"key_green (2)",
			(0x15, 0x03):	"key_gray (3)",
			(0x15, 0x04):	"key_violet (4)",
			(0x15, 0x05):	"key_darkred (5)",
			(0x15, 0x06):	"key_red (6)",
			(0x15, 0x07):	"key_orange (7)",
			(0x15, 0x08):	"key_brightgreen (8)",
			(0x15, 0x09):	"key_mintgreen (9)",
			(0x15, 0x0a):	"key_cyan (A)",
			(0x15, 0x0b):	"key_darkblue (B)",
			(0x15, 0x0c):	"key_blue (C)",
			(0x15, 0x0d):	"key_black_1 (D)",
			(0x15, 0x0e):	"key_darkgray (E)",
			(0x15, 0x0f):	"key_black_2 (F)",
			(0x16, 0x00):	"door_generic_black (0)",
			(0x16, 0x01):	"door_yellow (1)",
			(0x16, 0x02):	"door_green (2)",
			(0x16, 0x03):	"door_gray (3)",
			(0x16, 0x04):	"door_violet (4)",
			(0x16, 0x05):	"door_darkred (5)",
			(0x16, 0x06):	"door_red (6)",
			(0x16, 0x07):	"door_orange (7)",
			(0x16, 0x08):	"door_brightgreen (8)",
			(0x16, 0x09):	"door_mintgreen (9)",
			(0x16, 0x0a):	"door_cyan (A)",
			(0x16, 0x0b):	"door_darkblue (B)",
			(0x16, 0x0c):	"door_blue (C)",
			(0x16, 0x0d):	"door_black_1 (D)",
			(0x16, 0x0e):	"door_darkgray (E)",
			(0x16, 0x0f):	"door_black_2 (F)",
			(0x17, 0x00):	"blocked_exit",
			(0x18, 0x00):	"arrow_up",
			(0x19, 0x00):	"brick_wall",
			(0x1a, 0x00):	"me_puzzle_upper_left",
			(0x1b, 0x00):	"lamp_off",
			(0x1c, 0x00):	"skull_black",
			(0x1d, 0x00):	"magnet_red_green",
			(0x1e, 0x00):	"acid",
			(0x1f, 0x00):	"garlic",
			(0x20, 0x00):	"slingshot",
			(0x21, 0x00):	"ammo_1_shot",
			(0x21, 0x01):	"ammo_2_shot",
			(0x21, 0x02):	"ammo_3_shot",
			(0x21, 0x03):	"ammo_4_shot",
			(0x21, 0x04):	"ammo_5_shot",
			(0x21, 0x05):	"ammo_6_shot",
			(0x22, 0x00):	"electrode_left",
			(0x22, 0x01):	"electrode_right",
			(0x23, 0x00):	"electro_beam_horiz",
			(0x24, 0x00):	"exclamation_mark",
			(0x25, 0x00):	"letter",
			(0x26, 0x00):	"black_wall",
			(0x27, 0x00):	"thick_cable_left",
			(0x28, 0x00):	"blaumann",
			(0x29, 0x00):	"pen",
			(0x2a, 0x00):	"seed",
			(0x2b, 0x00):	"sichel",
			(0x2c, 0x00):	"haendler",
			(0x2d, 0x00):	"android",
			(0x2e, 0x00):	"platinum_bar",
			(0x2f, 0x00):	"point_field ?",
			(0x30, 0x00):	"android_egg",
			(0x31, 0x00):	"sand",
			(0x32, 0x00):	"arrow_field ?",
			(0x33, 0x00):	"1up",
			(0x34, 0x00):	"empty_square ?",
			(0x35, 0x00):	"sack ?",
			(0x36, 0x00):	"save_clock",
			(0x37, 0x00):	"worm_head",
			(0x38, 0x00):	"create_robot_field",
			(0x39, 0x00):	"slot_machine",
			(0x3a, 0x00):	"message_0",
			(0x3b, 0x00):	"book",
			(0x3c, 0x00):	"robot_brick_wall",
			(0x3d, 0x00):	"stairs",
			(0x3e, 0x00):	"magic_wand",
			(0x3f, 0x00):	"duplicator",
			(0x40, 0x00):	"thief",
			(0x41, 0x00):	"brick_interface_top",
			(0x42, 0x00):	"logic_AND",
			(0x43, 0x00):	"logic_lamp",
			(0x44, 0x00):	"diamond",
			(0x45, 0x00):	"???",
			(0x46, 0x00):	"pill",
			(0x47, 0x00):	"train_door ?",
			(0x48, 0x00):	"???",
			(0x49, 0x00):	"water",
			(0x4a, 0x00):	"???",
			(0x4b, 0x00):	"???",
			# All from 0x4c seem to be regarded as empty
			(0x7f, 0x00):	"teleporter",
	}
	_REV_ITEM_IDS = { y: x for (x, y) in _ITEM_IDS.items() }

	def __init__(self, data):
		self._data = data

	def __repr__(self):
		return str(self)

	@property
	def char(self):
		text = str(self)
		return {
			"empty":					"  ",
			"brick_wall":				"##",
			"black_wall":				"##",
			"exit":						"<-",
			"electric_fence":			"~~",
			"isolator":					"{}",
			"gold_bar":					"^ ",
			"arrow_up":					"->",
			"door_generic_black (0)":	".-",
			"letter":					"A ",
		}.get(text, text[:2])

	@property
	def is_empty(self):
		return (self._data[0] == 0x00) and (self._data[1] == 0x00)

	@classmethod
	def new_by_id(cls, main_id, sub_id):
		return cls(bytes([ main_id, sub_id ]))

	@classmethod
	def new_by_name(cls, name):
		if name not in cls._REV_ITEM_IDS:
			item_names = ", ".join(sorted(list(cls._REV_ITEM_IDS.keys())))
			raise Exception("'%s' is not a valid item name. Valid item names are %s." % (name, item_names))
		(main_id, sub_id) = cls._REV_ITEM_IDS[name]
		return cls(bytes([ main_id, sub_id ]))

	@property
	def data(self):
		return self._data

	def __str__(self):
		item_id = (self._data[0], self._data[1])
		if item_id in self._ITEM_IDS:
			return self._ITEM_IDS[item_id]
		else:
			return "Unknown<%02x %02x>" % (item_id[0], item_id[1])

class Room(object):
	_ROOM_WIDTH = 40
	_ROOM_HEIGHT = 29

	def __init__(self, room_id, data):
		self._room_id = room_id
		self._data = data
		self._offset = 0
		self._parse()

	def _room_layout(self, at_offset, count, block):
		cmd = self._data[at_offset]
		print("0x%x [%02x]: %d x %s" % (at_offset, cmd, count, block))
		self._room += [ block for i in range(count) ]

	def _subindex_layout(self, at_offset, count, subindex):
		cmd = self._data[at_offset]
		new_len = len(self._subindices) + count
		print("0x%x [%02x]: %d x 0x%x (then %d [%d, %d])" % (at_offset, cmd, count, subindex, new_len, new_len % self._ROOM_WIDTH, new_len // self._ROOM_WIDTH))
		self._subindices += [ subindex for i in range(count) ]

	def dump(self):
		print("Room ID 0x%x len %d (missing: %d)" % ((self._room_id, len(self._room), (self._ROOM_WIDTH * self._ROOM_HEIGHT) - len(self._room))))
		for i in range(0, len(self._room), self._ROOM_WIDTH):
#			print("".join(block.char for block in self._room[i : i + self._ROOM_WIDTH]))
			print("".join(block.char + "%-2x" % (self._subindices[i + j]) for (j, block) in enumerate(self._room[i : i + self._ROOM_WIDTH])))

	def _end_room(self):
		padding = self._ROOM_WIDTH - (len(self._room) % self._ROOM_WIDTH)
		self._room += " " * padding
		self._room += "*" * self._ROOM_WIDTH

	def _parse_room(self):
		self._room = [ ]
		while len(self._room) < (self._ROOM_WIDTH * self._ROOM_HEIGHT):
			cmd = self._data[self._offset]
			if cmd < 0x80:
				block = BackpackItem.new_by_id(cmd, 0)
				self._room_layout(self._offset, 1, block)
				self._offset += 1
			else:
				count = cmd - 0x80
				block_no = self._data[self._offset + 1]
				block = BackpackItem.new_by_id(block_no, 0)
				self._room_layout(self._offset, count, block)
				self._offset += 2

	def _parse_subindex_room(self):
		HexDump().dump(self._data[self._offset:])
		self._subindices = [ ]
		while len(self._subindices) < (self._ROOM_WIDTH * self._ROOM_HEIGHT):
			cmd = self._data[self._offset]
			if cmd < 0x80:
				self._subindex_layout(self._offset, 1, cmd)
				self._offset += 1
			elif cmd < 0xff:
				count = cmd - 0x80
				subindex = self._data[self._offset + 1]
				self._subindex_layout(self._offset, count, subindex)
				self._offset += 2
			else:
				count = self._data[self._offset + 1] - 0x8a
				subindex = self._data[self._offset + 2]
				self._subindex_layout(self._offset, count, subindex)
				self._offset += 3
		print("SUBIDx", len(self._subindices))

	def _parse(self):
		self._parse_room()
		self._parse_subindex_room()
#		self._parse_room()
#		print("REM", len(self._data) - self._offset)

class SceneData(object):
	def __init__(self, data, base_offset = 0):
		self._room = None
		self._data = data
		self._offset = 0
		self._base_offset = base_offset
		self._parse()

	def _parse_room_header(self):
		room_id = self._data[self._offset]
		length = self._data[self._offset + 2] | (self._data[self._offset + 3] << 8)
		return (room_id, length)

	def _parse(self):
		self._offset = 0
		room_cnt = 0
		while self._offset < len(self._data):
			(room_id, room_length) = self._parse_room_header()
			print("Room %d (ID 0x%d) at 0x%x length 0x%x" % (room_cnt, room_id, self._offset + self._base_offset, room_length))
			room_data = self._data[self._offset + 4 : self._offset + 4 + room_length]

			if (room_cnt == 1):
				HexDump().dump(room_data)
				room = Room(room_id, room_data)
				room.dump()
				print("=" * 150)
			self._offset += room_length + 2
			room_cnt += 1

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
		backpack_data = [ BackpackItem(backpack_data[i : i + self._BACKPACK_ITEM_SIZE]) for i in range(0, len(backpack_data), self._BACKPACK_ITEM_SIZE) ]
		return backpack_data

	def put_backpack(self, index, item):
		offset = self._OFFSETS["backpack"] + (index * self._BACKPACK_ITEM_SIZE)
		for i in range(self._BACKPACK_ITEM_SIZE):
			self._data[offset + i] = item.data[i]

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

