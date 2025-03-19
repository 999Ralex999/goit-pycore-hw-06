
from address_book_module import AddressBook, Record

address_book = AddressBook()


def main():
    """Main function to run the assistant bot with a command loop"""
    print("Welcome to the assistant bot!")
    commands = {
        "hello": greet,
        "add": add_contact,
        "change": change_contact,
        "phone": show_phone,
        "all": show_all,
        "delete": delete_contact,  
        "close": goodbye,
        "exit": goodbye
    }

    while True:
        user_input = input("Enter a command: ")
        try:
            cmd, *args = parse_input(user_input)
            if cmd in commands:
                print(commands[cmd](*args))
                if cmd in ["close", "exit"]:
                    break
            else:
                print("Invalid command. Available commands: ", ", ".join(commands.keys()))
        except Exception as e:
            print(f"Error: {e}")


def input_error(ValueErrorMessage="Give me name and phone please.", 
                IndexErrorMessage="Give me name and phone please.", 
                KeyErrorMessage="Please enter a valid key"):
    """Decorator to handle input errors with different messages"""
    def input_error_closure(func):
        def inner(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except ValueError:
                return ValueErrorMessage
            except KeyError:
                return KeyErrorMessage
            except IndexError:
                return IndexErrorMessage
        return inner
    return input_error_closure


def parse_input(input_str: str):
    """Parse user input into command and arguments"""
    cmd, *args = input_str.split()
    return cmd.strip().lower(), *args


@input_error(ValueErrorMessage="Give me name and phone please.")
def add_contact(*args):
    """Add a new contact to the contacts dictionary"""
    name, phone = args
    record = Record(name)
    if address_book.find(name):
        return "Contact already exists."
    else:
        record.add_phone(phone)
        address_book.add_record(record)
        return "Contact added."


@input_error(ValueErrorMessage="Give me name and phone please.")
def change_contact(*args):
    """Update an existing contact's phone number"""
    name, old_phone, new_phone = args
    contact = address_book.find(name)
    if contact is None:
        return "Contact not found."
    
    if contact.find_phone(old_phone):
        contact.edit_phone(old_phone, new_phone)
        return f"Phone {old_phone} changed to {new_phone} for {name}."
    else:
        return f"Phone {old_phone} not found for {name}."


@input_error(ValueErrorMessage="Give me name please.", IndexErrorMessage="Give me name please.")
def show_phone(*args):
    """Show the phone number for a specific contact"""
    name = args[0]
    contact = address_book.find(name)
    if contact is None:
        return "Contact not found."
    elif not contact.phones:
        return "No phone numbers found for this contact."
    return contact.phones[0].value


def show_all():
    """Show all contacts in the address book"""
    return "\n".join([f"{contact.name} - {', '.join(p.value for p in contact.phones)}" for contact in address_book.data.values()])


@input_error(ValueErrorMessage="Give me name please.")
def delete_contact(*args):
    """Delete a contact from the address book"""
    name = args[0]
    if address_book.delete(name):
        return f"Contact {name} deleted."
    return "Contact not found."


def greet():
    """Return a greeting message"""
    return "How can I help you?"


def goodbye():
    """Return a farewell message"""
    return "Goodbye!"


if __name__ == "__main__":
    main()

