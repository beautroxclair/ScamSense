import csv


with open("tokens.csv", "r") as dirtyTokensCSV:
	csv_reader = csv.reader(dirtyTokensCSV)
	with open("tokensTransformed.csv","w") as cleanTokensCSV:
		writer = csv.writer(cleanTokensCSV)
		writer.writerow(['Token_ID', 'Type', 'Symbol'])
		for row in csv_reader:
			if row[2] != 'Symbol' and row[2] != 'Cake-LP' and row[2] is not None and row[2] != "":
				writer.writerow(row)








