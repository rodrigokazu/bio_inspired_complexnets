read -p "Start simulations? " -n 1 -r

if [[ $REPLY =~ ^[Yy]$ ]]

echo "Nope? Ok."

then

code_file="./../Model/motaXT0.5.py"

basepath="./../../../Complex Networks 2010 - Storage/Large Nets/50k"

python "${code_file}" -nn 50000 -syn 10 -mn 20 -sr 50000 -meta "random" -metaargs 0 -dits 500 -pits 2500 -dmet "in-degree" -pmet "hebbian-approx" -ff 1.0 --no-cm --save-net --no-save-fitness --save-freq 50 -save-to "${basepath}/Sim 9"

python "${code_file}" -nn 50000 -syn 10 -mn 20 -sr 50000 -meta "lattice" -metaargs 3 -dits 500 -pits 2500 -dmet "in-degree" -pmet "hebbian-approx" -ff 1.0 --no-cm --save-net --no-save-fitness --save-freq 50 -save-to "${basepath}/Sim 10"

python "${code_file}" -nn 50000 -syn 10 -mn 20 -sr 50000 -meta "smallworld" -metaargs 0.1 -dits 500 -pits 2500 -dmet "in-degree" -pmet "hebbian-approx" -ff 1.0 --no-cm --save-net --no-save-fitness --save-freq 50 -save-to "${basepath}/Sim 11"

python "${code_file}" -nn 50000 -syn 10 -mn 20 -sr 50000 -meta "offdiagonal" -metaargs 0 -dits 500 -pits 2500 -dmet "in-degree" -pmet "hebbian-approx" -ff 1.0 --no-cm --save-net --no-save-fitness --save-freq 50 -save-to "${basepath}/Sim 12"

python "${code_file}" -nn 50000 -syn 10 -mn 20 -sr 50000 -meta "random" -metaargs 0 -dits 500 -pits 2500 -dmet "in-degree" -pmet "inv-hebbian-approx" -ff 1.0 --no-cm --save-net --no-save-fitness --save-freq 50 -save-to "${basepath}/Sim 21"

python "${code_file}" -nn 50000 -syn 10 -mn 20 -sr 50000 -meta "lattice" -metaargs 3 -dits 500 -pits 2500 -dmet "in-degree" -pmet "inv-hebbian-approx" -ff 1.0 --no-cm --save-net --no-save-fitness --save-freq 50 -save-to "${basepath}/Sim 23"

python "${code_file}" -nn 50000 -syn 10 -mn 20 -sr 50000 -meta "smallworld" -metaargs 0.1 -dits 500 -pits 2500 -dmet "in-degree" -pmet "inv-hebbian-approx" -ff 1.0 --no-cm --save-net --no-save-fitness --save-freq 50 -save-to "${basepath}/Sim 22"

python "${code_file}" -nn 50000 -syn 10 -mn 20 -sr 50000 -meta "offdiagonal" -metaargs 0 -dits 500 -pits 2500 -dmet "in-degree" -pmet "inv-hebbian-approx" -ff 1.0 --no-cm --save-net --no-save-fitness --save-freq 50 -save-to "${basepath}/Sim 24"

python "${code_file}" -nn 50000 -syn 10 -mn 1 -sr 50000 -meta "full" -metaargs 0 -dits 0 -pits 2500 -dmet "random" -pmet "inv-hebbian-approx" -ff 0.5 --no-cm --save-net --no-save-fitness --save-freq 50 -save-to "${basepath}/Sim 32_0"

python "${code_file}" -nn 50000 -syn 10 -mn 1 -sr 50000 -meta "full" -metaargs 0 -dits 1 -pits 2500 -dmet "random" -pmet "inv-hebbian-approx" -ff 0.5 --no-cm --save-net --no-save-fitness --save-freq 50 -save-to "${basepath}/Sim 32_1"



basepath="./../../../Complex Networks 2010 - Storage/Large Nets/100k"

python "${code_file}" -nn 10000 -syn 10 -mn 20 -sr 100000 -meta "random" -metaargs 0 -dits 500 -pits 2500 -dmet "in-degree" -pmet "hebbian-approx" -ff 1.0 --no-cm --save-net --no-save-fitness --save-freq 50 -save-to "${basepath}/Sim 9"

python "${code_file}" -nn 10000 -syn 10 -mn 20 -sr 100000 -meta "lattice" -metaargs 3 -dits 500 -pits 2500 -dmet "in-degree" -pmet "hebbian-approx" -ff 1.0 --no-cm --save-net --no-save-fitness --save-freq 50 -save-to "${basepath}/Sim 10"

python "${code_file}" -nn 10000 -syn 10 -mn 20 -sr 100000 -meta "smallworld" -metaargs 0.1 -dits 500 -pits 2500 -dmet "in-degree" -pmet "hebbian-approx" -ff 1.0 --no-cm --save-net --no-save-fitness --save-freq 50 -save-to "${basepath}/Sim 11"

python "${code_file}" -nn 10000 -syn 10 -mn 20 -sr 100000 -meta "offdiagonal" -metaargs 0 -dits 500 -pits 2500 -dmet "in-degree" -pmet "hebbian-approx" -ff 1.0 --no-cm --save-net --no-save-fitness --save-freq 50 -save-to "${basepath}/Sim 12"

python "${code_file}" -nn 10000 -syn 10 -mn 20 -sr 100000 -meta "random" -metaargs 0 -dits 500 -pits 2500 -dmet "in-degree" -pmet "inv-hebbian-approx" -ff 1.0 --no-cm --save-net --no-save-fitness --save-freq 50 -save-to "${basepath}/Sim 21"

python "${code_file}" -nn 10000 -syn 10 -mn 20 -sr 100000 -meta "lattice" -metaargs 3 -dits 500 -pits 2500 -dmet "in-degree" -pmet "inv-hebbian-approx" -ff 1.0 --no-cm --save-net --no-save-fitness --save-freq 50 -save-to "${basepath}/Sim 23"

python "${code_file}" -nn 10000 -syn 10 -mn 20 -sr 100000 -meta "smallworld" -metaargs 0.1 -dits 500 -pits 2500 -dmet "in-degree" -pmet "inv-hebbian-approx" -ff 1.0 --no-cm --save-net --no-save-fitness --save-freq 50 -save-to "${basepath}/Sim 22"

python "${code_file}" -nn 10000 -syn 10 -mn 20 -sr 100000 -meta "offdiagonal" -metaargs 0 -dits 500 -pits 2500 -dmet "in-degree" -pmet "inv-hebbian-approx" -ff 1.0 --no-cm --save-net --no-save-fitness --save-freq 50 -save-to "${basepath}/Sim 24"



basepath="./../../../Complex Networks 2010 - Storage/Large Nets/Sensitivity"

python "${code_file}" -nn 50000 -syn 10 -mn 1 -sr 50000 -meta "full" -metaargs 0 -dits 500 -pits 2500 -dmet "in-degree" -pmet "hebbian-approx" -ff 1.0 --no-cm --save-net --no-save-fitness --save-freq 50 -save-to "${basepath}/Sim 1" -a 0.01 -k 0.2

python "${code_file}" -nn 50000 -syn 10 -mn 1 -sr 50000 -meta "full" -metaargs 0 -dits 500 -pits 2500 -dmet "in-degree" -pmet "inv-hebbian-approx" -ff 1.0 --no-cm --save-net --no-save-fitness --save-freq 50 -save-to "${basepath}/Sim 5" -a 0.01 -k 0.2

python "${code_file}" -nn 50000 -syn 10 -mn 1 -sr 50000 -meta "full" -metaargs 0 -dits 500 -pits 2500 -dmet "in-degree" -pmet "hebbian-approx" -ff 1.0 --no-cm --save-net --no-save-fitness --save-freq 50 -save-to "${basepath}/Sim 1 - low A" -a 0.001 -k 0.2

python "${code_file}" -nn 50000 -syn 10 -mn 1 -sr 50000 -meta "full" -metaargs 0 -dits 500 -pits 2500 -dmet "in-degree" -pmet "inv-hebbian-approx" -ff 1.0 --no-cm --save-net --no-save-fitness --save-freq 50 -save-to "${basepath}/Sim 5 - low A" -a 0.001 -k 0.2

python "${code_file}" -nn 50000 -syn 10 -mn 1 -sr 50000 -meta "full" -metaargs 0 -dits 500 -pits 2500 -dmet "in-degree" -pmet "hebbian-approx" -ff 1.0 --no-cm --save-net --no-save-fitness --save-freq 50 -save-to "${basepath}/Sim 1 - high A" -a 0.1 -k 0.2

python "${code_file}" -nn 50000 -syn 10 -mn 1 -sr 50000 -meta "full" -metaargs 0 -dits 500 -pits 2500 -dmet "in-degree" -pmet "inv-hebbian-approx" -ff 1.0 --no-cm --save-net --no-save-fitness --save-freq 50 -save-to "${basepath}/Sim 5 - high A" -a 0.1 -k 0.2

python "${code_file}" -nn 50000 -syn 10 -mn 1 -sr 50000 -meta "full" -metaargs 0 -dits 500 -pits 2500 -dmet "in-degree" -pmet "hebbian-approx" -ff 1.0 --no-cm --save-net --no-save-fitness --save-freq 50 -save-to "${basepath}/Sim 1 - low K" -a 0.01 -k 0.02

python "${code_file}" -nn 50000 -syn 10 -mn 1 -sr 50000 -meta "full" -metaargs 0 -dits 500 -pits 2500 -dmet "in-degree" -pmet "inv-hebbian-approx" -ff 1.0 --no-cm --save-net --no-save-fitness --save-freq 50 -save-to "${basepath}/Sim 5 - low K" -a 0.01 -k 0.02

python "${code_file}" -nn 50000 -syn 10 -mn 1 -sr 50000 -meta "full" -metaargs 0 -dits 500 -pits 2500 -dmet "in-degree" -pmet "hebbian-approx" -ff 1.0 --no-cm --save-net --no-save-fitness --save-freq 50 -save-to "${basepath}/Sim 1 - high K" -a 0.01 -k 2

python "${code_file}" -nn 50000 -syn 10 -mn 1 -sr 50000 -meta "full" -metaargs 0 -dits 500 -pits 2500 -dmet "in-degree" -pmet "inv-hebbian-approx" -ff 1.0 --no-cm --save-net --no-save-fitness --save-freq 50 -save-to "${basepath}/Sim 5 - high K" -a 0.01 -k 2



basepath="./../../../Complex Networks 2010 - Storage/Large Nets/Long Death"

python "${code_file}" -nn 50000 -syn 10 -mn 1 -sr 50000 -meta "full" -metaargs 0 -dits 500 -pits 2500 -dmet "in-degree" -pmet "hebbian-approx" -ff 1.0 --no-cm --save-net --no-save-fitness --save-freq 50 -save-to "${basepath}/Sim 1"

python "${code_file}" -nn 50000 -syn 10 -mn 1 -sr 50000 -meta "full" -metaargs 0 -dits 500 -pits 2500 -dmet "in-degree" -pmet "inv-hebbian-approx" -ff 1.0 --no-cm --save-net --no-save-fitness --save-freq 50 -save-to "${basepath}/Sim 5"

python "${code_file}" -nn 50000 -syn 10 -mn 1 -sr 50000 -meta "full" -metaargs 0 -dits 1500 -pits 2500 -dmet "in-degree" -pmet "hebbian-approx" -ff 1.0 --no-cm --save-net --no-save-fitness --save-freq 50 -save-to "${basepath}/Sim 1 - long"

python "${code_file}" -nn 50000 -syn 10 -mn 1 -sr 50000 -meta "full" -metaargs 0 -dits 1500 -pits 2500 -dmet "in-degree" -pmet "inv-hebbian-approx" -ff 1.0 --no-cm --save-net --no-save-fitness --save-freq 50 -save-to "${basepath}/Sim 5 - long"