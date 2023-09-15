import ipinfo, argparse, sys, requests
from opencage.geocoder import OpenCageGeocode
from colorama import Fore, init

init()

# In this function, we get allow get the user's input from the terminal.
def cl_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-ip", dest="IP_Address", help="Program to Track devices, Use --help to see usage.")
    arguments = parser.parse_args()
    if not arguments.IP_Address:
        print("Please specify an IP address. Defaulting to User's IP Address. Use --help to see usage.\n")
    return arguments


''' In this function, we give an IP address, and it return the details of the IP including the Longitude and Latitude.
    It is this Longitude and Latitude we'd use to get the physical location of the target.'''


def get_ip_location(ip_address):
    try:
        # We start by setting our API token for the IPinfo service.
        token = "Your IPinfo token"

        # Then, we create an IPinfo handler using our token.
        ip_handler = ipinfo.getHandler(token)

        # Then, we get details about the provided IP address using the handler.
        ip_details = ip_handler.getDetails(ip_address)

        # Iterate through all the key-value pairs in the IP details
        for each_key, each_value in ip_details.all.items():
            # Print the key and value in green text. The way they do it in movies :)
            print(f"{Fore.GREEN}{each_key}: {each_value}")

        # Define global variables for latitude and longitude, so we can use them outside this function.
        global latitude, longitude

        # Try to retrieve latitude and longitude from the IP details. So we can pass to open cage for the Phyiscal address.
        try:
            latitude = ip_details.latitude  # Get latitude
            longitude = ip_details.longitude  # Get longitude
        except AttributeError:
            # If latitude and longitude attributes are not found, print a message.
            print("[-] Coordinates for this IP not found. Might be a spoofed IP.")
    except requests.exceptions.HTTPError and requests.exceptions.ConnectionError:
        print("[-] Please ensure you have a stable internet connection and valid API keys.")


# Call our function that gets arguments.
args = cl_arguments()

# Call our get_ip_location function with the provided IP address from command-line arguments.
get_ip_location(args.IP_Address)

# Initialize OpenCageGeocode with our API key.
OCG = OpenCageGeocode('Your Opencage API key')

# Try to reverse geocode the latitude and longitude. This is where we basically get the physical address by reverse geocoding.
try:
    results = OCG.reverse_geocode(latitude, longitude)
except NameError:
    # If latitude or 'longitude' is not defined, exit the program.
    sys.exit()
else:
    # If reverse geocoding is successful, print the accessible location.
    print(f'\n{Fore.RED}The approximate Location is: ', results[0]['formatted'])
