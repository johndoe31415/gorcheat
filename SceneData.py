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

from Room import Room

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
			print("Parsing room %d (ID 0x%x) at 0x%x length 0x%x" % (room_cnt, room_id, self._base_offset + self._offset, room_length))
			room_data = self._data[self._offset + 4 : self._offset + 4 + room_length]

			room = Room(room_id, room_data, base_offset = self._base_offset + self._offset)
			room.dump()

			self._offset += room_length + 2
			room_cnt += 1
