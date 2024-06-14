python "motaXT0.6.py" -nn 50000 -syn 100 -mn 1 -sr 50000 -meta "full" -metaargs 0 -dits 500 -pits 2500 -dmet "in-degree" -pmet "hebbian-approx" -ff 1.0 --no-cm --save-net --no-save-fitness --save-freq 50 -save-to "Sim 1x"

python "motaXT0.6.py" -nn 50000 -syn 100 -mn 1 -sr 50000 -meta "full" -metaargs 0 -dits 500 -pits 2500 -dmet "random" -pmet "hebbian-approx" -ff 1.0 --no-cm --save-net --no-save-fitness --save-freq 50 -save-to "Sim 2x"

python "motaXT0.6.py" -nn 50000 -syn 100 -mn 1 -sr 50000 -meta "full" -metaargs 0 -dits 500 -pits 2500 -dmet "in-degree" -pmet "random" -ff 1.0 --no-cm --save-net --no-save-fitness --save-freq 50 -save-to "Sim 6x"

python "motaXT0.6.py" -nn 50000 -syn 100 -mn 1 -sr 50000 -meta "full" -metaargs 0 -dits 500 -pits 2500 -dmet "in-degree" -pmet "hebbian-approx" -ff 0.8 --no-cm --save-net --no-save-fitness --save-freq 50 -save-to "Sim 7x"

python "motaXT0.6.py" -nn 50000 -syn 100 -mn 1 -sr 50000 -meta "full" -metaargs 0 -dits 500 -pits 2500 -dmet "in-degree" -pmet "hebbian-approx" -ff 0.5 --no-cm --save-net --no-save-fitness --save-freq 50 -save-to "Sim 8x"

