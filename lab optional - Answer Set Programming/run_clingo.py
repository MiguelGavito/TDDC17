import sys
from clingo.application import Application, clingo_main

class Clingo(Application):
    def __init__(self):
        self.program_name = "simple-clingo"
    
    def main(self, ctl, files):
        """
        Main entry point: loads ASP file(s), grounds, and solves.
        """
        # Load each file specified in the command line.
        for f in files:
            ctl.load(f)
        # If no files given, load from stdin.
        if not files:
            ctl.load("-")
        # Ground the 'base' part.
        ctl.ground([("base", [])])
        # Solve and print answer sets to stdout.
        ctl.solve()

if __name__ == "__main__":
    # Pass command line arguments (except script name)
    clingo_main(Clingo(), sys.argv[1:])
