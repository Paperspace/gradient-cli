import os
import sys

from .cli import cli
from .jobs import run, print_json_pretty
from .login import login, logout, set_apikey
from .version import version


def main():
    if len(sys.argv) >= 2 and sys.argv[1] in ('experiments', 'deployments', 'machines'):
        cli(sys.argv[1:])

    args = sys.argv[:]
    prog = os.path.basename(args.pop(0))

    if not args:
        usage(prog)
        sys.exit(1)

    cmd = args.pop(0)

    help_opts = ['help', '--help', '-h']

    if cmd in help_opts:
        usage(prog)
        sys.exit(0)

    if cmd in ['version', '--version', '-v']:
        vers(prog)
        sys.exit(0)

    if cmd == 'login':
        email = None
        password = None
        apiToken = None
        while args:
            opt = args.pop(0)
            if opt in help_opts:
                print('usage: %s' % login_usage(prog))
                sys.exit(0)
            elif opt == '--email':
                email = args.pop(0) if args else None
            elif opt == '--password':
                password = args.pop(0) if args else None
            elif opt == '--apiToken':
                apiToken = args.pop(0) if args else None
            elif not email:
                email = opt
            elif not password:
                password = opt
            elif not apiToken:
                apiToken = opt
        return not login(email, password, apiToken)

    if cmd == 'logout':
        if args:
            print('usage: %s logout' % prog)
            sys.exit(not (args[0] in help_opts))
        return not logout()

    if cmd == 'apikey' or cmd == 'apiKey':
        if not args or args[0] in help_opts:
            print('usage: %s' % apikey_usage(prog))
            sys.exit(not args)
        return not set_apikey(args[0])

    if cmd == 'run':
        if not args or args[0] in help_opts:
            print('run usage: %s' % run_usage(prog))
            sys.exit(not args)
        params = {}
        skip_arg_processing = False
        while args:
            opt = args.pop(0)
            if opt == '-':
                skip_arg_processing = True
            elif opt.startswith('--') and not skip_arg_processing:
                param = opt[2:]
                if param in ['script', 'python', 'conda', 'ignoreFiles', 'apiKey', 'container', 'machineType', 'name',
                             'project', 'projectId', 'command', 'workspace', 'dataset', 'registryUsername',
                             'registryPassword', 'workspaceUsername', 'workspacePassword', 'cluster', 'clusterId',
                             'ports', 'isPreemptible', 'useDockerfile', 'buildOnly', 'registryTarget',
                             'registryTargetUsername', 'registryTargetPassword', 'relDockerfilePath', 'customMetrics', 'modelType', 'modelPath']:
                    if args and not args[0].startswith('--'):
                        params[param] = args.pop(0)
                    else:
                        print('error: missing argument for %s' % opt)
                        print('usage: %s' % run_usage(prog))
                        sys.exit(1)
                elif param in ['init', 'req']:
                    params[param] = True
                    if args and not args[0].startswith('-') and not args[0].endswith('.py'):
                        params[param] = args.pop(0)
                elif param in ['no_logging', 'nologging', 'noLogging', 'json']:
                    params['no_logging'] = True
                elif param in ['dryrun', 'pipenv']:
                    params[param] = True
                else:
                    print('error: invalid option: %s' % opt)
                    print('usage: %s' % run_usage(prog))
                    sys.exit(1)
            elif opt == '-m' and not skip_arg_processing:
                params['run_module'] = True
                skip_arg_processing = True
            elif opt == '-c' and not skip_arg_processing:
                params['run_command'] = True
                skip_arg_processing = True
            elif 'script' not in params:
                params['script'] = opt
            else:
                if 'script_args' not in params:
                    params['script_args'] = [opt]
                else:
                    params['script_args'].append(opt)
        res = run(params)
        if 'error' in res:
            print_json_pretty(res)
            sys.exit(1)
        sys.exit(0)

    print('error: invalid command: %s' % cmd)
    usage(prog)
    sys.exit(1)


def vers(prog):
    print('%s %s' % (prog, version))


def login_usage(prog):
    return format('%s login [[--email] <user@domain.com>] [[--password] "<secretpw>"] [[--apiToken] "<api token name>"]\n       %s logout' % (prog, prog))


def apikey_usage(prog):
    return format('%s apikey <api_key>' % prog)


def run_usage(prog):
    return format('%s run [options] [[-m] <script> [args] | -c "python code" | --command "shell cmd"]\n'
        '    options:\n'
        '    [--python 2|3]\n'
        '    [--init [<init.sh>]]\n'
        '    [--pipenv]\n'
        '    [--req [<requirements.txt>]]\n'
        '    [--workspace .|<workspace_path>]\n'
        '    [--ignoreFiles "<file-or-dir>,..."]\n'
        '    [jobs create options]\n'
        '    [--dryrun]\n'
        '    [-]' % prog)


def experiments_usage(prog):
    return "{} experiments <command>   Manage experiments".format(prog)


def deployments_usage(prog):
    return "{} deployments <command>   Manage deployments".format(prog)


def machines_usage(prog):
    return "{} machines <command>   Manage machines".format(prog)


def usage(prog):
    print('usage: %s' % login_usage(prog))
    print('       %s' % apikey_usage(prog))
    print('       %s' % run_usage(prog))
    print('       %s' % experiments_usage(prog))
    print('       %s' % deployments_usage(prog))
    print('       %s' % machines_usage(prog))
    print('       %s version' % prog)
