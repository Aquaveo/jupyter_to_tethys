# This script programmatically invokes same feature as terminal command "bokeh serve XXXX.py"
# Set a breakpoint in Debug mode to step into Bokeh source code
import sys
import os
from bokeh.command.bootstrap import main

# Change here to switch between sliders_path and nyc_pickup_path
TEST_APP = "nyc_pickup"  # nyc_pickup or sliders

python_interpreter_path = sys.executable
bin_dir = os.path.dirname(python_interpreter_path)
node_path = os.path.join(bin_dir, "node")
os.environ['BOKEH_NODEJS_PATH'] = node_path
base_dir = os.path.dirname(os.path.abspath(__file__))
sample_dir = os.path.join(base_dir, "../embedding/deep/my_django_bokeh_site/djangobokeh/bokeh_apps/")
sliders_path = os.path.join(sample_dir, "sliders.py")
nyc_pickup_path = os.path.join(sample_dir, "nyc_pickup.py")
sys.argv.append("serve")

if TEST_APP == "sliders":
    sys.argv.append(sliders_path)
elif TEST_APP == "nyc_pickup":
    nyc_pickup_data_path = os.path.join(sample_dir, "data", "nyc_taxi_wide.parq")
    if not os.path.isfile(nyc_pickup_data_path):
        print('!' * 30)
        print("Download sample data nyc_taxi_wide.parq at https://s3.amazonaws.com/datashader-data/nyc_taxi_wide.parq")
        print("Put it in folder 'embedding/deep/my_django_bokeh_site/djangobokeh/bokeh_apps/data/'")
        print("And try to run this script again")
        print('!' * 30)
        exit(1)
    sys.argv.append(nyc_pickup_path)

sys.argv.append("--allow-websocket-origin=127.0.0.1:5006")
sys.argv.append("--allow-websocket-origin=localhost:5006")
print(sys.argv)

# Main entry point
main(sys.argv)
