
class Config:

    def __init__(self):
        self.python_version = "3.11"
        self.indentation = 2
        self.case_sensitive = False
    
    def set_python_version(self, version):
        self.python_version = version

    def set_indentation(self, indentation):
        self.indentation = indentation

    def set_case_sensitive(self, sens):
        self.case_sensitive = sens


def parse_config(lines):
    config = Config() # default config
    for line in lines[:4]:
        try:
            splt = line.split("=")
            key = splt[0].strip()
            val = splt[1].strip()
            match key:
                case "python_version":
                    config.set_python_version(val)
                case "indentation":
                    config.set_indentation(int(val))
                case "case_sensitive":
                    match val:
                        case "false":
                            val = False
                        case "true":
                            val = True
                    config.set_case_sensitive(val)
            lines.remove(line)
        except IndexError:
            # the line might not be a configuration line
            pass
    return (config, lines)
