import png 
# pip install png
import io
import os
import sys
import time
import argparse
import traceback

# By Icedude907

def main():
    splashtxt = "PNG optmiser by Icedude907."
    caution = "!!!! CAUTION, USING THIS TOOL WITH HDR, ICCP TAGS, etc. WILL REMOVE THEM!"

    parser = argparse.ArgumentParser(description=splashtxt, epilog=caution)
    parser.add_argument("path", help="The directory to start in")
    parser.add_argument("-r", "--recurse", action='store_const', const=True, default=False, help="Process files in subdirectories")
    outgroup = parser.add_mutually_exclusive_group()
    outgroup.add_argument("-w!", "--writeover", action='store_const', const=True, default=False, help="Overwrite image files when a more optimal version is generated")
    # TODO:
    outgroup.add_argument("-o", "--output", metavar="DIR", action='store', help="Specify an output directory to place optimal files into. If relative, based on the current directory.")
    parser.add_argument("--no-skip", action='store_const', const=True, default=False, help="If specified, the new file will be written even if it saves space")

    args = parser.parse_args()

    print(splashtxt)
    print(caution)
    print(args)

     # converts to system notation
    rootpath = os.path.abspath(args.path)
    outpath = rootpath
    if args.output is not None:
        outpath = os.path.abspath(args.output)

    # Truncates the relative path print which is nice
    os.chdir(rootpath)

    sumsaving = 0
    unoptimisablefiles = []
    for curdir, dirs, files in os.walk("."):
        for f in files:
            path = os.path.join(curdir, f)
            if(path.endswith(".png")):
                result = tryreencode(path, args.writeover, args.no_skip, os.path.join(outpath,path))
                if result is not None:
                    sumsaving += result
                else:
                    unoptimisablefiles.append(path)
                print(path)
        print(end="", flush=True)
        if not args.recurse:
            break # Skip subfolders
    

    print("--- DONE WITH THE DIRECTORY ---")
    print("Unoptimisable files: " + str(len(unoptimisablefiles)) + ", " + str(unoptimisablefiles))
    print("Total savings: " + str(sumsaving))

def tryreencode(path, write, no_skip, outfile=None):
    if outfile == None:
        outfile = path

    infs = os.path.getsize(path)

    read = png.Reader(path).read()
    info = read[3]

    # TODO: Make an autopalette tool to identify palettes & eliminate alpha channels if not needed
    # TODO: Same with background

    try:
        writ = png.Writer(compression=9, size=info["size"], greyscale=info["greyscale"], alpha=info["alpha"], 
                          palette=info.get("palette"), bitdepth=info.get("bitdepth"),  # TODO: appropriate depth when creating palettes
        )
        outf = io.BytesIO()
        writ.write(outf, read[2]) # rows
    except: 
        print(traceback.format_exc())
        print(">>> File: " + str(path) + ", " + str(info))
        quit()

    outfs = outf.getbuffer().nbytes
    savings = infs - outfs
    print('{: >6d}'.format(infs) + " -> " + '{: >6d}'.format(outfs), end="")

    if no_skip or savings > 0:
        print("  sav: " + '{: >6d}'.format(-savings), end="\t")
        if write:
            with open(outfile, "wb") as out:
                out.write(outf.getbuffer())
                return savings # break
            print("ERROR: Could not open file {path} for writing!")
        return savings
    else:
        print("  SKIPPED    ", end="\t")
        return None

main()
