# Exercises for the Chyber-Pysichal System (CPS) Course
2024 - University of Trieste - [link](https://corsi.units.it/en/in20/teaching-unit/2024/397806/af_id/400512)\
Teacher: Prof. Laura Nenzi\
Assistant: Simone Silvetti

(This is a fork from the Ennio Visconti's GitHub [page](https://github.com/ennioVisco/cps-labs). Thanks Ennio!)


## Prerequisites:

- Python 3.9+
- poetry
- JDK 21+ in the running environment

## Installing Java 
### Linux / Mac
There are two possibilities: 

#### 1) SDKMAN
My suggestion is to use [SDKMAN](https://sdkman.io/install).
After you have installed it, then execute this in console:
```bash
sdk install java
```
More information [here](https://sdkman.io/usage). 
#### 2) Adoptium
You may also dlownload the executable from [Adoptiom](https://adoptium.net/temurin/releases/?os=any) and install it. 

### Windows
You can download the JRE version from: [Adoptiom](https://adoptium.net/temurin/releases/?os=any)

## Setup
Please follow these steps to configure your environment:
### 1 - Creating a virtual environment
```sh
python -m venv env
```
`env` is the name on the environment (you can choose whatever you like).

### 2 - Activating the virtual environment

```sh
source env/bin/activate
```

### 3 - Installing Poetry

```sh
pip install poetry
```

### 4 - Installing all the packages (through Poetry)

Run the following command at the root of the project:

```bash
poetry install
```
Now you have a full working enviroment!

## Documentation

For basic Moonlight documentation, you can check the wiki at the main repository [here](https://github.com/MoonLightSuite/moonlight/wiki)
