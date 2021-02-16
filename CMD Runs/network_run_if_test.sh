read -p "Start simulations? " -n 1 -r
if [[ $REPLY =~ ^[Yy]$ ]]
echo "Nope? Ok."
then

code_file="./../Model/motaXT0.4.py"
basepath="./../../../Complex Networks 2010 - Storage"

python "${code_file}" -nn 50000 -syn 20 -mn 1 -sr 10000 -meta "full" -metaargs 0 -dits 400 -pits 1000 -dmet "in-degree" -pmet "inv-hebbian-approx" -ff 1.0 --no-cm --save-net --no-save-fitness --save-freq 100 -save-to "${basepath}/Teste IF 21Nov19_3/Sel"

python "${code_file}" -nn 50000 -syn 20 -mn 1 -sr 10000 -meta "full" -metaargs 0 -dits 400 -pits 1000 -dmet "in-degree" -pmet "random" -ff 1.0 --no-cm --save-net --no-save-fitness --save-freq 100 -save-to "${basepath}/Teste IF 21Nov19_3/Rnd"
fi
