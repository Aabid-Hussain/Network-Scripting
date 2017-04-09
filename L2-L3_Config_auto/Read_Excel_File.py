# open Device_List.xlsx

import xlrd

def open_excel_file(workbook_name):
	#use xlrd.open_workbook(path/object) for opening excel sheet
	workbook = xlrd.open_workbook(workbook_name)
	#under excel, capture sheet 1
	worksheet = workbook.sheet_by_name('Sheet1')

	return worksheet


def main():
	'''
	Open "switch_list.xlsx" and display its data
	'''
	worksheet = open_excel_file("Device_List.xlsx")
	num_rows = worksheet.nrows - 1
	num_cells = worksheet.ncols - 1
	curr_row = -1
	while curr_row < num_rows:
		curr_row += 1
		row = worksheet.row(curr_row)
		print 'Row:', curr_row
		curr_cell = -1
		while curr_cell < num_cells:
			curr_cell += 1
			# Cell Types: 0=Empty, 1=Text, 2=Number, 3=Date, 4=Boolean, 5=Error, 6=Blank
			cell_type = worksheet.cell_type(curr_row, curr_cell)
			cell_value = worksheet.cell_value(curr_row, curr_cell)
			print '\t', cell_type, ':', cell_value
			
			
if __name__ == "__main__":
	main()