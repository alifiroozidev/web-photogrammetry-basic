from os import path
import subprocess
import shutil

class Meshroom(object):

    def __init__(self, inputdir, outputdir):
        """
        Constructor.

        ---
        inputdir: Path to input folder where the images of the model should be.
        outputdir: Path where meshroom will place its output.
        """
        if not path.isdir(inputdir):
            raise Exception(f"{inputdir} is not a directory")
        if not path.isdir(outputdir):
            raise Exception(f"{outputdir} is not a directory")

        # Store the references to the input and output directories
        self._input = inputdir
        self._output = outputdir

    async def run(self, config, pipe):
        """
        Run a simulation with a given configuration file.

        raises: Exception
        ---
        config: Path to JSON file that holds the configuration of a meshroom simulation.
        pipe: Function that receives the output of the program.
        """

        # Check if the given config file exists
        if not path.isfile(config):
            raise Exception(f"Config file {config} does not exist")

        # Check if it's a json file
        if not config.endswith('.json'):
            raise Exception(f"Config file {config} is not a JSON file")

        # Check if meshroom exec is available
        if not path.isfile(path.join('.', 'meshroom', 'meshroom_batch')):
            raise Exception("Meshroom executable is not available")

        # Run the meshroom cli
        process = subprocess.Popen([
            path.join(".", "meshroom", "meshroom_batch"),
            "--inputRecursive", self._input,
            "--output", self._output,
            "--overrides", config,
            "--save", path.join(self._output, "project")
        ], stdout=subprocess.PIPE)

        # Print the output
        while True:

            # Read the current line of the process' output
            output = process.stdout.readline()
            if output == '' and process.poll() is not None:
                break

            # Output the current line
            if output:
                await pipe(output)