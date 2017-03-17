# space_allocator
-*-coding: utf-8 -*-

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
