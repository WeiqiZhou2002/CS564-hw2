rm -f *.dat
rm -f *.db
python skeleton_parser.py items-*.json
sort -u category.dat -o category.dat
sort -u user.dat -o user.dat
sort -u bid.dat -o bid.dat
sort -u item.dat -o item.dat
sqlite3 ebayData.db < create.sql
sqlite3 ebayData.db < load.txt