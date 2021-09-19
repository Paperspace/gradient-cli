import pydoc
import terminaltables
from gradient.cliutils import get_terminal_lines


def print_table(data):
	ascii_table = terminaltables.AsciiTable(data)
	table_string = ascii_table.table

	if len(table_string.splitlines()) > get_terminal_lines():
		pydoc.pager(table_string)
	else:
		print(table_string)

def formatted_graphql(data):
	output = {}

	for key in data.keys():
		if type(data[key]) is dict and 'nodes' in data[key]:
			output[key] = []
			for node in data[key]['nodes']:
				output[key].append(formatted_graphql(node))
		elif type(data[key]) is dict:
			output[key] = formatted_graphql(data[key])
		else:
			output[key] = data[key]

	return output