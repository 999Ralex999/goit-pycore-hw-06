from collections import UserDict


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    def __init__(self, value):
        if not value:
            raise ValueError("Please enter a valid name")
        super().__init__(value)


class Phone(Field):
    def __init__(self, value):
        if not value.isdigit() or len(value) != 10:
            raise ValueError("Phone must be exactly 10 digits")
        super().__init__(value)


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []

    def add_phone(self, phone: str) -> None:
        """Adds a new phone to the record"""
        self.phones.append(Phone(phone))

    def remove_phone(self, phone: str) -> bool:
        """Removes a phone from the record"""
        for p in self.phones:
            if p.value == phone:
                self.phones.remove(p)
                return True
        return False

    def edit_phone(self, old_phone: str, new_phone: str) -> bool:
        """Edits an existing phone"""
        for i, p in enumerate(self.phones):
            if p.value == old_phone:
                self.phones[i] = Phone(new_phone)  
                return True
        raise ValueError(f"Phone {old_phone} not found in contact")

    def find_phone(self, phone: str) -> str | None:
        """Finds a phone in the list of phones in the record"""
        for p in self.phones:
            if p.value == phone:
                return p.value  

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"


class AddressBook(UserDict):
    def add_record(self, record: Record):
        """Adds a record to the address book"""
        self.data[record.name.value] = record

    def find(self, name: str) -> Record | None:
        """Finds a record by name"""
        return self.data.get(name)

    def delete(self, name: str) -> bool:
        """Removes a contact by name"""
        if name in self.data:
            del self.data[name]
            return True
        return False
