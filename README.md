---

# Kriptografia-fiat-shamir-block-chain

This project was developed during my university studies in the Cryptography course. It provides an implementation of the Fiat–Shamir heuristic, a cryptographic technique that transforms interactive proofs into non-interactive ones using a hash function. This method is foundational in creating digital signatures and is integral to various blockchain technologies.

## Project Overview

The repository contains Python scripts that demonstrate key generation and verification processes using the Fiat–Shamir method. The primary focus is on understanding how to generate cryptographic keys and verify them using this heuristic.

## Repository Contents

- `Beadandó(ez leellenőrzi, hogy van-e már kulcs).py`: This script checks for the existence of a key and performs operations accordingly.
- `Kirpto random szamokkal meg for ciklussal.py`: This script utilizes random numbers and loops to demonstrate the cryptographic processes.
- `README.md`: The project description and overview.

## Getting Started

To explore and run the scripts in this project, follow these steps:

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/OcsenasBence/Kriptografia-fiat-shamir-block-chain.git
   cd Kriptografia-fiat-shamir-block-chain
   ```

2. **Ensure Python is Installed**:
   Make sure you have Python installed on your system. You can download it from [python.org](https://www.python.org/).

3. **Run the Scripts**:
   Execute the Python scripts to observe the key generation and verification processes. For example:
   ```bash
   python "Beadandó(ez leellenőrzi, hogy van-e már kulcs).py"
   ```

## Understanding the Fiat–Shamir Heuristic

The Fiat–Shamir heuristic is a cryptographic technique that converts an interactive proof of knowledge into a non-interactive one by replacing the verifier's random challenges with hash function outputs. This approach allows for the creation of digital signatures without the need for interactive communication between the prover and verifier. It's widely used in various cryptographic protocols and blockchain technologies. citeturn0search0

## Acknowledgments

This project was inspired by the foundational concepts in cryptography and aims to provide a practical understanding of the Fiat–Shamir heuristic.

---
