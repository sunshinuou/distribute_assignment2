import xmlrpc.client
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime

server_url = "http://localhost:8000"


def add_note(topic_name, note_name, text, timestamp):
    with xmlrpc.client.ServerProxy(server_url) as proxy:
        proxy.add_note(topic_name, note_name, text, timestamp)


def simulate_concurrent_requests(num_requests):
    with ThreadPoolExecutor(max_workers=num_requests) as executor:
        for i in range(num_requests):
            timestamp = datetime.now().strftime("%x - %X")
            executor.submit(add_note, f"Topic {i}", f"Note {i}",
                            "This is the text for the note.", timestamp)

if __name__ == "__main__":
    simulate_concurrent_requests(5)
