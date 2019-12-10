import argparse
import sqlite3

# TODO
# validation for email and phone

# CLI interface
parser = argparse.ArgumentParser()
parser.add_argument("contact", type=str, help="search for contact by name, enter 'list' for all contacts")
parser.add_argument("-a", "--add", action="store_true", help="add contact to the list")
parser.add_argument("-d", "--delete", action="store_true", help="remove contact with the given name")
parser.add_argument("-e", "--edit", action="store_true", help="edit existing contact")
args = parser.parse_args()

# SQLite connection and set up
conn = sqlite3.connect("contacts.db")
c = conn.cursor()

""" Comented out after first run """
# c.execute("""CREATE TABLE contacts (
#             name text,
#             address text,
#             phone_number text,
#             email text
# ) """)


class Contact():
    """class to represent contact in address book"""
    def __init__(self, name):
        self.name = name

    def add_contact(self):
        if self.contact_NOT_in_DB():    
            self.address = input("Address: ")
            self.phone_number = input("Phone number: ")
            self.email = input("Email: ")
            c.execute("INSERT INTO contacts VALUES(:name, :address, :phone, :email)",
                        {"name": self.name, "address": self.address, "phone": self.phone_number, "email": self.email})
            conn.commit()
            conn.close()
            print(f"New contact created: {self.name}, {self.address}, {self.phone_number}, {self.email}")
        else:
            print("Contact already exists")

    def delete_contact(self):
        if not self.contact_NOT_in_DB():
            c.execute("DELETE FROM contacts WHERE name=:name", {"name": self.name})
            confirm = input(f"Do you want to delete {self.name}? (Y/N) ")
            if confirm.lower() == "y":
                conn.commit()
                conn.close()
            elif confirm.lower() == "n":
                print("Action canceled.")
            else:
                print("Wrong input, try again.")
        else:
            print("Contact you wanted to delete doesn't exist.")

    def edit_contact(self):
        if not self.contact_NOT_in_DB():
            item_to_edit = input("What do you want to edit: name, address, phone or email? ")
            if item_to_edit == 'name':
                new_name = input('Enter new name: ')
                c.execute("UPDATE contacts SET name=:new_name WHERE name=:name", {"new_name": new_name, "name": self.name})
                print(f"{self.name} changed to {new_name}")
            elif item_to_edit == 'address':
                new_address = input('Enter new address: ')
                c.execute("UPDATE contacts SET address=:new_address WHERE name=:name", {"new_address": new_address, "name": self.name})
                print(f"Address for {self.name} changed to {new_address}")
            elif item_to_edit == 'phone':
                new_phone = input('Enter new phone number: ')
                c.execute("UPDATE contacts SET phone_number=:new_phone WHERE name=:name", {"new_phone": new_phone, "name": self.name})
                print(f"Phone number for {self.name} changed to {new_phone}")
            elif item_to_edit == 'email':
                new_email = input('Enter new email: ')
                c.execute("UPDATE contacts SET email=:new_email WHERE name=:name", {"new_email": new_email, "name": self.name})
                print(f"Email for {self.name} changed to {new_email}")
            conn.commit()
            conn.close()
        else:
            print("Contact you wanted to edit doesn't exist.")

    def contact_NOT_in_DB(self):
        check = c.execute("SELECT * FROM contacts WHERE name=:name", {"name": self.name})
        if list(check) == []:
            return True
        else:
            return False

        
activeContact = Contact(args.contact)
# add new contact
if args.add:
    activeContact.add_contact()

# remove contact
elif args.delete:
    activeContact.delete_contact()

# edit contact
elif args.edit:
    activeContact.edit_contact()

# print list of all contacts  
elif args.contact == 'list':
    c.execute("SELECT * FROM contacts ORDER BY name")
    found_contacts = c.fetchall()
    for contact in found_contacts:
        print(f"Name: {contact[0]}\nAddress: {contact[1]}\nPhone number: {contact[2]}\nEmail: {contact[3]}\n")

# return data for specific contact name
else:
    c.execute("SELECT * FROM contacts WHERE name=:name", {"name": args.contact})
    found_contacts = c.fetchall()
    if found_contacts == []:
        print("Contact doesn't exist.")
    else:
        for contact in found_contacts:
            print(f"Name: {contact[0]}\nAddress: {contact[1]}\nPhone number: {contact[2]}\nEmail: {contact[3]}\n")
