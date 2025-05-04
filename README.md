
# WiFi Distance & Trilateration Tool

This project contains three scripts developed for a practical session focusing on Wi-Fi signal-based distance estimation and trilateration using Python.

## 🔧 Features

- 📶 **Signal Strength Detection**: Uses `netsh` command to extract available SSIDs and their signal strength.
- 📏 **Distance Estimation**: Converts RSSI percentage to distance in meters using a log-distance path loss model.
- 📍 **Trilateration Plotting**: Graphically determines the estimated position of a device relative to 3 access points.
- 🖥️ **Graphical Interface**: Provides a GUI to visualize distances in real time.

## 📁 File Descriptions

- `calculdistancetp3q1.py`: Command-line script to calculate distance from a single access point.
- `3pointsaccestp3q2.py`: Trilateration of mobile position based on 3 manually entered SSIDs.
- `interfacetp3q3.py`: Graphical Tkinter interface to interact with access points and visualize signal strengths and distances.

## 💻 Requirements

- Python 3.x
- `matplotlib`
- `numpy`
- `sympy` (optional)

## 🚀 How to Run

```bash
python calculdistancetp3q1.py
python 3pointsaccestp3q2.py
python interfacetp3q3.py
```

> ⚠️ **Note**: This script uses the Windows `netsh` command and must be run on a Windows machine with Wi-Fi enabled.

## 📜 License

MIT License.

---

# Outil de Mesure de Distance & Trilatération Wi-Fi

Ce projet contient trois scripts Python développés dans le cadre d’un TP portant sur l'estimation de distance via Wi-Fi et la trilatération.

## 🔧 Fonctionnalités

- 📶 **Détection de la puissance du signal** : Utilise `netsh` pour extraire les SSIDs disponibles et leur puissance.
- 📏 **Estimation de distance** : Convertit le pourcentage RSSI en distance en mètres via un modèle de perte de signal.
- 📍 **Trilatération** : Affichage graphique de la position estimée à partir de 3 points d'accès.
- 🖥️ **Interface graphique** : Interface Tkinter pour visualiser les distances en temps réel.

## 📁 Description des fichiers

- `calculdistancetp3q1.py` : Script pour calculer la distance à un seul point d'accès.
- `3pointsaccestp3q2.py` : Trilatération basée sur 3 SSID entrés manuellement.
- `interfacetp3q3.py` : Interface graphique avec affichage des distances.

## 💻 Prérequis

- Python 3.x
- `matplotlib`
- `numpy`
- `sympy` (optionnel)

## 🚀 Exécution

```bash
python calculdistancetp3q1.py
python 3pointsaccestp3q2.py
python interfacetp3q3.py
```

> ⚠️ **Attention** : Ce script utilise la commande `netsh` et doit être exécuté sous Windows avec le Wi-Fi activé.

## 📜 Licence

Licence MIT.
