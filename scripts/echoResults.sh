echo "" > ./results.txt
for file in $(ls ./compiled); do
    ./compiled/$file
    echo "$? $file" >> ./results.txt
done

echo "Basic done"