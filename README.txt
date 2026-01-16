GA-Based Bioprinting Parameter Optimization
📌 Project Overview

This project implements a Genetic Algorithm (GA) to optimize 3D bioprinting parameters using experimental data from the CECT Bioprinting Database. The system identifies optimal printing conditions that balance cell viability, printing stability, and material safety.

🎯 Objectives

Optimize bioprinting parameters using evolutionary computation

Reduce cell damage caused by high pressure and speed

Provide data-driven decision support for biomaterial printing

Enable future integration with a user-friendly UI

⚙️ Parameters Optimized

Extrusion Pressure (kPa)

Printing Speed (mm/s)

Needle Diameter (µm)

Cell Density (×10⁶ cells/ml)

🧪 Methodology

Dataset preprocessing and normalization

Constraint-aware fitness function design

Genetic Algorithm with:

Selection

Crossover

Mutation

Elitism

Convergence analysis using fitness plots

🖥️ Current Interface

Command Line Interface (CLI)

User-defined constraints entered via terminal

Real-time GA progress displayed per generation

🔮 Future Work

Graphical User Interface (UI)

Material-specific optimization

Multi-objective GA

Integration with bioprinting hardware

📂 Project Structure
biomaterials/
├── data/
│   └── cect-3d-printing-db-all-materials.csv
├── src/
│   └── ga_bioprinting_terminal.py
├── results/
│   └── ga_convergence.png
└── README.md

▶️ How to Run
python src/ga_bioprinting_terminal.py

🛠️ Technologies Used

Python

Pandas

NumPy

Matplotlib

Genetic Algorithms

👩‍🔬 Academic Context

This project is developed as part of Semester IV academic coursework focusing on biomaterials and biofabrication.