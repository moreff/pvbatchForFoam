import os.path
import argparse
import numpy as np

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

def check_file_exists(path):
    if not os.path.isfile(foamfoam_path):
        sys.stderr.write("\"" + path + "\" not found!")
        quit()

parser = argparse.ArgumentParser(description='Creates a series of screenshots of a paraview state.')
parser.add_argument(dest='pvsm_path',
                    help='a path to .pvsm file')
parser.add_argument('--output', default=None,
                    help='path to output file (default - name of the .pvsm'\
                         ' file). A number of a screenshot will be added in'\
                         ' the end of the filename after "_"')
parser.add_argument('--path', dest='input', default='.',
                    help='path to case folder, where foam.foam file is located'\
                         ' (default=.)')

args = parser.parse_args()

foamfoam_path = os.path.join(args.input,'foam.foam')

check_file_exists(foamfoam_path)
check_file_exists(args.pvsm_path)
check_file_exists(os.path.join(args.input, "system", "controlDict"))

if args.output is None:
    args.output = str(args.pvsm_path[:-5]) + "_"



from paraview.simple import *
paraview.simple._DisableFirstRenderCameraReset()
renderView1 = GetActiveViewOrCreate('RenderView')
Delete(renderView1)
del renderView1

LoadState(args.pvsm_path, LoadStateDataFileOptions='Choose File Names',
    DataDirectory=args.input)
    # foamfoamFileName=args.input+'/foam.foam')

animationScene1 = GetAnimationScene()
layout1 = GetLayout()

i = 0
# print(animationScene1.StartTime)
# print(animationScene1.EndTime)

timeKeeper1 = GetTimeKeeper()

# animationScene1.GoToFirst() # doesn't work
# animationScene1.AnimationTime = animationScene1.StartTime
for time in timeKeeper1.TimestepValues:
    # save screenshot
    animationScene1.AnimationTime = time
    filename = args.output + "%04d"%i + ".png"
    print("Saving screenshot \"" + filename + "\" for time = " +
          str(animationScene1.AnimationTime))
    SaveScreenshot(filename, layout1, SaveAllViews=1,
        CompressionLevel='5')

    # animationScene1.GoToNext() # doesn't work
    i+=1
