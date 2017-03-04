#!/usr/bin/env python
# -*-coding: utf-8 -*-

"""
Welcome to Sophia.
Andela's one and only space allocator

Usage:
    sophia create_room <type_of_room> <room_names>...
    sophia add_person <first_name> <surname> (fellow|staff) [<wants_accomodation>]
    sophia (-i | --interactive)
    sophia (-h | --help)
    sophia (-v | --version)
    sophia quit

Arguments:
    <type_of_room>              Choose between a livingspace and an office
    <room_name>                 The name of the room to create
    <first_name>                First name of the new person
    <surname>                   Surnaname of the new person
    (<fellow>|<staff>)          Choose whether the new person is a fellow or staff
    [<wants_accomodation>]      Choose whether the new person wants accomodation

Options:
    -h --help                   Show this screen.
    -i --interactive            Interactive Mode
    -v --version
"""
import os
import sys
import cmd
import signal

from termcolor import cprint, colored
from pyfiglet import figlet_format
from docopt import docopt, DocoptExit

from app import dojorun

def docopt_cmd(func):
    """
    This decorator is used to simplify the try/except block and pass the result
    of the docopt parsing to the called action
    """

    def fn(self, args):
        try:
            opt = docopt(fn.__doc__, args)
        except DocoptExit as error:
            # The DocoptExit is thrown when the args do not match
            print('The command entered is invalid!')
            print(error)
            return
        except SystemExit:
            # The SystemExit exception prints the usage for --help
            return
        return func(self, opt)

    fn.__name__ = func.__name__
    fn.__doc__ = func.__doc__
    fn.__dict__.update(func.__dict__)
    return fn

line = "\n"
doubleline = "\n\n"

os.system("clear")
cprint(figlet_format('SOPHIA', font='chiseled'), 'green', attrs=['bold'])
print(line)
cprint('**************************************************************************', 'magenta')
cprint("\t\tHELLO WORD! This is Sophia, call me Sophy ;)", 'yellow')
cprint("**************************************************************************", 'magenta')
cprint("\n\t\t Type '-h' to see a full list of commands\n", 'white')


class Start(cmd.Cmd):
    """
    This class is what starts Sophia Interactive and makes her WORK

    """

    @docopt_cmd
    def do_create_room(self, args):
        """Usage: create_room <type_of_room> <room_names>..."""
        roomnames = args['<room_names>']
        roomtype = args['<type_of_room>']
        for roomname in roomnames:
            dojorun.create_room(roomname, roomtype)
        
        

    @docopt_cmd
    def do_add_person(self, args):
        """usage: add_person <first_name> <surname> (fellow|staff) [<wants_accomodation>]"""
        firstname = args['<first_name>']
        surname   = args['<surname>']
        category = "fellow" if args["fellow"] is True else "staff"
        accomodation = "Y" if args["<wants_accomodation>"] == "Y" else "NONE" 
        dojorun.add_person(category, firstname, surname, accomodation)


if __name__ == '__main__':
    prompt = Start()
    prompt.prompt = colored('Sophy> ', 'green', attrs=['bold'])
    prompt.cmdloop('Talk to me...')
