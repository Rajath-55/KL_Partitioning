#!/bin/bash

# Run C++ program and extract cost
cd ./App
for file in *
do
        if [[ -f $file ]]; then
            graph_val=$file
            echo "Evaluating for file $graph_val"
            echo ""
            cpp_result=$(cd ../CPP_Code && ./a.out $graph_val 100 0 | grep "cost in CC" | grep -o '[0-9]*\.[0-9]*')
            echo "CPP Result : $cpp_result"
            echo ""
            # Run Python program and extract cost
            python_result=$(cd ../Python_Code && python3 opticalKL.py $graph_val 100 0 | grep "cost in CC" | grep -o '[0-9]*\.[0-9]*')

            echo "Python result : $python_result"
            echo ""
            # Calculate and print difference
            difference=$(echo "($cpp_result - $python_result)*100/$cpp_result" | bc)

            echo "The difference between C++ and Python results for $graph_val is: $difference %"
            echo ""
            echo "-----------------------------------------------------------------------------"
            echo ""
        fi

done
