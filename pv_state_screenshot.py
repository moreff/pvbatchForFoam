import os.path
import sys
import argparse
import numpy as np

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

def get_latestTime(path):
    times = [float(d) for d in os.listdir(path) if os.path.isdir(os.path.join(path, d)) and is_number(d)]
    times.sort()
    return times[-1]

def check_file_exists(path):
    if not os.path.isfile(foamfoam_path):
        sys.stderr.write("\"" + path + "\" not found!")
        quit()

parser = argparse.ArgumentParser(description='Creates a screenshot of a'\
                                             ' paraview state.')
parser.add_argument(dest='pvsm_path',
                    help='a path to .pvsm file')
parser.add_argument('--output', default=None,
                    help='path to output file (default - name of the .pvsm'\
                         ' file)')
parser.add_argument('--path', dest='input', default='.',
                    help='path to case folder, where foam.foam file is located'\
                         ' (default=.)')
parser.add_argument('--time', dest='myTimestep', default=None,
                    help='time instance to depict (default = latestTime)')

args = parser.parse_args()

foamfoam_path = os.path.join(args.input,'foam.foam')

check_file_exists(foamfoam_path)
check_file_exists(args.pvsm_path)
check_file_exists(os.path.join(args.input, "system", "controlDict"))

if args.myTimestep is None:
    args.myTimestep = get_latestTime(args.input)

if args.output is None:
    args.output = str(args.pvsm_path[:-5]) + "_" + str(args.myTimestep) + ".png"



from paraview.simple import *
paraview.simple._DisableFirstRenderCameraReset()
renderView1 = GetActiveViewOrCreate('RenderView')
Delete(renderView1)
del renderView1

LoadState(args.pvsm_path, LoadStateDataFileOptions='Choose File Names',
    DataDirectory=args.input)
    # foamfoamFileName=foamfoam_path)

animationScene1 = GetAnimationScene()
animationScene1.AnimationTime = float(args.myTimestep)

layout1 = GetLayout()

print("Saving screenshot \"" + args.output + "\"")
SaveScreenshot(args.output, layout1, SaveAllViews=1, CompressionLevel='5')
