#!/bin/sh /cvmfs/icecube.opensciencegrid.org/py3-v4.3.0/icetray-start
#METAPROJECT icetray/v1.12.1

# --+ Preamble +----------------------------------------------------------------
import os
from icecube import icetray, dataclasses, dataio
from icecube.icetray import I3Tray
from icecube.hdfwriter import I3HDFWriter, I3SimHDFWriter

# Reduce amount of output for icetray to avoid clean up program output.
icetray.logging.set_level(icetray.logging.I3LogLevel.LOG_WARN)

def i32hdf5(
    infile: str, outfile: str, keys: list[str], sevtstrm: list[str] = None
) -> bool:
    """
    Converts one .i3 file into an .hdf5 file, writing a preset list of keys.

    Args:
        infile   : filename for the input i3 file.
        outfile  : filename for the output hdf5 file.
        keys     : list of the keys to write to the hdf5 file.
        sevtstrm : list of strings containing the allowed sub_event_streams. Set
                   to None if input i3 file is from simulation.

        returns  : True if the program was executed successfully, False other-
                   wise.
    """
    # Skip if file has already been converted.
    if os.path.isfile(outfile):
        print("File %s already exists. Skipping..." % outfile)
        return False

    # Prepare tray.
    tray = I3Tray()
    tray.Add("I3Reader", filenamelist = [infile])

    try:
        if sevtstrm is not None:
            tray.Add(
                I3HDFWriter, Keys = keys, SubEventStreams = sevtstrm,
                Output = outfile
            )
        else:
            tray.AddSegment(I3SimHDFWriter, Keys = keys, Output = outfile)
    except RuntimeError as e:
        print(
            "\n\nFailed to setup tray. Maybe output path doesn't exist?"
            "\n\nException:\n%s" % e
        )
        return False

    # Execute and close tray.
    tray.Execute()
    tray.Finish()

    return True
