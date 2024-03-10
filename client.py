import xmlrpc.client
from datetime import datetime

server_url = "http://localhost:8000"
proxy = xmlrpc.client.ServerProxy(server_url)

def add_note():
    topic_name = input("Enter the topic name: ")
    note_name = input("Enter the note name: ")
    text = input("Enter the note text: ")
    timestamp = datetime.now().strftime("%x - %X")
    result = proxy.add_note(topic_name, note_name, text, timestamp)
    print(result)

def get_notes_by_topic():
    topic_name = input("Enter the topic name to retrieve notes: ")
    notes = proxy.get_notes_by_topic(topic_name)
    if isinstance(notes, list):
        print(f"Notes for topic '{topic_name}':")
        for note_name, text, timestamp in notes:
            print(f"Name: {note_name}\nText: {text}\nTimestamp: {timestamp}\n")
    else:
        print(notes)

def main():
    while True:
        print("\nOptions:\n1. Add a note\n2. Get notes by topic\n3. Exit")
        choice = input("Enter your choice: ")
        if choice == '1':
            add_note()
        elif choice == '2':
            get_notes_by_topic()
        elif choice == '3':
            print("Exiting...")
            break
        else:
            print("Invalid choice, please try again.")

if __name__ == "__main__":
    main()
