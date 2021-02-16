read -p "Start simulations? " -n 1 -r

if [[ $REPLY =~ ^[Yy]$ ]]

echo "Nope? Ok."

then

code_file="./../Model/motaXT0.5.py"

basepath="./../../../Complex Networks 2010 - Storage/Teste Meta"

python "${code_file}" -nn 5 -syn 1 -mn 2 -sr 5 -meta "random" -metaargs 0 -dits 5 -pits 2 -dmet "in-degree" -pmet "hebbian-approx" -ff 1.0 --nocm --save-net --no-save-fitness --save-freq 50 -save-to "${basepath}/Sim 9"

# python "${code_file}" -nn 200 -syn 10 -mn 20 -sr 200 -meta "lattice" -metaargs 3 -dits 500 -pits 2500 -dmet "in-degree" -pmet "hebbian-approx" -ff 1.0 --no-cm --save-net --no-save-fitness --save-freq 50 -save-to "${basepath}/Sim 10"

# python "${code_file}" -nn 200 -syn 10 -mn 20 -sr 200 -meta "smallworld" -metaargs 0.1 -dits 500 -pits 2500 -dmet "in-degree" -pmet "hebbian-approx" -ff 1.0 --no-cm --save-net --no-save-fitness --save-freq 50 -save-to "${basepath}/Sim 11"

# python "${code_file}" -nn 200 -syn 10 -mn 20 -sr 200 -meta "offdiagonal" -metaargs 0 -dits 500 -pits 2500 -dmet "in-degree" -pmet "hebbian-approx" -ff 1.0 --no-cm --save-net --no-save-fitness --save-freq 50 -save-to "${basepath}/Sim 12"

# python "${code_file}" -nn 200 -syn 10 -mn 20 -sr 200 -meta "random" -metaargs 0 -dits 500 -pits 2500 -dmet "in-degree" -pmet "inv-hebbian-approx" -ff 1.0 --no-cm --save-net --no-save-fitness --save-freq 50 -save-to "${basepath}/Sim 21"

# python "${code_file}" -nn 200 -syn 10 -mn 20 -sr 200 -meta "lattice" -metaargs 3 -dits 500 -pits 2500 -dmet "in-degree" -pmet "inv-hebbian-approx" -ff 1.0 --no-cm --save-net --no-save-fitness --save-freq 50 -save-to "${basepath}/Sim 23"

# python "${code_file}" -nn 200 -syn 10 -mn 20 -sr 200 -meta "smallworld" -metaargs 0.1 -dits 500 -pits 2500 -dmet "in-degree" -pmet "inv-hebbian-approx" -ff 1.0 --no-cm --save-net --no-save-fitness --save-freq 50 -save-to "${basepath}/Sim 22"

# python "${code_file}" -nn 200 -syn 10 -mn 20 -sr 200 -meta "offdiagonal" -metaargs 0 -dits 500 -pits 2500 -dmet "in-degree" -pmet "inv-hebbian-approx" -ff 1.0 --no-cm --save-net --no-save-fitness --save-freq 50 -save-to "${basepath}/Sim 24"

fi