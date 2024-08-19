from sgp4.api import Satrec, WGS72
from sgp4.api import jday
import math

# Path to the TLE file
input_file = 'C:\\Users\\extre\\Documents\\GitHub\\blacksky_elsets.txt'
output_file = 'C:\\Users\\extre\\Documents\\GitHub\\classical_orbital_elements.txt'

def read_tles_from_file(input_file):
    """Reads TLEs from a text file."""
    tles = []
    with open(input_file, 'r') as file:
        lines = file.readlines()
        for i in range(0, len(lines), 3):
            if i+2 < len(lines):
                # Each TLE consists of three lines: the name (optional), line1, and line2
                tles.append((lines[i].strip(), lines[i+1].strip(), lines[i+2].strip()))
    return tles

def convert_to_classical_elements(satellite, jd, fr):
    """Converts SGP4 orbital elements to classical orbital elements."""
    # Get the satellite position and velocity at a specific time
    e, r, v = satellite.sgp4(jd, fr)

    if e != 0:
        raise RuntimeError(f"SGP4 propagation error: {e}")

    # Gravitational constant for Earth (WGS72)
    mu = 398600.8  # km^3/s^2

    # Position and velocity vectors
    rx, ry, rz = r  # in km
    vx, vy, vz = v  # in km/s

    # Compute the classical orbital elements

    # 1. Specific angular momentum (h vector)
    h_x = ry * vz - rz * vy
    h_y = rz * vx - rx * vz
    h_z = rx * vy - ry * vx
    h_mag = math.sqrt(h_x**2 + h_y**2 + h_z**2)

    # 2. Inclination (i)
    inclination = math.degrees(math.acos(h_z / h_mag))

    # 3. Node line vector (n vector)
    n_x = -h_y
    n_y = h_x
    n_z = 0
    n_mag = math.sqrt(n_x**2 + n_y**2)

    # 4. Right Ascension of Ascending Node (RAAN)
    if n_mag != 0:
        raan = math.degrees(math.acos(n_x / n_mag))
        if n_y < 0:
            raan = 360 - raan
    else:
        raan = 0  # RAAN undefined for equatorial orbits

    # 5. Eccentricity vector (e vector)
    r_mag = math.sqrt(rx**2 + ry**2 + rz**2)
    v_mag = math.sqrt(vx**2 + vy**2 + vz**2)
    e_x = (1/mu) * ((v_mag**2 - mu/r_mag) * rx - (rx*vx + ry*vy + rz*vz) * vx)
    e_y = (1/mu) * ((v_mag**2 - mu/r_mag) * ry - (rx*vx + ry*vy + rz*vz) * vy)
    e_z = (1/mu) * ((v_mag**2 - mu/r_mag) * rz - (rx*vx + ry*vy + rz*vz) * vz)
    eccentricity = math.sqrt(e_x**2 + e_y**2 + e_z**2)

    # 6. Argument of Perigee (omega)
    if eccentricity != 0:
        arg_perigee = math.degrees(math.acos((n_x*e_x + n_y*e_y) / (n_mag * eccentricity)))
        if e_z < 0:
            arg_perigee = 360 - arg_perigee
    else:
        arg_perigee = 0  # Argument of perigee undefined for circular orbits

    # 7. True Anomaly (v)
    if eccentricity != 0:
        true_anomaly = math.degrees(math.acos((e_x*rx + e_y*ry + e_z*rz) / (eccentricity * r_mag)))
        if rx*vx + ry*vy + rz*vz < 0:
            true_anomaly = 360 - true_anomaly
    else:
        true_anomaly = 0  # True anomaly undefined for circular orbits

    # 8. Semi-major axis (a)
    semi_major_axis = 1 / ((2/r_mag) - (v_mag**2 / mu))

    return {
        "semi_major_axis": semi_major_axis,
        "eccentricity": eccentricity,
        "inclination": inclination,
        "raan": raan,
        "arg_perigee": arg_perigee,
        "true_anomaly": true_anomaly
    }

def write_classical_elements_to_file(output_file, classical_elements):
    """Writes classical orbital elements to a text file."""
    with open(output_file, 'w') as file:
        for element_set in classical_elements:
            file.write(f"Satellite: {element_set['name']}\n")
            file.write(f"Semi-major axis (km): {element_set['semi_major_axis']}\n")
            file.write(f"Eccentricity: {element_set['eccentricity']}\n")
            file.write(f"Inclination (degrees): {element_set['inclination']}\n")
            file.write(f"RAAN (degrees): {element_set['raan']}\n")
            file.write(f"Argument of perigee (degrees): {element_set['arg_perigee']}\n")
            file.write(f"True anomaly (degrees): {element_set['true_anomaly']}\n")
            file.write("\n")

def process_tles(input_file, output_file):
    """Main function to convert TLEs to classical orbital elements and write to a file."""
    tles = read_tles_from_file(input_file)
    classical_elements = []

    for tle in tles:
        try:
            satellite = Satrec.twoline2rv(tle[1], tle[2], WGS72)
            jd, fr = jday(2024, 1, 1, 0, 0, 0)  # Arbitrary Julian date for conversion
            coe = convert_to_classical_elements(satellite, jd, fr)
            classical_elements.append({"name": tle[0], **coe})
        except RuntimeError as e:
            print(f"Error processing TLE for {tle[0]}: {e}")
            continue  # Skip to the next TLE

    write_classical_elements_to_file(output_file, classical_elements)

# Run the process
process_tles(input_file, output_file)

# Output file path for further use
output_file
