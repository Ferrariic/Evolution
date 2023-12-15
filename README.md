# Evolution

Genetic algorithms for a self-contained ecosystem.

![GitHub repo size](https://img.shields.io/github/repo-size/Ferrariic/Evolution?style=plastic) ![Lines of code](https://img.shields.io/tokei/lines/github/Ferrariic/Evolution?style=plastic)


## What is this?
`Evolution` is a repository for simulating populations with genetic algorithms. It primarily runs in Python, and can be used as a teaching element to display how populations change with time.
 
## Usage
### Installing and Running
1. Install [VsCode](https://code.visualstudio.com/)
2. Install (Github Desktop)[https://docs.github.com/en/desktop/installing-and-configuring-github-desktop/installing-and-authenticating-to-github-desktop/installing-github-desktop]
3. Fork this repository
4. Open in VsCode
5. Start a new Terminal in VsCode
6. In `notes.md` run the following. This will download and install the latest dependencies in a virtual environment.
```
python -m venv venv
venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```
7. Run the file `World.py` in `src\World\World.py`

### What are the different screen-related elements?
**Sprites**

![Sprite](https://user-images.githubusercontent.com/5789682/154923420-d236f3f9-7ddb-4156-9a25-ae075fb4a905.png)

These are sprites. They represent single entities in the environment. The actions that the entities are performing can be seen above the sprite. In this case, this entity is moving upward relative to the surrounding screen.
 
 **Environment**
 
The environment is a collection of sprites and their actions. Every `year` or `turn` the sprites can perform exactly one action. During this action period, they may fight, mate, move, rotate, or make another decision, this is reflected in the console, and on the corresponding display.

![image](https://user-images.githubusercontent.com/5789682/154921737-cafe672f-1c71-42b2-b6ee-f7c3ee9aa56d.png)

## Sprite Information
1. **How are the sprites able to make decisions, and how do these decisions change as the generations and years increase?**
*The sprites are able to make decisions based upon their initialized genetic code. Their genetic code is first set at random, and then every subsequent generation contains the offspring of the survivors of the last generation. The genetic code is in hexadecimal which is then decoded into a binary string. The binary string is further decoded into weights for a neural network - this neural network allows each sprite to make a decision based upon its environment.*
2. **How does the sprite know what is going on around it?**
*If the sprite has a neuron which allows it to visualize, or take information, from the environment in the form of direction, proximity, or more -- then it will utilize that information in the neural network input.*
3. **How is the sprite look determined?**
*At this moment the sprite is created based upon flipping the binary representation of the first hexadecimal section of its genetic code. Therefore offspring, and parents of the offspring, all look relatively the same.*
4. **How are mutations handled?**
*As the generations increase, offspring are created from the survivors. During this mating process, mutations are incorporated into their genome, this can be used to solve a problem faster - or to encourage diversity in a population.*
5. **What do the symbols above each sprite represent?**
*The symbols above each sprite represent the action that the sprite is performing. If it is moving upward, you will see an upward moving arrow. If it has turned into a `plant` then it will have a grass icon above its representation.*

## Environment Information
1. **What is the shape of the environment?**
*At the moment, the shape of the environment is a rectangle. This may change in the future.*
2. **Can I remove the edges of the environment and allow for overlap?**
*Yes, this can be done in the `src\World\Entity\status.py` file, this location will change in the future.*
3. **Can I add obstructions to the environment?**
*Not at this time, though that will be planned for the future.*
