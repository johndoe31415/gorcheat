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

from BackpackItem import BackpackItem
from HexDump import HexDump

class Room(object):
	_ROOM_WIDTH = 40
	_ROOM_HEIGHT = 29

	def __init__(self, room_id, data, base_offset = 0):
		self._room_id = room_id
		self._data = data
		self._base_offset = base_offset
		self._offset = 0
		self._room = None
		self._main_ids = [ ]
		self._sub_ids = [ ]
		self._parse()

	def _append_roomdata(self, array, count, block_id):
		at_offset = self._base_offset + self._offset
		cmd = self._data[self._offset]
		new_len = len(array) + count
#		if self._room_id == 0x3f:
#			print("0x%x [%02x]: %d x 0x%02x (after adding %d [%d, %d])" % (at_offset, cmd, count, block_id, new_len, new_len % self._ROOM_WIDTH, new_len // self._ROOM_WIDTH))
		array += [ block_id for i in range(count) ]

	def dump(self):
		print("Room ID 0x%x (%d blocks)" % ((self._room_id, len(self._room))))
		for i in range(0, len(self._room), self._ROOM_WIDTH):
			print("".join(block.char for block in self._room[i : i + self._ROOM_WIDTH]))

	def _parse_main_ids(self):
		while len(self._main_ids) < (self._ROOM_WIDTH * self._ROOM_HEIGHT):
			cmd = self._data[self._offset]
			if cmd < 0x80:
				self._append_roomdata(self._main_ids, 1, cmd)
				self._offset += 1
			else:
				count = cmd - 0x80
				block_id = self._data[self._offset + 1]
				self._append_roomdata(self._main_ids, count, block_id)
				self._offset += 2
		if len(self._main_ids) != self._ROOM_WIDTH * self._ROOM_HEIGHT:
			raise Exception("Main IDs of room 0x%x have length %d (expected %d x %d = %d). Difference of %+d elements." % (self._room_id, len(self._main_ids), self._ROOM_WIDTH, self._ROOM_HEIGHT, self._ROOM_WIDTH * self._ROOM_HEIGHT, len(self._main_ids) - (self._ROOM_WIDTH * self._ROOM_HEIGHT)))

	def _parse_sub_ids(self):
#		HexDump().dump(self._data[self._offset:])
		while len(self._sub_ids) < (self._ROOM_WIDTH * self._ROOM_HEIGHT):
			try:
				cmd = self._data[self._offset]
			except IndexError:
				break
			if cmd < 0x80:
				self._append_roomdata(self._sub_ids, 1, cmd)
				self._offset += 1
			elif cmd < 0xff:
				count = cmd - 0x80
				if count == 0:
					# Odd. Why would this be different to 0x81?
					count = 1
				sub_id = self._data[self._offset + 1]
				self._append_roomdata(self._sub_ids, count, sub_id)
				self._offset += 2
			else:
				count = 127
				sub_id = 0			# Is this correct?
				self._append_roomdata(self._sub_ids, count, sub_id)
				self._offset += 1
		if len(self._sub_ids) != self._ROOM_WIDTH * self._ROOM_HEIGHT:
			raise Exception("Sub IDs of room 0x%x have length %d (expected %d x %d = %d). Difference of %+d elements." % (self._room_id, len(self._sub_ids), self._ROOM_WIDTH, self._ROOM_HEIGHT, self._ROOM_WIDTH * self._ROOM_HEIGHT, len(self._sub_ids) - (self._ROOM_WIDTH * self._ROOM_HEIGHT)))

	def _parse_other(self):
		data = self._data[self._offset:]
		offset = 0
		for offset in range(0, len(data), 11):
			rob_data = data[offset : offset + 11]
			HexDump().dump(rob_data)
			if (len(rob_data) == 11) and (rob_data[5] == 0x81):
				col1 = rob_data[3]
				col2 = rob_data[4]
				rtype = rob_data[6]
				rx = rob_data[7]
				ry = rob_data[8]
				speed = rob_data[9]
				speed_percent = 100 * (255 - speed) / 255
				invisibility = rob_data[10]		# ?? usually 0
				print("Robot type %d at %d, %d Color %d, %d, speed %.0f%%, invisibility %d" % (rtype, rx, ry, col1, col2, speed_percent, invisibility))
			elif rob_data == bytes.fromhex("ff ff ff ff ff ff ff ff ff 91 00"):
				# No idea what this is. Header?
				pass
			elif len(rob_data) == 11:
				print("Unknown robdata: %s" % (rob_data.hex()))
			elif len(rob_data) == 2:
				print("Previous room: 0x%x" % (rob_data[0]))

	def _create_room(self):
		self._room = [ BackpackItem(main_id, sub_id) for (main_id, sub_id) in zip(self._main_ids, self._sub_ids) ]

	def _parse(self):
		self._parse_main_ids()
		self._parse_sub_ids()
		self._parse_other()
		self._create_room()

if __name__ == "__main__":
	roomdata = bytes.fromhex("82 06") + bytes([ 0x06 ] * (1160 - 2))
	roomdata += bytes([ 0x00 ] * 1160)
	roomdata += bytes([ 0xff ] * 24)
	r = Room(0xab, roomdata)
	r.dump()
