read -p "Start simulations? " -n 1 -r

if [[ $REPLY =~ ^[Yy]$ ]]

echo "Nope? Ok."

then

code_file="./../Model/motaXT0.4.py"

basepath="./../../../Complex Networks 2010 - Storage/Large Nets/50k"

python "${code_file}" -nn 50000 -syn 10 -mn 1 -sr 50000 -meta "full" -metaargs 0 -dits 500 -pits 2500 -dmet "in-degree" -pmet "hebbian-approx" -ff 1.0 --no-cm --save-net --no-save-fitness --save-freq 50 -save-to "${basepath}/Sim 1"

python "${code_file}" -nn 50000 -syn 10 -mn 1 -sr 50000 -meta "full" -metaargs 0 -dits 500 -pits 2500 -dmet "random" -pmet "hebbian-approx" -ff 1.0 --no-cm --save-net --no-save-fitness --save-freq 50 -save-to "${basepath}/Sim 2"

python "${code_file}" -nn 50000 -syn 10 -mn 1 -sr 50000 -meta "full" -metaargs 0 -dits 0 -pits 2500 -dmet "in-degree" -pmet "hebbian-approx" -ff 1.0 --no-cm --save-net --no-save-fitness --save-freq 50 -save-to "${basepath}/Sim 3"

python "${code_file}" -nn 50000 -syn 10 -mn 1 -sr 50000 -meta "full" -metaargs 0 -dits 500 -pits 2500 -dmet "in-degree" -pmet "random" -ff 1.0 --no-cm --save-net --no-save-fitness --save-freq 50 -save-to "${basepath}/Sim 6"

python "${code_file}" -nn 50000 -syn 10 -mn 1 -sr 50000 -meta "full" -metaargs 0 -dits 500 -pits 2500 -dmet "in-degree" -pmet "hebbian-approx" -ff 0.8 --no-cm --save-net --no-save-fitness --save-freq 50 -save-to "${basepath}/Sim 7"

python "${code_file}" -nn 50000 -syn 10 -mn 1 -sr 50000 -meta "full" -metaargs 0 -dits 500 -pits 2500 -dmet "in-degree" -pmet "hebbian-approx" -ff 0.5 --no-cm --save-net --no-save-fitness --save-freq 50 -save-to "${basepath}/Sim 8"

python "${code_file}" -nn 50000 -syn 10 -mn 20 -sr 50000 -meta "random" -metaargs 0 -dits 500 -pits 2500 -dmet "in-degree" -pmet "hebbian-approx" -ff 1.0 --no-cm --save-net --no-save-fitness --save-freq 50 -save-to "${basepath}/Sim 9"

python "${code_file}" -nn 50000 -syn 10 -mn 20 -sr 50000 -meta "lattice" -metaargs 3 -dits 500 -pits 2500 -dmet "in-degree" -pmet "hebbian-approx" -ff 1.0 --no-cm --save-net --no-save-fitness --save-freq 50 -save-to "${basepath}/Sim 10"

python "${code_file}" -nn 50000 -syn 10 -mn 20 -sr 50000 -meta "smallworld" -metaargs 0.1 -dits 500 -pits 2500 -dmet "in-degree" -pmet "hebbian-approx" -ff 1.0 --no-cm --save-net --no-save-fitness --save-freq 50 -save-to "${basepath}/Sim 11"

python "${code_file}" -nn 50000 -syn 10 -mn 20 -sr 50000 -meta "offdiagonal" -metaargs 0 -dits 500 -pits 2500 -dmet "in-degree" -pmet "hebbian-approx" -ff 1.0 --no-cm --save-net --no-save-fitness --save-freq 50 -save-to "${basepath}/Sim 12"

python "${code_file}" -nn 50000 -syn 10 -mn 1 -sr 50000 -meta "full" -metaargs 0 -dits 500 -pits 2500 -dmet "in-degree" -pmet "inv-hebbian-approx" -ff 1.0 --no-cm --save-net --no-save-fitness --save-freq 50 -save-to "${basepath}/Sim 5"

python "${code_file}" -nn 50000 -syn 10 -mn 1 -sr 50000 -meta "full" -metaargs 0 -dits 500 -pits 2500 -dmet "random" -pmet "inv-hebbian-approx" -ff 1.0 --no-cm --save-net --no-save-fitness --save-freq 50 -save-to "${basepath}/Sim 17"

python "${code_file}" -nn 50000 -syn 10 -mn 1 -sr 50000 -meta "full" -metaargs 0 -dits 0 -pits 2500 -dmet "random" -pmet "inv-hebbian-approx" -ff 1.0 --no-cm --save-net --no-save-fitness --save-freq 50 -save-to "${basepath}/Sim 18"

python "${code_file}" -nn 50000 -syn 10 -mn 1 -sr 50000 -meta "full" -metaargs 0 -dits 500 -pits 2500 -dmet "in-degree" -pmet "inv-hebbian-approx" -ff 0.8 --no-cm --save-net --no-save-fitness --save-freq 50 -save-to "${basepath}/Sim 19"

python "${code_file}" -nn 50000 -syn 10 -mn 1 -sr 50000 -meta "full" -metaargs 0 -dits 500 -pits 2500 -dmet "in-degree" -pmet "inv-hebbian-approx" -ff 0.5 --no-cm --save-net --no-save-fitness --save-freq 50 -save-to "${basepath}/Sim 20"

python "${code_file}" -nn 10000 -syn 10 -mn 20 -sr 50000 -meta "random" -metaargs 0 -dits 500 -pits 2500 -dmet "in-degree" -pmet "inv-hebbian-approx" -ff 1.0 --no-cm --save-net --no-save-fitness --save-freq 50 -save-to "${basepath}/Sim 21"

python "${code_file}" -nn 10000 -syn 10 -mn 20 -sr 50000 -meta "lattice" -metaargs 3 -dits 500 -pits 2500 -dmet "in-degree" -pmet "inv-hebbian-approx" -ff 1.0 --no-cm --save-net --no-save-fitness --save-freq 50 -save-to "${basepath}/Sim 23"

python "${code_file}" -nn 10000 -syn 10 -mn 20 -sr 50000 -meta "smallworld" -metaargs 0.1 -dits 500 -pits 2500 -dmet "in-degree" -pmet "inv-hebbian-approx" -ff 1.0 --no-cm --save-net --no-save-fitness --save-freq 50 -save-to "${basepath}/Sim 22"

python "${code_file}" -nn 10000 -syn 10 -mn 20 -sr 50000 -meta "offdiagonal" -metaargs 0 -dits 500 -pits 2500 -dmet "in-degree" -pmet "inv-hebbian-approx" -ff 1.0 --no-cm --save-net --no-save-fitness --save-freq 50 -save-to "${basepath}/Sim 24"

python "${code_file}" -nn 50000 -syn 10 -mn 1 -sr 50000 -meta "full" -metaargs 0 -dits 500 -pits 2500 -dmet "random" -pmet "hebbian-approx" -ff 0.8 --no-cm --save-net --no-save-fitness --save-freq 50 -save-to "${basepath}/Sim 25"

python "${code_file}" -nn 50000 -syn 10 -mn 1 -sr 50000 -meta "full" -metaargs 0 -dits 500 -pits 2500 -dmet "random" -pmet "hebbian-approx" -ff 0.5 --no-cm --save-net --no-save-fitness --save-freq 50 -save-to "${basepath}/Sim 26"

python "${code_file}" -nn 50000 -syn 10 -mn 1 -sr 50000 -meta "full" -metaargs 0 -dits 500 -pits 2500 -dmet "random" -pmet "inv-hebbian-approx" -ff 0.8 --no-cm --save-net --no-save-fitness --save-freq 50 -save-to "${basepath}/Sim 27"

python "${code_file}" -nn 50000 -syn 10 -mn 1 -sr 50000 -meta "full" -metaargs 0 -dits 500 -pits 2500 -dmet "random" -pmet "inv-hebbian-approx" -ff 0.5 --no-cm --save-net --no-save-fitness --save-freq 50 -save-to "${basepath}/Sim 28"

python "${code_file}" -nn 50000 -syn 10 -mn 1 -sr 50000 -meta "full" -metaargs 0 -dits 0 -pits 2500 -dmet "random" -pmet "hebbian-approx" -ff 0.8 --no-cm --save-net --no-save-fitness --save-freq 50 -save-to "${basepath}/Sim 29"

python "${code_file}" -nn 50000 -syn 10 -mn 1 -sr 50000 -meta "full" -metaargs 0 -dits 0 -pits 2500 -dmet "random" -pmet "hebbian-approx" -ff 0.5 --no-cm --save-net --no-save-fitness --save-freq 50 -save-to "${basepath}/Sim 30"

python "${code_file}" -nn 50000 -syn 10 -mn 1 -sr 50000 -meta "full" -metaargs 0 -dits 0 -pits 2500 -dmet "random" -pmet "inv-hebbian-approx" -ff 0.8 --no-cm --save-net --no-save-fitness --save-freq 50 -save-to "${basepath}/Sim 31"

python "${code_file}" -nn 50000 -syn 10 -mn 1 -sr 50000 -meta "full" -metaargs 0 -dits 1 -pits 2500 -dmet "random" -pmet "inv-hebbian-approx" -ff 0.5 --no-cm --save-net --no-save-fitness --save-freq 50 -save-to "${basepath}/Sim 32"



basepath="./../../../Complex Networks 2010 - Storage/Large Nets/100k"

python "${code_file}" -nn 100000 -syn 10 -mn 1 -sr 100000 -meta "full" -metaargs 0 -dits 500 -pits 2500 -dmet "in-degree" -pmet "hebbian-approx" -ff 1.0 --no-cm --save-net --no-save-fitness --save-freq 50 -save-to "${basepath}/Sim 1"

python "${code_file}" -nn 100000 -syn 10 -mn 1 -sr 100000 -meta "full" -metaargs 0 -dits 500 -pits 2500 -dmet "random" -pmet "hebbian-approx" -ff 1.0 --no-cm --save-net --no-save-fitness --save-freq 50 -save-to "${basepath}/Sim 2"

python "${code_file}" -nn 100000 -syn 10 -mn 1 -sr 100000 -meta "full" -metaargs 0 -dits 0 -pits 2500 -dmet "in-degree" -pmet "hebbian-approx" -ff 1.0 --no-cm --save-net --no-save-fitness --save-freq 50 -save-to "${basepath}/Sim 3"

python "${code_file}" -nn 100000 -syn 10 -mn 1 -sr 100000 -meta "full" -metaargs 0 -dits 500 -pits 2500 -dmet "in-degree" -pmet "random" -ff 1.0 --no-cm --save-net --no-save-fitness --save-freq 50 -save-to "${basepath}/Sim 6"

python "${code_file}" -nn 100000 -syn 10 -mn 1 -sr 100000 -meta "full" -metaargs 0 -dits 500 -pits 2500 -dmet "in-degree" -pmet "hebbian-approx" -ff 0.8 --no-cm --save-net --no-save-fitness --save-freq 50 -save-to "${basepath}/Sim 7"

python "${code_file}" -nn 100000 -syn 10 -mn 1 -sr 100000 -meta "full" -metaargs 0 -dits 500 -pits 2500 -dmet "in-degree" -pmet "hebbian-approx" -ff 0.5 --no-cm --save-net --no-save-fitness --save-freq 50 -save-to "${basepath}/Sim 8"

python "${code_file}" -nn 100000 -syn 10 -mn 20 -sr 100000 -meta "random" -metaargs 0 -dits 500 -pits 2500 -dmet "in-degree" -pmet "hebbian-approx" -ff 1.0 --no-cm --save-net --no-save-fitness --save-freq 50 -save-to "${basepath}/Sim 9"

python "${code_file}" -nn 100000 -syn 10 -mn 20 -sr 100000 -meta "lattice" -metaargs 3 -dits 500 -pits 2500 -dmet "in-degree" -pmet "hebbian-approx" -ff 1.0 --no-cm --save-net --no-save-fitness --save-freq 50 -save-to "${basepath}/Sim 10"

python "${code_file}" -nn 100000 -syn 10 -mn 20 -sr 100000 -meta "smallworld" -metaargs 0.1 -dits 500 -pits 2500 -dmet "in-degree" -pmet "hebbian-approx" -ff 1.0 --no-cm --save-net --no-save-fitness --save-freq 50 -save-to "${basepath}/Sim 11"

python "${code_file}" -nn 100000 -syn 10 -mn 20 -sr 100000 -meta "offdiagonal" -metaargs 0 -dits 500 -pits 2500 -dmet "in-degree" -pmet "hebbian-approx" -ff 1.0 --no-cm --save-net --no-save-fitness --save-freq 50 -save-to "${basepath}/Sim 12"

python "${code_file}" -nn 100000 -syn 10 -mn 1 -sr 100000 -meta "full" -metaargs 0 -dits 500 -pits 2500 -dmet "in-degree" -pmet "inv-hebbian-approx" -ff 1.0 --no-cm --save-net --no-save-fitness --save-freq 50 -save-to "${basepath}/Sim 5"

python "${code_file}" -nn 100000 -syn 10 -mn 1 -sr 100000 -meta "full" -metaargs 0 -dits 500 -pits 2500 -dmet "random" -pmet "inv-hebbian-approx" -ff 1.0 --no-cm --save-net --no-save-fitness --save-freq 50 -save-to "${basepath}/Sim 17"

python "${code_file}" -nn 100000 -syn 10 -mn 1 -sr 100000 -meta "full" -metaargs 0 -dits 0 -pits 2500 -dmet "random" -pmet "inv-hebbian-approx" -ff 1.0 --no-cm --save-net --no-save-fitness --save-freq 50 -save-to "${basepath}/Sim 18"

python "${code_file}" -nn 100000 -syn 10 -mn 1 -sr 100000 -meta "full" -metaargs 0 -dits 500 -pits 2500 -dmet "in-degree" -pmet "inv-hebbian-approx" -ff 0.8 --no-cm --save-net --no-save-fitness --save-freq 50 -save-to "${basepath}/Sim 19"

python "${code_file}" -nn 100000 -syn 10 -mn 1 -sr 100000 -meta "full" -metaargs 0 -dits 500 -pits 2500 -dmet "in-degree" -pmet "inv-hebbian-approx" -ff 0.5 --no-cm --save-net --no-save-fitness --save-freq 50 -save-to "${basepath}/Sim 20"

python "${code_file}" -nn 20000 -syn 10 -mn 20 -sr 100000 -meta "random" -metaargs 0 -dits 500 -pits 2500 -dmet "in-degree" -pmet "inv-hebbian-approx" -ff 1.0 --no-cm --save-net --no-save-fitness --save-freq 50 -save-to "${basepath}/Sim 21"

python "${code_file}" -nn 20000 -syn 10 -mn 20 -sr 100000 -meta "lattice" -metaargs 3 -dits 500 -pits 2500 -dmet "in-degree" -pmet "inv-hebbian-approx" -ff 1.0 --no-cm --save-net --no-save-fitness --save-freq 50 -save-to "${basepath}/Sim 23"

python "${code_file}" -nn 20000 -syn 10 -mn 20 -sr 100000 -meta "smallworld" -metaargs 0.1 -dits 500 -pits 2500 -dmet "in-degree" -pmet "inv-hebbian-approx" -ff 1.0 --no-cm --save-net --no-save-fitness --save-freq 50 -save-to "${basepath}/Sim 22"

python "${code_file}" -nn 20000 -syn 10 -mn 20 -sr 100000 -meta "offdiagonal" -metaargs 0 -dits 500 -pits 2500 -dmet "in-degree" -pmet "inv-hebbian-approx" -ff 1.0 --no-cm --save-net --no-save-fitness --save-freq 50 -save-to "${basepath}/Sim 24"

python "${code_file}" -nn 100000 -syn 10 -mn 1 -sr 100000 -meta "full" -metaargs 0 -dits 500 -pits 2500 -dmet "random" -pmet "hebbian-approx" -ff 0.8 --no-cm --save-net --no-save-fitness --save-freq 50 -save-to "${basepath}/Sim 25"

python "${code_file}" -nn 100000 -syn 10 -mn 1 -sr 100000 -meta "full" -metaargs 0 -dits 500 -pits 2500 -dmet "random" -pmet "hebbian-approx" -ff 0.5 --no-cm --save-net --no-save-fitness --save-freq 50 -save-to "${basepath}/Sim 26"

python "${code_file}" -nn 100000 -syn 10 -mn 1 -sr 100000 -meta "full" -metaargs 0 -dits 500 -pits 2500 -dmet "random" -pmet "inv-hebbian-approx" -ff 0.8 --no-cm --save-net --no-save-fitness --save-freq 50 -save-to "${basepath}/Sim 27"

python "${code_file}" -nn 100000 -syn 10 -mn 1 -sr 100000 -meta "full" -metaargs 0 -dits 500 -pits 2500 -dmet "random" -pmet "inv-hebbian-approx" -ff 0.5 --no-cm --save-net --no-save-fitness --save-freq 50 -save-to "${basepath}/Sim 28"

python "${code_file}" -nn 100000 -syn 10 -mn 1 -sr 100000 -meta "full" -metaargs 0 -dits 0 -pits 2500 -dmet "random" -pmet "hebbian-approx" -ff 0.8 --no-cm --save-net --no-save-fitness --save-freq 50 -save-to "${basepath}/Sim 29"

python "${code_file}" -nn 100000 -syn 10 -mn 1 -sr 100000 -meta "full" -metaargs 0 -dits 0 -pits 2500 -dmet "random" -pmet "hebbian-approx" -ff 0.5 --no-cm --save-net --no-save-fitness --save-freq 50 -save-to "${basepath}/Sim 30"

python "${code_file}" -nn 100000 -syn 10 -mn 1 -sr 100000 -meta "full" -metaargs 0 -dits 0 -pits 2500 -dmet "random" -pmet "inv-hebbian-approx" -ff 0.8 --no-cm --save-net --no-save-fitness --save-freq 50 -save-to "${basepath}/Sim 31"

python "${code_file}" -nn 100000 -syn 10 -mn 1 -sr 100000 -meta "full" -metaargs 0 -dits 0 -pits 2500 -dmet "random" -pmet "inv-hebbian-approx" -ff 0.5 --no-cm --save-net --no-save-fitness --save-freq 50 -save-to "${basepath}/Sim 32"

fi