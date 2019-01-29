INPUT_TS_PATH=$1
rm -rf ./dist
tsc --outDir ./dist $INPUT_TS_PATH
find ./dist/ -iname "*.js" -exec node {} \;