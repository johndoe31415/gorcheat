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

import enum

class ItemClass(object):
	def __init__(self, main_id, class_name, sub_id_types = None):
		self._main_id = main_id
		self._class_name = class_name
		self._sub_id_types = sub_id_types

	@property
	def main_id(self):
		return self._main_id

	@property
	def class_name(self):
		return self._class_name

	@property
	def sub_names(self):
		if self._sub_id_types is None:
			return { 0: self._class_name }.items()
		else:
			return self._sub_id_types.items()

	def get_name(self, sub_id):
		if self._sub_id_types is None:
			return self._class_name
		else:
			return self._sub_id_types.get(sub_id, self._class_name)

class BackpackItem(object):
	_ITEM_CLASSES = { iclass.main_id : iclass for iclass in (
		ItemClass(0x00, "empty"),
		# 0x01..0x05 cause crash
		ItemClass(0x06, "brick_wall", sub_id_types = {
			0x00:	"full",
			0x01:	"tri_tl",
			0x02:	"tri_tr",
			0x03:	"tri_br",
			0x04:	"tri_bl",
			0x05:	"full_solid",
		}),
		ItemClass(0x07, "electric_fence"),
		ItemClass(0x08, "computer"),
		ItemClass(0x09, "isolator"),
		ItemClass(0x0a, "gold_bar"),
		ItemClass(0x0b, "xmas_tree"),
		ItemClass(0x0c, "doppelganger_heart"),
		ItemClass(0x0d, "explosion"),
		ItemClass(0x0e, "red_button"),
		ItemClass(0x0f, "robot_switch"),
		ItemClass(0x10, "exit"),
		ItemClass(0x11, "question_mark"),
		ItemClass(0x12, "water_top_left"),
		ItemClass(0x13, "bomb"),
		ItemClass(0x14, "bank"),
		ItemClass(0x15, "key", sub_id_types = {
			0x00:	"key_black_0 (0)",
			0x01:	"key_yellow (1)",
			0x02:	"key_green (2)",
			0x03:	"key_gray (3)",
			0x04:	"key_violet (4)",
			0x05:	"key_darkred (5)",
			0x06:	"key_red (6)",
			0x07:	"key_orange (7)",
			0x08:	"key_brightgreen (8)",
			0x09:	"key_mintgreen (9)",
			0x0a:	"key_cyan (A)",
			0x0b:	"key_darkblue (B)",
			0x0c:	"key_blue (C)",
			0x0d:	"key_black_1 (D)",
			0x0e:	"key_darkgray (E)",
			0x0f:	"key_black_2 (F)",
		}),
		ItemClass(0x16, "door", sub_id_types = {
			0x00:	"door_black_0 (0)",
			0x01:	"door_yellow (1)",
			0x02:	"door_green (2)",
			0x03:	"door_gray (3)",
			0x04:	"door_violet (4)",
			0x05:	"door_darkred (5)",
			0x06:	"door_red (6)",
			0x07:	"door_orange (7)",
			0x08:	"door_brightgreen (8)",
			0x09:	"door_mintgreen (9)",
			0x0a:	"door_cyan (A)",
			0x0b:	"door_darkblue (B)",
			0x0c:	"door_blue (C)",
			0x0d:	"door_black_1 (D)",
			0x0e:	"door_darkgray (E)",
			0x0f:	"door_black_2 (F)",
		}),
		ItemClass(0x17, "blocked_exit"),
		ItemClass(0x18, "arrow", sub_id_types = {
			0x00:	"arrow_up",
			0x01:	"arrow_right",
			0x02:	"arrow_down",
			0x03:	"arrow_left",
		}),
		ItemClass(0x19, "brick_wall_acid"),
		ItemClass(0x1a, "me_puzzle_upper_left"),
		ItemClass(0x1b, "lamp_off"),
		ItemClass(0x1c, "skull_black"),
		ItemClass(0x1d, "magnet_red_green"),
		ItemClass(0x1e, "acid"),
		ItemClass(0x1f, "garlic"),
		ItemClass(0x20, "slingshot"),
		ItemClass(0x21, "ammo", sub_id_types = {
			0x00:	"ammo_1_shot",
			0x01:	"ammo_2_shot",
			0x02:	"ammo_3_shot",
			0x03:	"ammo_4_shot",
			0x04:	"ammo_5_shot",
			0x05:	"ammo_6_shot",
		}),
		ItemClass(0x22, "electrode", sub_id_types = {
			0x00:	"electrode_left",
			0x01:	"electrode_right",
		}),
		ItemClass(0x23, "electro_beam", sub_id_types = {
			0x00:	"electro_beam_horiz",
		}),
		ItemClass(0x24, "exclamation_mark"),
		ItemClass(0x25, "letter", sub_id_types = {
			0x41:	"letter_A",
			0x42:	"letter_B",
			0x43:	"letter_C",
			0x44:	"letter_D",
			0x45:	"letter_E",
			0x46:	"letter_F",
			0x47:	"letter_G",
			0x48:	"letter_H",
			0x49:	"letter_I",
			0x4a:	"letter_J",
			0x4b:	"letter_K",
			0x4c:	"letter_L",
			0x4d:	"letter_M",
			0x4e:	"letter_N",
			0x4f:	"letter_O",
			0x50:	"letter_P",
			0x51:	"letter_Q",
			0x52:	"letter_R",
			0x53:	"letter_S",
			0x54:	"letter_T",
			0x55:	"letter_U",
			0x56:	"letter_V",
			0x57:	"letter_W",
			0x58:	"letter_X",
			0x59:	"letter_Y",
			0x5a:	"letter_Z",
		}),
		ItemClass(0x26, "black_wall"),
		ItemClass(0x27, "thick_cable", sub_id_types = {
			0x00:	"tick_cable_left",
		}),
		ItemClass(0x28, "blaumann"),
		ItemClass(0x29, "pen"),
		ItemClass(0x2a, "seed"),
		ItemClass(0x2b, "sichel"),
		ItemClass(0x2c, "haendler"),
		ItemClass(0x2d, "android"),
		ItemClass(0x2e, "platinum_bar"),
		ItemClass(0x2f, "point_field"),
		ItemClass(0x30, "android_egg"),
		ItemClass(0x31, "sand"),
		ItemClass(0x32, "arrow_field"),
		ItemClass(0x33, "1up"),
		ItemClass(0x34, "empty_square"),
		ItemClass(0x35, "sack"),
		ItemClass(0x36, "save_clock"),
		ItemClass(0x37, "worm_head"),
		ItemClass(0x38, "create_robot_field"),
		ItemClass(0x39, "slot_machine"),
		ItemClass(0x3a, "message_0"),
		ItemClass(0x3b, "book"),
		ItemClass(0x3c, "robot_brick_wall"),
		ItemClass(0x3d, "stairs"),
		ItemClass(0x3e, "magic_wand"),
		ItemClass(0x3f, "duplicator"),
		ItemClass(0x40, "thief"),
		ItemClass(0x41, "brick_interface", sub_id_types = {
			0x00:	"brick_interface_top",
		}),
		ItemClass(0x42, "logic_AND"),
		ItemClass(0x43, "logic_lamp"),
		ItemClass(0x44, "diamond"),
		ItemClass(0x45, "???"),
		ItemClass(0x46, "pill"),
		ItemClass(0x47, "train_door"),
		ItemClass(0x48, "???"),
		ItemClass(0x49, "water"),
		ItemClass(0x4a, "???"),
		ItemClass(0x4b, "???"),
		ItemClass(0x7f, "teleporter"),
	)}
	_REV_ITEM_IDS = { sub_name: (iclass, sub_id) for iclass in _ITEM_CLASSES.values() for (sub_id, sub_name) in iclass.sub_names }

	_MAIN_CLASS_TRANSCRIPTS = {
		"empty":				"  ",
		"black_wall":			"■ ",
		"exit":					"⇋ ",
		"electric_fence":		"⌁ ",
		"isolator":				"▥ ",
		"gold_bar":				"▭ ",
#		"arrow":				"->",
		"door":					"🚪 ",
		"ammo":					"◦ ",
		"brick_wall_acid":		"■ ",
		"bank":					"💰 ",
	}
	_SUB_CLASS_TRANSCRIPTS = {
		"brick_wall": {
#			"full":			"■■",
			"full":			"■ ",
			"full_solid":	"■ ",
			"tri_tl":		"◤ ",
			"tri_tr":		"◥ ",
			"tri_bl":		"◣ ",
			"tri_br":		"◢ ",
		},
		"arrow": {
			"arrow_up":		"↑ ",
			"arrow_down":	"↓ ",
			"arrow_left":	"← ",
			"arrow_right":	"→ ",
		},
		"letter": {
			"letter_A":		"A ",
			"letter_B":		"B ",
			"letter_C":		"C ",
			"letter_D":		"D ",
			"letter_E":		"E ",
			"letter_F":		"F ",
			"letter_G":		"G ",
			"letter_H":		"H ",
			"letter_I":		"I ",
			"letter_J":		"J ",
			"letter_K":		"K ",
			"letter_L":		"L ",
			"letter_M":		"M ",
			"letter_N":		"N ",
			"letter_O":		"O ",
			"letter_P":		"P ",
			"letter_Q":		"Q ",
			"letter_R":		"R ",
			"letter_S":		"S ",
			"letter_T":		"T ",
			"letter_U":		"U ",
			"letter_V":		"V ",
			"letter_W":		"W ",
			"letter_X":		"X ",
			"letter_Y":		"Y ",
			"letter_Z":		"Z ",
		},
	}

	def __init__(self, main_id, sub_id):
		self._main_id = main_id
		self._sub_id = sub_id

	def __repr__(self):
		return str(self)

	@property
	def char(self):
		if self.iclass is not None:
			class_name = self.iclass.class_name
			if class_name in self._MAIN_CLASS_TRANSCRIPTS:
				return self._MAIN_CLASS_TRANSCRIPTS[class_name]
			elif class_name in self._SUB_CLASS_TRANSCRIPTS:
				return self._SUB_CLASS_TRANSCRIPTS[class_name].get(self.iclass.get_name(self.sub_id), "%02x%02x" % (self.main_id, self.sub_id))
		return "??"


	@property
	def iclass(self):
		return self._ITEM_CLASSES.get(self.main_id)

	@property
	def main_id(self):
		return self._main_id

	@property
	def sub_id(self):
		return self._sub_id

	@property
	def is_empty(self):
		return self.main_id == 0

	@classmethod
	def new_by_name(cls, name):
		if name not in cls._REV_ITEM_IDS:
			item_names = ", ".join(sorted(list(cls._REV_ITEM_IDS.keys())))
			raise Exception("'%s' is not a valid item name. Valid item names are %s." % (name, item_names))
		(iclass, sub_id) = cls._REV_ITEM_IDS[name]
		return cls(iclass.main_id, sub_id)

	def __str__(self):
		iclass = self._ITEM_CLASSES.get(self.main_id)
		if iclass is not None:
			return iclass.get_name(self.sub_id)
		else:
			return "Unknown<%02x %02x>" % (self.main_id, self.sub_id)

