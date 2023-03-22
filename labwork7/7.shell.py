from subprocess import Popen, PIPE


class Shell:
    """This class is a shell"""
    def __init__(self):
        self.current_cmd = ""
        self.current_processes = []
        self.ouput_file = None
        self.input_file = None

    def get_cmd(self):
        """Input a cmd from user and return it"""
        self.current_cmd = input("> ").strip()
        return self.current_cmd

    def get_input_output_files(self):
        """Get output redirection file in the cmd"""
        args = self.current_cmd.split(" ")
        self.ouput_file = args[args.index(">") + 1]
        self.input_file = args[args.index("<") + 1]
    
    def remove_redirection(self, redirections):
        """Remove input, output redirections from current cmd
        
        Parameters
        ----------
        redirections : list string of redirection to remove
        """
        for r in redirections:
            self.current_cmd= self.current_cmd.replace(r, "")
        

    def split_cmd(self):
        """Split the cmd into individual processes"""
        try:
            self.get_input_output_files()
            self.remove_redirection()
        except:
            pass    
        self.current_processes = self.current_cmd.split("|")
        self.no_processes = len(self.current_processes)

    def run_processes(self):
        """Run the processes from the cmd"""
        # Get the output file if exist
        redirect_output = open(self.ouput_file, "W") if self.ouput_file else None
        # Get the input file if exist
        previous_process_output = open(self.input_file, "r") if self.input_file else None
        previous_process = None
        # Loop over the processes
        for index, process in enumerate(self.current_processes):
            # Get the args list of the process
            args = process.strip().split(" ")

            # Set stdout to be PIPE if it is not the final process 
            stdout = PIPE if index != self.no_processes - 1 else redirect_output

            # Run the process
            previous_process = Popen(args, stdin=previous_process_output, stdout=stdout, shell=True)
            previous_process_output = previous_process.stdout
        previous_process.wait()
        if redirect_output:
            redirect_output.close()

    def clear(self):
        self.current_cmd = ""
        self.current_processes = []
        self.ouput_file = None
        self.input_file = None

    def main(self):
        """Main function"""

        # Main loop
        while True:
            cmd = self.get_cmd()
            if cmd == "q":
                print("Exited")
                return
            if cmd == "":
                continue

            self.split_cmd()
            self.run_processes()
            self.clear()

if __name__ == "__main__":
    shell = Shell()
    shell.main()