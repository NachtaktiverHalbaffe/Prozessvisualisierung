# Process Visualization
![IMG_20210713_163232734](https://github.com/NachtaktiverHalbaffe/Prozessvisualisierung/assets/57433516/bf6d1195-d6d9-423e-b944-aa9a40d27f8c)

This application was developed in my Bachelor Thesis in 2021. The goal was to provide virtual production process to a model process which only contained empty carriers as physical units. 
These were run on Raspberry Pi 4s and connected to an display above the pyhsical machines of the CP Factory model process of the institute. The process visualization deployed as distributed systems and were communicating 
with [IAS-MES](https://github.com/NachtaktiverHalbaffe/IAS-MES) which stored the state of these virtual products which were manufactured.

For communication a Flask API was used and for the 3D visualization PyGame was utilized. This programm was developed in one and a halth month alongside the [IAS-MES](https://github.com/NachtaktiverHalbaffe/IAS-MES) and 
[FleetIAS](https://github.com/NachtaktiverHalbaffe/FleetIAS). It was my fist time messing around with 3D visualization and creating a REST API with Django and Flask.

#  License
Copyright 2023 Institute of Industrial Automation and Software Engineering, University of Stuttgart

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

  http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
