modal volume delete odds-data
modal volume create odds-data
mkdir first_basket
cd first_basket
touch dummy
cd ..
modal volume put odds-data first_basket first_basket
rm -rf first_basket