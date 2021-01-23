import sys
import os
from pathlib import Path
from cliff.app import App
from cliff.commandmanager import CommandManager

from ifn_standards.utils import read_yaml
from ifn_standards.commands import get_commands

class MyApp(App):
    
    def build_option_parser(self, description, version):
        parser = super(MyApp, self).build_option_parser(
            description,
            version,
        )

        parser.add_argument(
            "-c",
            "--config",
            help="Config path",
            default=os.path.join('config.yaml')
        )

        self._configs = {}
        return parser

    def initialize_app(self, argv):
        commands = get_commands()
        for command in commands:
            if hasattr(command, 'name'):
                name = command.name
            else:
                name = command.__name__
            self.command_manager.add_command(name.lower(), command)

    def load_config(self):
        cfg_path = self.options.config
        if not Path(cfg_path).is_file():
            raise Exception("Unable to find config file at %s" % (cfg_path,))
        try:
            self._configs = read_yaml(cfg_path)
        except:
            print("Unable to load configuration file")
            raise


    def prepare_to_run_command(self, cmd):
        # self.load_config()
        pass

    def get_app_path(self):
        path = os.path.dirname(os.path.abspath(__file__))
        return path

    def get_schemas_path(self):
        return os.path.abspath(self.get_app_path() + '/../../schemas')

def main(argv=sys.argv[1:]):
    app = MyApp(
            description="InfluenzaNet Standards CLI",
            version="0.0.1",
            command_manager=CommandManager('ifn_standards'),
            deferred_help=True,
        )
    return app.run(argv)


if __name__ == '__main__':
    sys.exit(main())