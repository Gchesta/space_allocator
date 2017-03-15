#!/usr/bin/env python
# -*-coding: utf-8 -*-

"""
Welcome to Sophia.
Andela's one and only space allocator

Usage:
    sophia create_room <type_of_room> <room_names>...
    sophia add_person <first_name> <surname> (fellow|staff) [<wants_accomodation>]
    sophia print_room <room_name>
    sophia print_allocations [<filename>]
    sophia rellocate_person <id> <room_name>
    sophia load_people <filename>
    sophia save_state [<filename>]
    sophia load_state <filename>
    sophia exit
    sophia (-i | --interactive)
    sophia (-h | --help)
    sophia (-v | --version)
    sophia quit

Arguments:
    <type_of_room>              Choose between a livingspace and an office
    <room_name>                 The name of the room to create, print or rellocate person to
    <first_name>                First name of the new person
    <surname>                   Surnaname of the new person
    (<fellow>|<staff>)          Choose whether the new person is a fellow or staff
    [<wants_accomodation>]      Choose whether the new person wants accomodation
    [<filename>]                The name of the text file if you want a file to print or load from
    <id>                        The person id 

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

from app import dojo, database
#database = Database()

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
            dojo.create_room(roomname, roomtype)
    
    @docopt_cmd
    def do_add_person(self, args):
        """usage: add_person <first_name> <surname> (fellow|staff) [<wants_accomodation>]"""
        firstname = args['<first_name>']
        surname   = args['<surname>']
        category = "fellow" if args["fellow"] is True else "staff"
        accomodation = str(args["<wants_accomodation>"]).capitalize() if args["<wants_accomodation>"] else "N" 
        dojo.add_person(category, firstname, surname, accomodation)

    @docopt_cmd
    def do_print_room(self, args):
        """usage: print_room <room_name>"""
        roomname = args['<room_name>']
        dojo.print_room(roomname)

    @docopt_cmd
    def do_print_allocations(self, args):
        """usage: print_allocations [<filename>]"""
        filename = args["<filename>"] + ".txt" if args["<filename>"] else False
        dojo.print_allocations(filename)

    @docopt_cmd
    def do_print_unallocated(self, args):
        """usage: print_unallocated [<filename>]"""
        filename = args["<filename>"] + ".txt" if args["<filename>"] else False
        dojo.print_unallocated(filename)

    @docopt_cmd
    def do_rellocate_person(self, args):
        """usage: rellocate_person <id> <room_name>"""
        idno = args['<id>']
        roomname = args["<room_name>"]
        dojo.rellocate_person(idno, roomname)

    @docopt_cmd
    def do_load_people(self, args):
        """usage: load_people <filename>"""
        filename = args["<filename>"] + ".txt"
        dojo.load_people(filename)

    @docopt_cmd
    def do_save_state(self, args):
        """usage: save_state [<filename>]"""
        filename = args["<filename>"] + ".db" if args["<filename>"] else False
        database.save_state(filename)

    @docopt_cmd
    def do_load_state(self, args):
        """usage: load_state <filename>"""
        filename = args["<filename>"] + ".db"
        database.load_state(filename)

    @docopt_cmd
    def do_exit(self, arg):
        """Usage: exit"""
        cprint ("\nSophia says bye...\n", "yellow")
        raise SystemExit(0)

if __name__ == '__main__':
    prompt = Start()
    prompt.prompt = colored('Sophy> ', 'green', attrs=['bold'])
    prompt.cmdloop("\nTalk to me...\n")
