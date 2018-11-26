from arxiv_logs import app
import sys

def main(source_folder):
    print 'Going to process: %s', source_folder
    a = app.ArxivLogApplication('main')
    a.process_folder(source_folder)
    


if __name__ == '__main__':
    if len(sys.argv) <= 1:
        print 'Usage: run.py <source-folder>'
        exit 1
    main(sys.argv[1])
        