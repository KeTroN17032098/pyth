from cmd import Cmd
import sys
import shutil

class YourCmdSubclass(Cmd):
    def do_dir(*args):
        """delete dir"""
        dir_path=sys.argv[2:][0]
        try:shutil.rmtree(dir_path)
        except: print('Failed to delete')
        return -1

    def do_exit(*args):
        return -1


if __name__ == '__main__':
    c = YourCmdSubclass()
    command = ' '.join(sys.argv[1:])
    if command:
        sys.exit(c.onecmd(command))
    c.cmdloop()