rm -f *.dat
rm -f *.db
python skeleton_parser.py items-*.json
sort -u Category.dat -o category.dat
sort -u User.dat -o user.dat
sort -u Bid.dat -o bid.dat
sort -u Item.dat -o item.dat
sqlite3 ebayData.db < create.sql
sqlite3 ebayData.db < load.txt
