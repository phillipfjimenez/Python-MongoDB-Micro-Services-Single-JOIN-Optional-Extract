import argparse
import json
import pandas as pd
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

def main():

	parser = argparse.ArgumentParser(description="Process some parameters.")
	parser.add_argument('query', type=str, help='SQL Query.')
	parser.add_argument('sorter', type=str, help='SQL Query Sort.')
	parser.add_argument('extract_filename', type=str, help='SQL Query Extract Filename.')

	args = parser.parse_args()
	valid_query = validate_query(args)

	if args.sorter != "null":
		if json.loads(args.sorter)[list(json.loads(args.sorter).keys())[0]] == 0:
			exit("$sort key ordering must be 1 (for ascending) or -1 (for descending)")

	errorONprimary = "true"
	errorONforeign = "true"
	for checkONprimary in valid_query["ON"]:
		if checkONprimary in valid_query["SELECT_PRIMARY"] and errorONprimary == "true":
			errorONprimary = "false"

	for checkONforeign in valid_query["ON"]:
		if checkONforeign in valid_query["SELECT_FOREIGN"] and errorONforeign == "true":
			errorONforeign = "false"

	if errorONprimary == "true" or errorONforeign == "true":
		exit("Error Parameter: ON please make sure parameter in ON exist in SELECT_PRIMARY and/or SELECT_FOREIGN.")

	try:
		client = MongoClient("mongodb+srv://<USERNAME>:<PASSWORD>@<HOST>")

		build_select_primary = {'_id': 0}
		for select_primary in valid_query["SELECT_PRIMARY"]:
			build_select_primary[select_primary] = 1

		build_select_foreign = {'_id': 0}
		for select_foreign in valid_query["SELECT_FOREIGN"]:
			build_select_foreign[select_foreign] = 1

		build_where_primary = {}
		if len(valid_query["WHERE_PRIMARY"]) > 0:
			for where_primary in valid_query["WHERE_PRIMARY"]:
				if type(where_primary[list(where_primary.keys())[0]]) not in (tuple, list):
					build_where_primary[list(where_primary.keys())[0]] = where_primary[list(where_primary.keys())[0]]
				else:
					build_where_primary[list(where_primary.keys())[0]] = { '$in': where_primary[list(where_primary.keys())[0]] }

		build_where_foreign = {}
		if len(valid_query["WHERE_FOREIGN"]) > 0:
			for where_foreign in valid_query["WHERE_FOREIGN"]:
				if type(where_foreign[list(where_foreign.keys())[0]]) not in (tuple, list):
					build_where_foreign[list(where_foreign.keys())[0]] = where_foreign[list(where_foreign.keys())[0]]
				else:
					build_where_foreign[list(where_foreign.keys())[0]] = { '$in': where_foreign[list(where_foreign.keys())[0]] }

		from_array = valid_query["FROM"].split(".")
		join_array = valid_query["JOIN"].split(".")
		if len(from_array) != 2:
			exit("Invalid Query FROM parameter.")
		if len(join_array) != 2:
			exit("Invalid Query JOIN parameter.")
		if type(valid_query["SELECT_PRIMARY"]) not in (tuple, list):
			exit("Invalid Query SELECT_PRIMARY parameter.")
		if type(valid_query["WHERE_PRIMARY"]) not in (tuple, list):
			exit("Invalid Query WHERE_PRIMARY parameter.")
		if type(valid_query["SELECT_FOREIGN"]) not in (tuple, list):
			exit("Invalid Query SELECT_FOREIGN parameter.")
		if type(valid_query["WHERE_FOREIGN"]) not in (tuple, list):
			exit("Invalid Query WHERE_FOREIGN parameter.")

		primary_query_builder = []
		if len(build_where_primary) > 0:
			primary_query_builder.append({ "$match": build_where_primary })

		if len(build_select_primary) > 0:
			primary_query_builder.append({ "$project": build_select_primary })

		query_from_results = []
		if len(primary_query_builder) > 0:
			from_db_query = from_array[0]
			from_db = client[from_db_query]
			from_collection_db_query = from_array[1]
			from_collection = from_db[from_collection_db_query]
			query_from = from_collection.aggregate(primary_query_builder)
			for results in query_from:
				query_from_results.append(results)

		foreign_query_builder = []
		if len(build_where_foreign) > 0:
			foreign_query_builder.append({ "$match": build_where_foreign })

		if len(build_select_foreign) > 0:
			foreign_query_builder.append({ "$project": build_select_foreign })

		query_join_results = []
		if len(foreign_query_builder) > 0:
			join_db_query = join_array[0]
			join_db = client[join_db_query]
			join_collection_db_query = join_array[1]
			join_collection = join_db[join_collection_db_query]
			query_join = join_collection.aggregate(foreign_query_builder)
			for results in query_join:
				query_join_results.append(results)

		# processing results
		if len(query_from_results) == 0 and len(query_join_results) == 0:
			exit("Query Results: Failed to join collections: Please fix your query.")
		else:
			result_builder = dict()
			output = []
			if len(query_from_results) > 0 or len(query_from_results) >= len(query_join_results):
				for from_results in query_from_results:
					for join_results in query_join_results:
						if valid_query["ON"][0] in from_results and valid_query["ON"][1] in join_results and from_results[valid_query["ON"][0]] == join_results[valid_query["ON"][1]]:
							result_builder.update(from_results)
							result_builder.update(join_results)
							output.append(result_builder)
							result_builder = dict()
			else:
				for join_results in query_join_results:
					for join_results in query_join_results:
						if valid_query["ON"][0] in join_results and valid_query["ON"][1] in from_results and join_results[valid_query["ON"][0]] == from_results[valid_query["ON"][1]]:
							result_builder.update(join_results)
							result_builder.update(from_results)
							output.append(result_builder)
							result_builder = dict()

		if args.sorter != "null":
			if json.loads(args.sorter)[list(json.loads(args.sorter).keys())[0]] < 0:
				output = sorted(output, key=lambda output:output[list(json.loads(args.sorter).keys())[0]], reverse=True)

		if args.extract_filename == "null":
			if len(output) == 0:
				print("No results found. Please confirm your Query.")
			else:
				print("Results:")
				print(output)
		else:
			extract_file = pd.DataFrame(output)
			extract_file.to_excel(args.extract_filename + ".xlsx", index=False)
			print("Extraction completed.")

		client.close()
	except ConnectionFailure:
		exit("ConnectionFailure: Failed to Connect to MongoDB.")

def validate_query(args):
	query = args.query.replace("'", '"')

	try:
		query = json.loads(query)

		if 'SELECT_PRIMARY' not in query or query["SELECT_PRIMARY"] == "":
			exit("Missing parameter or value: SELECT_PRIMARY")
		if 'SELECT_FOREIGN' not in query or query["SELECT_FOREIGN"] == "":
			exit("Missing parameter or value: SELECT_FOREIGN")
		if 'FROM' not in query or query["FROM"] == "":
			exit("Missing parameter or value: FROM")
		if 'JOIN' not in query or query["JOIN"] == "":
			exit("Missing parameter or value: JOIN")
		if 'ON' not in query or query["ON"] == "":
			exit("Missing parameter: ON")
		if len(query["ON"]) != 2:
			exit("Parameter: ON required 2 parameter only.")
		if 'WHERE_PRIMARY' not in query or query["WHERE_PRIMARY"] == "":
			exit("Missing parameter or value: WHERE_PRIMARY")
		if 'WHERE_FOREIGN' not in query or query["WHERE_FOREIGN"] == "":
			exit("Missing parameter or value: WHERE_FOREIGN")

		return query

	except ValueError as e:
		exit("Invalid Query Parameters.");

if __name__ == '__main__':
    main()
