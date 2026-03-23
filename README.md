# 🤖 Gurobi-Solver

## 💡 Overview

This project implements linear programming problems code solutions.
Problems are solved using gurobi solving envinge, specificly gurobipy.
Repo was created for learning purposes, as a solution center for System
Analysis and Decision Support Methods Laboratories.

## ⚙️ Building Commands:

Project is using anaconda, as a packet manager and enviroment.

```bash
# Create Environment
conda create -n gurobi_env python=3.10 20
conda install python=3.10
conda install gurobi
conda install scipy
conda install pytest
conda activate gurobi_env

# Run tests
python3 -m unittest discover -s tests -p '*test.py'

# Set local git hook pre-commit
chmod +x .githooks/pre-commit
git config core.hooksPath .githooks
```

## 📚 Documentation

Generate Documentation Template

```bash
python3 -m pydoc -w \
    src.classes.Problem \
    src.classes.PartitionProblem \
    src.classes.MakespanSchedulingProblem \
    src.classes.KnapsackProblem \
    src.classes.DistancesProblem
```

## 🛠 Technologies

<p align="center">
    <a href="https://skillicons.dev">
        <img src="https://skillicons.dev/icons?i=python,anaconda,vscode,github,git" />
    </a>
</p>
