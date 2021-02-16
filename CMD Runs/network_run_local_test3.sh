read -p "Start simulations? " -n 1 -r
if [[ $REPLY =~ ^[Yy]$ ]]; then

code_file="/home/kleber/Dropbox/Scientific Research/Projects/Networks of Neurons - Death and Pruning/Complex Networks 2010 - Shared/Code/Model/motaXT0.4.py"
basepath="/home/kleber/Dropbox/Scientific Research/Projects/Networks of Neurons - Death and Pruning/Complex Networks 2010 - Storage"

python "${code_file}" -nn 20000 -syn 100 -mn 1 -sr 20000 -meta "full" -metaargs 0 -dits 0 -pits 1000 -dmet "random" -pmet "inv-hebbian-approx" -ff 1.0 --no-cm --save-net --no-save-fitness --save-freq 100 -save-to "${basepath}/Teste Expoente/Sem Morte + InvHebb"

python "${code_file}" -nn 20000 -syn 100 -mn 1 -sr 20000 -meta "full" -metaargs 0 -dits 0 -pits 1000 -dmet "random" -pmet "random" -ff 1.0 --no-cm --save-net --no-save-fitness --save-freq 100 -save-to "${basepath}/Teste Expoente/Sem Morte = Rnd"

python "${code_file}" -nn 20000 -syn 100 -mn 1 -sr 20000 -meta "full" -metaargs 0 -dits 0 -pits 1000 -dmet "random" -pmet "hebbian-approx" -ff 1.0 --no-cm --save-net --no-save-fitness --save-freq 100 -save-to "${basepath}/Teste Expoente/Sem Morte + Hebb"
    
python "${code_file}" -nn 20000 -syn 100 -mn 1 -sr 20000 -meta "full" -metaargs 0 -dits 500 -pits 1000 -dmet "random" -pmet "inv-hebbian-approx" -ff 1.0 --no-cm --save-net --no-save-fitness --save-freq 100 -save-to "${basepath}/Teste Expoente/Morte Rnd + InvHebb"

python "${code_file}" -nn 20000 -syn 100 -mn 1 -sr 20000 -meta "full" -metaargs 0 -dits 500 -pits 1000 -dmet "random" -pmet "random" -ff 1.0 --no-cm --save-net --no-save-fitness --save-freq 100 -save-to "${basepath}/Teste Expoente/Morte Rnd + Rnd"

python "${code_file}" -nn 20000 -syn 100 -mn 1 -sr 20000 -meta "full" -metaargs 0 -dits 500 -pits 1000 -dmet "random" -pmet "hebbian-approx" -ff 1.0 --no-cm --save-net --no-save-fitness --save-freq 100 -save-to "${basepath}/Teste Expoente/Morte Rnd + Hebb"

python "${code_file}" -nn 20000 -syn 100 -mn 1 -sr 20000 -meta "full" -metaargs 0 -dits 500 -pits 1000 -dmet "in-degree" -pmet "inv-hebbian-approx" -ff 1.0 --no-cm --save-net --no-save-fitness --save-freq 50 -save-to "${basepath}/Teste Expoente/InvHebb2"
python "${code_file}" -nn 20000 -syn 100 -mn 1 -sr 20000 -meta "full" -metaargs 0 -dits 500 -pits 1000 -dmet "in-degree" -pmet "hebbian-approx" -ff 1.0 --no-cm --save-net --no-save-fitness --save-freq 50 -save-to "${basepath}/Teste Expoente/Hebb2"

else
    printf "\nNope? Ok.\n"
fi
