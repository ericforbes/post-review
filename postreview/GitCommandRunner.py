import subprocess
import sys

class GitCommandRunner():

    @staticmethod
    def remove_api_token(config_key):
        return run_cmd("git config --unset %s" % config_key).strip()

    @staticmethod
    def get_api_token(config_key):
        return run_cmd("git config %s" % config_key).strip()

    @staticmethod
    def add_api_token(config_key, val):
        return run_cmd("git config %s %s" % (config_key, val))

    @staticmethod
    def get_last_commit_msg():
        return run_cmd("git log -1 --pretty=%B").strip()

    @staticmethod
    def inside_working_tree():
        in_git_tree = run_cmd("git rev-parse --is-inside-work-tree").strip()
        if in_git_tree == 'true':
            return True
        return False

    @staticmethod
    def get_current_branch():
        branch = run_cmd("git rev-parse --abbrev-ref HEAD").rstrip()
        if 'fatal: Not a git repository' in branch:
            sys.stderr.write("Unable to determine current git branch: git rev-parse --abbrev-ref HEAD\n")
            sys.exit()

        return branch

    @staticmethod
    def get_remote_origin_url():
        return run_cmd("git config --get remote.origin.url").rstrip()

    @staticmethod
    def push_branch_to_remote(source):
        cmd = "git push origin HEAD:%s" % source
        u = raw_input("\n\nPushing local branch [%s] to remote [%s],  Yes or no? " % (source, source))
        if u.lower() != 'yes' and u.lower() != 'y':
            sys.stderr.write("Exiting...\n")
            sys.exit()

        output = run_cmd(cmd)
        sys.stderr.write(output)
        sys.stderr.write("\n")

def run_cmd(cmd):
    cmd_list = cmd.split()
    try:
        p = subprocess.Popen(
        cmd_list,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE)
        output = p.communicate()

        if not output[0]:
            return output[1]
        return output[0]

    except OSError as e:
        sys.stderr.write("Fatal: '%s' is either not in your path or is not installed\n" % cmd_list[0])
        sys.exit()
    except IndexError as e:
        sys.stderr.write("Error: Unexpected response from `%s`\n" % cmd)
        sys.exit()