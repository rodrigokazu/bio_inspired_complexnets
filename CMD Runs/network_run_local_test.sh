read -p "Start simulations? " -n 1 -r
if [[ $REPLY =~ ^[Yy]$ ]]
echo "Nope? Ok."
then

code_file="/home/kleber/Dropbox/Scientific Research/Projects/Networks of Neurons - Death and Pruning/Complex Networks 2010 - Shared/Code/Model/motaXT0.4.py"
basepath="/home/kleber/Dropbox/Scientific Research/Projects/Networks of Neurons - Death and Pruning/Complex Networks 2010 - Storage"

python "${code_file}" -nn 10000 -syn 50 -mn 1 -sr 10000 -meta "full" -metaargs 0 -dits 101 -pits 101 -dmet "in-degree" -pmet "inv-hebbian-approx" -ff 1.0 --no-cm --save-net --no-save-fitness --save-freq 100 -save-to "${basepath}/Teste Local_2/Sel"

python "${code_file}" -nn 10000 -syn 50 -mn 1 -sr 10000 -meta "full" -metaargs 0 -dits 101 -pits 101 -dmet "in-degree" -pmet "random" -ff 1.0 --no-cm --save-net --no-save-fitness --save-freq 100 -save-to "${basepath}/Teste Local_2/Rnd"
fi
