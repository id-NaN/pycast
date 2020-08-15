map_raw = """\
# # # # # # # # # # # # # # # #
# - - - - - - - - - - - - - - #
# - # - - # - - - - - - - - - #
# - - - - - - - - - - - - - - #
# - - - - - - - - - - - - - - #
# - # - - # - - - - - - - - - #
# - - - - - - - - - - - - - - #
# - - - - - - - - - - - - - - #
# - - - - - - - - - - - - - - #
# - - - - - - - - # - # # # # #
# - # # # # - - - # - # - # - #
# - - - - # - - - # - # - # - #
# - - - - # - - - # - - - - - #
# - # # # # - - - # - # # # - #
# - - - - - - - - # - - - # - #
# # # # # # # # # # # # # # # #"""



def load_map():
	game_map = []
	global map_raw
	for row in map_raw.split("\n"):
		final_row = []
		for tile in row.split(" "):
			final_row.append(tile == "#")
		game_map.append(final_row)
	return game_map