echo "" > ./resultsFromGCC.txt
for file in $(ls ./tests); do
    ./compiledWithGCC/$file
    echo "$? $file" >> ./resultsFromGCC.txt
done

echo "GCC done"