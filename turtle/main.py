# import another_module
# print(another_module.variable)

# from turtle import Turtle, Screen
# billy = Turtle()
# print(billy)
# billy.shape("turtle")
# billy.color("orange")
# billy.forward(100)
#
# my_screen = Screen()
# my_screen.exitonclick()

import contextlib
import subprocess

# Unix, Windows and old Macintosh end-of-line
newlines = ['\n', '\r\n', '\r']
def unbuffered(proc, stream='stdout'):
    stream = getattr(proc, stream)
    with contextlib.closing(stream):
        while True:
            out = []
            last = stream.read(1)
            # Don't loop forever
            if last == '' and proc.poll() is not None:
                break
            while last not in newlines:
                # Don't loop forever
                if last == '' and proc.poll() is not None:
                    break
                out.append(last)
                last = stream.read(1)
            out = ''.join(out)
            yield out #

def example():
    alias = "deploy-scratch"
    cmd = ['sfdx', 'force:source:deploy', '-w', '33', '-p', 'force-app/main/default', '-u', alias, \
           '-c']
    create_org = ['sfdx', 'force:org:create', '-a', 'deploy-scratch', '-f', 'config/project-scratch-def.json', '-v' \
                  'DevHub', '-w', '33']
    # Execution of the suprocess command will execute the command on a separate thread.
    proc = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        cwd='/Users/josephcorcoran/lwc-recipes',
        # Make all end-of-lines '\n'
        universal_newlines=True,
    )

    some_var = []
    for line in unbuffered(proc):
        some_var.append(line)
        if "=== Component Failures [1]" in line:
            # stop printing once deployment is finished. Only print failures.
            continue
        some_var.append(line)
        print(line)
    print(some_var)


def example_2():
    alias = "deploy-scratch"
    cmd = f"sfdx force:source:deploy -w 33 -p force-app/main/default -c -u {alias} --verbose"

    # Execution of the suprocess command will execute the command on a separate thread.
    proc = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        cwd='/Users/josephcorcoran/lwc-recipes',
        shell = True,
        # Make all end-of-lines '\n'
        universal_newlines=True,
    )

    while True:
        for line in proc.stdout:
            closed_status = proc.stdout.closed
            poll = proc.poll()
            if "===" in line:
                print(line.strip())
                break
            print(line)

    for line in proc.stdout:
        print(line)

    # for line in unbuffered(proc):
    #     print(line)

example()
#example_2()
