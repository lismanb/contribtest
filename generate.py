# generate site from static pages, loosely inspired by Jekyll
# run like this:
#   ./generate.py test/source output
# the generated `output` should be the same as `test/expected_output`

import os
import logging
import jinja2

#added missing imports
import json
import sys

#get the logger for this script (__name__ is the name of the file)
log = logging.getLogger(__name__)

class BadArguments(Exception):
    pass

def list_files(folder_path):
    """
    Loop through the files in the source folder and return one entry each time
    """
    for name in os.listdir(folder_path):
        base, ext = os.path.splitext(name)
        if ext != '.rst':
            continue
        yield os.path.join(folder_path, name)

def read_file(file_path):
    """
    read the contents of a file and construct a dictionary and a string content then return the tuple
    """
    with open(file_path, 'r') as f:
        raw_metadata = ""
        for line in f:
            if line.strip() == '---':
                break
            raw_metadata += line
        content = ""
        for line in f:
            content += line
    return json.loads(raw_metadata), content

def write_output(folder_path, name, html):
    """
    Writes the html buffer into the file that will be created in the folder_path and having the name "name"
    :param folder_path: output path to store the html file
    :type folder_path: str,unicode
    :param name; output file name
    :type name: str,unicode
    :param html: html generated buffer by the jinja template
    :type html: str,unicode
    """
    #creates and overwrites(if exists) the file and writes the buffer inside it
    with open(os.path.join(folder_path + os.sep, name+".html"), "w") as f:
        f.write(html)

def generate_site(folder_path, output_path):
    """
    Sets the jinja template environment and creates the html files from the templates and the .rst content files.
    :param folder_path: path to the source template layout folder
    :type folder_path: str,unicode
    :param output_path: output folder path for saving the generated html files
    :type output_path: str,unicode
    """

    if type(folder_path) is not str and type(folder_path) is not unicode:
        raise TypeError("folder_path must be a valid path string")

    if type(output_path) is not str and type(output_path) is not unicode:
        raise TypeError("output_path must be a valid path string")

    log.info("Generating site from %r", folder_path)

    #path is missing a '/' for layout folder so add it using the separator from os module to be cross platform
    jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(folder_path + os.sep+'layout'),
                                   keep_trailing_newline=True, lstrip_blocks=True, trim_blocks=True)

    #loop trough all the "content" files and generate html files for each of them
    for file_path in list_files(folder_path):

        #read the metadata and the content from file
        metadata, content = read_file(file_path)

        #get the name of the output file
        name, _ = os.path.splitext(os.path.basename(file_path))

        #the metadata dict returned didn't had any key named template, but it had a key named layout
        template_name = metadata['layout']

        #get the template from the environment
        template = jinja_env.get_template(template_name)

        #create the data to be added to the template
        data = dict(metadata, content=content)

        #generate the html page from the template and data provided
        html = template.render(**data)

        #try to create the output folder
        try:
            os.mkdir(output_path)
        except OSError as e:
            log.info(str(e))
            pass

        #write the content to the file
        write_output(output_path, name, html)
        log.info("Writing %r with template %r", output_path, template_name)


def main():
    """
    function called to generate the static html pages
    """

    #pass two arguments , one for template source and one for output path
    if len(sys.argv) != 3:
        raise BadArguments("the script was run with a wrong number of arguments")
    generate_site(sys.argv[1], sys.argv[2])


#if the script is run , configure the logger and start the generation of pages by calling main
if __name__ == '__main__':
    logging.basicConfig()
    main()