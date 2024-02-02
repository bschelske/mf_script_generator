import xml.etree.ElementTree as ET

def update_frequency(xml_file_path, new_frequency, output_file_path):
    # Parse the XML file
    tree = ET.parse(xml_file_path)
    root = tree.getroot()

    # Find the 'frequency' element and update its value
    for channel in root.iter('channel'):
        frequency_element = channel.find('frequency')
        if frequency_element is not None:
            frequency_element.text = str(new_frequency)

    # Manually write the XML declaration and content to a file
    with open(output_file_path, "w", encoding="utf-8") as file:
        file.write('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n')
        tree = ET.ElementTree(root)
        tree.write(file, encoding="unicode", method="xml")


def create_script(frequencies, ontime, offtime, output_filename):
    # Takes frequencies as a list
    # Update the list to include offtime
    frequencies_with_pause = []
    for item in frequencies:
        frequencies_with_pause.extend([item, 'all_off.xml'])

    # Create the root element
    root = ET.Element("root")

    # Add the 'type' element
    type_element = ET.SubElement(root, "type")
    type_element.text = "Script"

    # Start with everything off
    segment1 = ET.SubElement(root, "segment")
    sequence1 = ET.SubElement(segment1, "sequence")
    sequence1.text = "1"
    filename1 = ET.SubElement(segment1, "filename")
    filename1.text = "all_off.xml"
    runtime1 = ET.SubElement(segment1, "runtime")
    runtime1.text = "1"

    for i, frequency in enumerate(frequencies_with_pause):
        # Create child elements for each segment
        segment = ET.SubElement(root, "segment")
        sequence = ET.SubElement(segment, "sequence")
        sequence.text = str(i + 2)
        filename = ET.SubElement(segment, 'filename')
        filename.text = str(frequency)
        runtime = ET.SubElement(segment, "runtime")
        if frequency == 'all_off.xml':
            runtime.text = str(offtime)
        else:
            runtime.text = str(ontime)

    # Manually write the XML declaration and content to a file
    with open(output_filename, "w", encoding="utf-8") as file:
        file.write('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n')
        tree = ET.ElementTree(root)
        tree.write(file, encoding="unicode", method="xml")


# Example usage
template_file = r'C:\Users\bensc\PycharmProjects\MF_automation\channel_1_20kHz.xml'
output_path = r'C:\Users\bensc\PycharmProjects\MF_automation\output'
ontime = 1
offtime = 1
output_script = output_path+'\\' + 'script.xml'

frequencies = []
for frequency in range(10, 110, 10):
    filename = '\\'+str(frequency)+'kHz.xml'
    output_filename = output_path + filename
    # update_frequency(template_file, frequency, output_filename) # This  makes settings files
    frequencies.append(filename)

create_script(frequencies, ontime, offtime, output_script) # This makes scripts
