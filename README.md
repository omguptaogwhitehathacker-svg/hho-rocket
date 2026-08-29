# HHO Rocket & Acrylic Wet Cell Generator

An experimental propulsion prototype featuring a custom 3mm acrylic wet-cell reactor with 12 carbon rod electrodes, inline flashback safety protection, low-pressure gas storage, and a wireless Raspberry Pi Zero 2 W ignition system powering a curved nozzle rocket engine.

---

## 1. System Overview

The project consists of three core operational modules:

* **Wet Cell Reactor:** 3mm acrylic body housing 12 carbon rod electrodes in a Sodium Hydroxide ($\\text{NaOH}$) solution.
* **Safety & Storage:** Inline flashback arrestor and low-pressure gas storage vessel.
* **Avionics & Propulsion:** Wireless Raspberry Pi Zero 2 W controlling high-voltage arc ignition driving a converging-diverging curved nozzle.

---

## 2. Fuel Generation (Acrylic Arc Reactor)

The electrolyzer reactor uses a sealed 3mm acrylic chamber designed for a submerged wet-cell configuration.

* **3mm Acrylic Housing:** Custom sealed enclosure engineered to hold the liquid electrolyte bath and collect generated gas in the upper headspace.
* **Electrolyte Solution:** Distilled water mixed with Sodium Hydroxide ($\\text{NaOH}$) to maximize electrical conductivity.
* **12 Carbon Rod Array:** 12 submerged carbon rods wired in an alternating parallel circuit ($6\\times \\text{positive}, 6\\times \\text{negative}$) to split water into stoichiometric HHO gas ($2\\text{H}_2\\text{O} \\rightarrow 2\\text{H}_2 + \\text{O}_2$).

```
        +-----------------------------------+
        |          GAS HEADSPACE            |===> HHO Gas Output
        +-----------------------------------+
        |  [+] [-] [+] [-] [+] [-] [+] [-]  |
        |   |   |   |   |   |   |   |   |   |  <-- 12 Carbon Rods
        |   |   |   |   |   |   |   |   |   |      (Submerged)
        |  [NaOH + Distilled Water Solution]|
        +-----------------------------------+
             3mm Acrylic Reactor Chamber
```

---

## 3. Gas Storage & Flashback Safety

To ensure safe gas routing into storage and protect the acrylic cell:

* **Inline Flashback Arrestor:** A metallic porous barrier integrated into the main feed line that quenches flame fronts before fire can reach the acrylic reactor.
* **Low-Pressure Storage Tank:** Collects HHO gas from the reactor and holds it under controlled low pressure until launch.
* **Mechanical Check Valve:** Retains stored gas pressure and prevents backflow.

---

## 4. Wireless Avionics & Rocket Ignition

Ignition is triggered remotely using a wireless micro-controller paired with high-voltage electronics.

* **Raspberry Pi Zero 2 W:** Configured as a wireless node receiving remote trigger commands over Wi-Fi/Bluetooth to pull a GPIO pin high.
* **Arc Ignition System:** The GPIO signal triggers a relay/MOSFET driver linked to a high-voltage step-up module, striking an electric arc across electrodes in the combustion chamber.
* **Curved Converging-Diverging Nozzle:**
  * **Compression:** Smoothly curving inner walls compress expanding hot exhaust gases down to a narrow throat section, building high internal pressure.
  * **Decompression:** The nozzle expands outward after the throat, allowing gas to decompress rapidly and accelerate out to generate forward thrust.

```
       +--------------------+
       |  Combustion Chamber |
       +---------  ---------+
                 \  /        <-- Compression (Curved Converging)
                  ||         <-- Throat
                 /  \        <-- Decompression (Curved Diverging)
                /    \       ===> Supersonic Exhaust Thrust
```

---

## 5. Operational Safety Summary

* **Flashback Protection:** Inline flashback arrestor quenches flame propagation between the storage vessel and the reactor.
* **Wireless Standoff:** Raspberry Pi Zero 2 W allows remote arming and ignition from a safe distance during launch sequences.
