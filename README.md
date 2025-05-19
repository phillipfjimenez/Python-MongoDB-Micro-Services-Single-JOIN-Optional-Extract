# Python + MongoDB + Single JOIN + Optional Extract
 Developed/tested using Python v3.11.9 & UP for MongoDB Structure which is developed as Micro Services.  
 MongoDB aggregate does not work with Cross Functional Database Collections.  
## Installation and Setup
 1. Install Python
 2. Install packages using **command prompt**: pip install argparse json pandas pymongo
 3. Download **mongodb_single_join.py**
 4. Open **mongodb_single_join.py** using Editor
 5. Locate and edit line: **35** `client = MongoClient("mongodb+srv://<USERNAME>:<PASSWORD>@<HOST>")`
 6. Replace **&lt;USERNAME&gt;**, **&lt;PASSWORD&gt;**, and **&lt;HOST&gt;**

### Two style of Query:
 1. Query with Web Minifier/Escape Quotes.
 2. Manual
    - Keys and Values inside Double Quotes with Single Quotes.
    - You have to manually remove spaces and break lines.(can use editor.

## Style 1: Initial Build of Query - Query with Web Minifier/Escape Quotes
 1. Creating Query in JSON Format. **Example:**  
```
{
	"SELECT_PRIMARY": ["",""],
	"SELECT_FOREIGN": ["",""],
	"FROM": "",
	"JOIN": "",
	"ON": ["", ""],
	"WHERE_PRIMARY": [{"":""},{"":[]}],
	"WHERE_FOREIGN": [{"":""},{"":[]}
}
```

 2. **“SELECT_PRIMARY“** and **“SELECT_FOREIGN“** will be use for the fields to be selected from joining two table.
 3. **“FROM“** and **“JOIN“** format must be like **“DATABASE_NAME.collection_name“**.
 4. **“ON“** requires two parameter in array which will be use for joining the two table.- Two Parameter in **“ON”** field is required to be exist in **“SELECT_PRIMARY“** and **“SELECT_FOREIGN“** field.
 5. **“WHERE_PRIMARY“** and **“WHERE_FOREIGN“. Examples:**  
 **Example 1**. WHERE field=”value”  
```
"WHERE_PRIMARY": [{"field":"value"}],
"WHERE_FOREIGN": [{"field":"value"}],
```

**Example 2**. WHERE field_1=”value_1” AND field_2=”value_2” AND field_3=”value3”  
```
"WHERE_PRIMARY": [{"field_1":"value_1"},{"field_2":"value_2"},{"field_3":"value_3"}],
"WHERE_FOREIGN": [{"field_1":"value_1"},{"field_2":"value_2"},{"field_3":"value_3"}],
```

**Example 3**. WHERE field IN (“value_1“,“value_2“,“value_3“)  
```
"WHERE_PRIMARY": [{"field":["value_1","value_2","value_3"]}],
"WHERE_FOREIGN": [{"field":["value_1","value_2","value_3"]}],
```

6. **Example Query Expected Format:**  
```
{
 	"SELECT_PRIMARY": ["primary_field_1","primary_field_2","primary_field_3", "match_primary_field_id"],
 	"SELECT_FOREIGN": ["match_foreign_field_id","foreign_field_1","foreign_field_2","foreign_field_3"],
 	"FROM": "DATABASE_NAME_1.collection_1",
 	"JOIN": "DATABASE_NAME_2.collection_2",
 	"ON": ["match_primary_field_id", "match_foreign_field_id"],
 	"WHERE_PRIMARY": [{"primary_field_1":"primary_value_1"},{"primary_field_2":["primary_value_2","primary_value_3"]}],
 	"WHERE_FOREIGN": [{"foreign_field_2":["foreign_value_2","foreign_value_3"]},{"foreign_field_1":"foreign_value_1"}]
}
```

 7. Making our Query Compatible/Acceptable with our **mongodb_single_join.py**. script program.
-  Minify the Query using https://codebeautify.org/jsonminifier. **Minified Query Format**:  
```
{"SELECT_PRIMARY":["primary_field_1","primary_field_2","primary_field_3","match_primary_field_id"],"SELECT_FOREIGN":["match_foreign_field_id","foreign_field_1","foreign_field_2","foreign_field_3"],"FROM":"DATABASE_NAME_1.collection_1","JOIN":"DATABASE_NAME_2.collection_2","ON":["match_primary_field_id","match_foreign_field_id"],"WHERE_PRIMARY":[{"primary_field_1":"primary_value_1"},{"primary_field_2":["primary_value_2","primary_value_3"]}],"WHERE_FOREIGN":[{"foreign_field_2":["foreign_value_2","foreign_value_3"]},{"foreign_field_1":"foreign_value_1"}]}
```
-  Escape Quotes of Minified Output using https://jsonformatter.org/json-escape. **Escaped Query Format**  
```
{\"SELECT_PRIMARY\":[\"primary_field_1\",\"primary_field_2\",\"primary_field_3\",\"match_primary_field_id\"],\"SELECT_FOREIGN\":[\"match_foreign_field_id\",\"foreign_field_1\",\"foreign_field_2\",\"foreign_field_3\"],\"FROM\":\"DATABASE_NAME_1.collection_1\",\"JOIN\":\"DATABASE_NAME_2.collection_2\",\"ON\":[\"match_primary_field_id\",\"match_foreign_field_id\"],\"WHERE_PRIMARY\":[{\"primary_field_1\":\"primary_value_1\"},{\"primary_field_2\":[\"primary_value_2\",\"primary_value_3\"]}],\"WHERE_FOREIGN\":[{\"foreign_field_2\":[\"foreign_value_2\",\"foreign_value_3\"]},{\"foreign_field_1\":\"foreign_value_1\"}]}
```

 8. Once familiar with the Escaped Quotes Output **\”Key\”:\”Value\”**, you can manually edit/update the query object. **Done**

##  Style 2: Build of Query - Manual(Not fully tested yet. :D)
 1. You can use <ins>**Style 1, Step 2 - 6**</ins> for the **guide** but **Keys** and **Values** will be inside **Double Quoteswith Single Quotes**.
```
{
	'"SELECT_PRIMARY"':['"primary_field_1"','"primary_field_2"','"primary_field_3"','"match_primary_field_id"'],
	'"SELECT_FOREIGN"':['"match_foreign_field_id"','"foreign_field_1"','"foreign_field_2"','"foreign_field_3"'],
	'"FROM"':'"DATABASE_NAME_1.collection_1"','"JOIN"':'"DATABASE_NAME_2.collection_2"',
	'"ON"':['"match_primary_field_id"','"match_foreign_field_id"'],
	'"WHERE_PRIMARY"':[{'"primary_field_1"':'"primary_value_1"'},{'"primary_field_2"':['"primary_value_2"','"primary_value_3"']}],
	'"WHERE_FOREIGN"':[{'"foreign_field_2"':['"foreign_value_2"','"foreign_value_3"']},{'"foreign_field_1"':'"foreign_value_1"'}]
}
```
2. Remove Spaces and Break Lines.(You can use any editor)  
```
{'"SELECT_PRIMARY"':['"primary_field_1"','"primary_field_2"','"primary_field_3"','"match_primary_field_id"'],'"SELECT_FOREIGN"':['"match_foreign_field_id"','"foreign_field_1"','"foreign_field_2"','"foreign_field_3"'],'"FROM"':'"DATABASE_NAME_1.collection_1"','"JOIN"':'"DATABASE_NAME_2.collection_2"','"ON"':['"match_primary_field_id"','"match_foreign_field_id"'],'"WHERE_PRIMARY"':[{'"primary_field_1"':'"primary_value_1"'},{'"primary_field_2"':['"primary_value_2"','"primary_value_3"']}],'"WHERE_FOREIGN"':[{'"foreign_field_2"':['"foreign_value_2"','"foreign_value_3"']},{'"foreign_field_1"':'"foreign_value_1"'}]}
```

**Done**  

##  Running the Program
 1. Locate the **mongodb_single_join.py**. script program. **Example:**
``` cd C:\directory_of_mongodb_single_join```
 2. Running the mongodb_single_join.py. script program requires 3 parameters. **Example** without 3 params:  
    ![alt text](https://github.com/phillipfjimenez/readme-images/blob/main/python-mongodb-singlejoin-no-param.png)  
 4. The script can only be run by providing the Correct Escaped Quotes Output or Double Quotes with Single Quotes and with null for the next two parameter. **Example:**  
    ![alt text](https://github.com/phillipfjimenez/readme-images/blob/main/python-mongodb-singlejoin-paramquery.png)  
 5. The next two parameter which is null from the previous example is the condition to **sort** the **output** and for the **filename** if you want it to be extract. Example:  
    ![alt text](https://github.com/phillipfjimenez/readme-images/blob/main/python-mongodb-singlejoin-paramquery-with-sort-andor-extract.png)  
