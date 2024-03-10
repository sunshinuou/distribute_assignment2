from xmlrpc.server import SimpleXMLRPCServer, SimpleXMLRPCRequestHandler
import xml.etree.ElementTree as ET
import threading
from socketserver import ThreadingMixIn
import os

class ThreadedXMLRPCServer(ThreadingMixIn, SimpleXMLRPCServer):
    pass

class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/RPC2',)

class NotesServer:
    def __init__(self, host="localhost", port=8000):
        self.server = SimpleXMLRPCServer((host, port), requestHandler=RequestHandler, allow_none=True)
        self.server.register_introspection_functions()
        self.server.register_instance(self)
        self.file_path = "db.xml"
        self.lock = threading.Lock()

    def run(self):
        print(f"Server running on http://{self.server.server_address[0]}:{self.server.server_address[1]}")
        try:
            self.server.serve_forever()
        except KeyboardInterrupt:
            print("Server is shutting down.")
        self.server.server_close()

    def _load_data(self):
        if not os.path.exists(self.file_path):
            return ET.Element("data")
        tree = ET.parse(self.file_path)
        return tree.getroot()

    def _save_data(self, root):
        tree = ET.ElementTree(root)
        tree.write(self.file_path)

    def add_note(self, topic_name, note_name, text, timestamp):
        with self.lock:
            root = self._load_data()
            # check if topic is exist
            topic = root.find(f"./topic[@name='{topic_name}']")
            if topic is not None:
                # check note
                note = topic.find(f"./note[@name='{note_name}']")
                if note is not None:
                    ET.SubElement(note, 'text').text = text
                    ET.SubElement(note, 'timestamp').text = timestamp
                    note[-1].tail = "\n\t\t\t"
                    note[-2].tail = "\n\t\t\t"
                else:
                    note = ET.SubElement(topic, 'note', {'name': note_name})
                    note.text = "\n\t\t\t"
                    ET.SubElement(note, 'text').text = text
                    ET.SubElement(note, 'timestamp').text = timestamp
                    note[-1].tail = "\n\t\t\t"
                    note[-2].tail = "\n\t\t\t"
                    note.tail = "\n\t\t"
            else:
                # create new topic if not exist
                if root[-1].tail and root[-1].tail.strip() == "":
                    root[-1].tail = "\n\t"
                topic = ET.SubElement(root, 'topic', {'name': topic_name})
                topic.text = "\n\t\t"
                note = ET.SubElement(topic, 'note', {'name': note_name})
                note.text = "\n\t\t\t"
                ET.SubElement(note, 'text').text = text
                ET.SubElement(note, 'timestamp').text = timestamp
                note[-1].tail = "\n\t\t\t"
                note[-2].tail = "\n\t\t\t"
                note.tail = "\n\t\t"
                topic[-1].tail = "\n\t"
                topic.tail = "\n"
            root[-1].tail = "\n"
            self._save_data(root)
            return "Note added successfully."

    def get_notes_by_topic(self, topic_name):
        with self.lock:
            root = self._load_data()
            topic = root.find(f"./topic[@name='{topic_name}']")
            if topic is not None:
                return [(note.get('name'), note.find('text').text, note.find('timestamp').text) for note in topic.findall('note')]
            return "No notes found for this topic."

if __name__ == "__main__":
    server = NotesServer()
    server.run()
