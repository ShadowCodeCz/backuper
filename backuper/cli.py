import os.path
import zipfile
import datetime
import shutil
from . import app_core
import alphabetic_timestamp as ats


def backup(arguments):
    if os.path.isfile(arguments.path):
        backuper = FileBackuperCommand()
        backuper.run(arguments)
    if os.path.isdir(arguments.path):
        backuper = DirectoryBackuperCommand()
        backuper.run(arguments)


class FileBackuperCommand:
    def __init__(self):
        self.arguments = None
        self.ac = app_core.AppCore()

    def run(self, arguments):
        self.arguments = arguments
        output_path = self.output_path()
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        with zipfile.ZipFile(output_path, "w") as zipf:
            zipf.write(arguments.path)

        if os.path.exists(output_path):
            self.ac.logger().info(f"src: {self.arguments.path}")
            self.ac.logger().info(f"dst: {output_path}")

        if self.arguments.remove:
            os.remove(self.arguments.path)

    def output_path(self):
        filename = os.path.basename(self.arguments.path)
        ats_now = ats.base36.now()

        ats_filename = f"{ats_now}-{filename}.zip"

        template = os.path.join(
            self.arguments.output_dir,
            ats_filename
        )

        return datetime.datetime.now().strftime(template)


class DirectoryBackuperCommand:
    def __init__(self):
        self.arguments = None
        self.ac = app_core.AppCore()

    def run(self, arguments):
        self.arguments = arguments

        output_path = self.output_path()
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        shutil.make_archive(output_path, "zip", self.arguments.path)

        if os.path.exists(f"{output_path}.zip"):
            self.ac.logger().info(f"src: {self.arguments.path}")
            self.ac.logger().info(f"dst: {output_path}")

        if self.arguments.remove:
            if (os.path.normpath(self.arguments.path) == os.path.normpath(os.getcwd())):
                os.chdir(os.path.dirname(os.path.abspath(self.arguments.path)))
            shutil.rmtree(self.arguments.path)

    def output_path(self):
        _, dir_name = os.path.split(os.path.abspath(self.arguments.path))
        ats_now = ats.base36.now()

        ats_dirname = f"{ats_now}-{dir_name}.zip"

        template = os.path.join(
            self.arguments.output_dir,
            ats_dirname
        )

        return datetime.datetime.now().strftime(template)

