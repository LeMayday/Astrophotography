# Author: Mayday
# Date: 6/29/2024
# inspired by https://docs.astropy.org/en/stable/generated/examples/coordinates/plot_obs-planning.html
# requires matplotlib, numpy, astropy, and jplephem modules

import argparse
import matplotlib.pyplot as plt
import numpy as np
import astropy.units as u
from astropy.coordinates import AltAz, EarthLocation, SkyCoord, get_body
from astropy.time import Time

# determines the time from sunset to midnight and astronomical dark to midnight
def night_half_duration(local_midnight, location):
    # number of points used to estimate sunset
    n = 1000
    # given midnight, we know sunset will occur sometime within the 12 hours prior
    range_to_search = local_midnight + np.linspace(-12, 0, n) * u.hour
    local_frame = AltAz(obstime=range_to_search, location=location)
    # requires jplephem module
    sun = get_body('sun', range_to_search).transform_to(local_frame)
    # set variable = 0 if sunset does not occur over the range
    sunset_to_midnight = (n - np.argmin(np.abs(sun.alt.degree))) / n * 12 if np.argmin(np.abs(sun.alt.degree)) != n - 1 else 0
    # astronomical dark is accepted to occur when the sun is 18 degrees below the horizon
    astro_dark_to_midnight = (n - np.argmin(np.abs(sun.alt.degree + 18))) / n * 12 if np.argmin(np.abs(sun.alt.degree + 18)) != n - 1 else 0
    return sunset_to_midnight, astro_dark_to_midnight

def plot_object(celestial_object, lat, long, date):
    celestial_object_coords = SkyCoord.from_name(celestial_object)
    location = EarthLocation(lat=lat * u.deg, lon=long * u.deg, height = 0 * u.m)

    month, day, year = date.split("/")
    date = Time(year + "-" + month + "-" + day, format='iso', scale='utc')
    # +1 for night of date
    local_midnight = Time(date.to_value('jd', 'float') + 1 - long / 360, format='jd')

    night_half_length, astro_dark_half_length = night_half_duration(local_midnight, location)
    if (night_half_length == 0):
        print("Sun does not set.")
        exit()
    delta_night = np.linspace(-night_half_length, night_half_length, 1000) * u.hour
    local_frame = AltAz(obstime=local_midnight + delta_night, location=location)

    celestial_object_alt_az = celestial_object_coords.transform_to(local_frame)

    fig = plt.figure(figsize = (12, 9))

    plt.plot(delta_night, celestial_object_alt_az.alt.degree, linewidth=2)
    plt.title(celestial_object + " on the night of " + month + "/" + day + "/" + year + " at " + str(lat) + " Lat")
    plt.xlabel('Local Solar Time')
    plt.ylabel('Altitude (degrees)')
    plt.xticks([-night_half_length, -astro_dark_half_length, 0, astro_dark_half_length, night_half_length], 
            ["Sunset", "Astro Dusk", "Midnight", "Astro Dawn", "Sunrise"])
    plt.ylim([0, 90])
    plt.yticks(np.arange(0, 91, 15))

    plt.savefig(celestial_object.replace(" ", "_") + "_altitude_" + month + "_" + day + "_" + year)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-n', '--name', required=True, help="Name of object")
    parser.add_argument('-l', '--latitude', required=True, type=float, help="Latitude as decimal degrees")
    # parser.add_argument('-m', '--meridian', required=True, type=float, help="Longitude (meridian) as decimal degrees")
    parser.add_argument('-d', '--date', required=True, help="Date of the observation")
    args = parser.parse_args()

    plot_object(args.name, args.latitude, 0, args.date)

if __name__ == "__main__":
    main()
