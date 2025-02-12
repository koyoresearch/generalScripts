#!/bin/sh
#usage: dbSearchString.sh "text to search for" database.db

searchFor="$1"
dbListFilename="$2"
dbList=$(cat $dbListFilename)

for db in $dbList
do
	echo "\nFile: $db-----"
	tables=$(sqlite3 "$db" .tables)
	echo "Table list: $tables"

	for table in $tables
	do
	    echo "\n---$table  -----"
	    tableContents=$(sqlite3 -line "$db" ".mode list '$separator'" "select * from $table")
	    searchResults=$(echo $tableContents | grep "$searchFor")

	    if [ -z "$searchResults" ]; then
	      echo "Variable is empty"
	    else
	      echo "searchResults=$searchResults"
	      echo "$db,$table: searchResults=$searchResults" >> sqliteSearchResults.txt
	    fi
	done
done