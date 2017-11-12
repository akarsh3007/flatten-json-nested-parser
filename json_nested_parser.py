import json
import os, errno
import os.path
import shutil
class JsonNestedParser:
    #"parser for JSON and its nested object flattening all nested objects"
    #construtor takes file path and output directory name
    def __init__(self, filepath, dir="output"):
        self.filepath = filepath
        self.dir = dir
        # check if file exists
        if not os.path.isfile(self.filepath):
            print "File does not exists at " + self.filepath
            exit()
        # check if folder exists, delete and create new folder
        if not os.path.exists(dir):
            os.makedirs(dir,0777)
        else:
            shutil.rmtree(dir)
            os.makedirs(dir,0777)
    #method to initate parsing
    def read_json_from_file(self):
        f = open(self.filepath,"r")
        # check if the json is valid
        try:
            data = json.load(f)
        except ValueError:
            print "File does not contain a valid JSON"
            exit()
        print "Please wait. Parsing file"
        for values in data[data.keys()[0]]:
            self.parse_json(data.keys()[0],values,-1,values['id'])
        f.close()
        print "Parsing Completed. Output files are in " + self.dir + " folder"

    # method to recusrively traverse json objects
    def parse_json(self,name,data,index,_id):
        if os.path.isfile(self.dir+'/%s.json' % str(name)):
            output = open(self.dir+'/%s.json' % str(name),"r+")
            outputStr=output.read()
            outputStr=outputStr[:-1]
            output.seek(0)
            output.truncate()
            output.write(outputStr)
            output.close()
        output = open(self.dir+'/%s.json' % str(name),"a+")
        out={}
        if os.stat(self.dir+'/%s.json' % str(name)).st_size != 0:
            output.seek(-1,2)
            output.write(",")
        else:
            output.write("[\n")
        out['id'] = _id
        if(index!=-1):
            out['__index']=index
        out['id'] = _id
        for field in data:
            if type(data[field]) == dict:
                self.parse_json(name+'_'+field,data[field],index,_id)
            elif type(data[field]) == list:
                i=0
                for entry in data[field]:
                    if(type(entry)!=dict):
                        break;
                    self.parse_json(name+'_'+field,entry,i,_id)
                    i=i+1
                out[field] = data[field]
            else:
                out[field]=data[field]
        output.write(str(json.dumps(out)))
        output.write("\n]")
        output.close()

class Runner:
    #main method
    if __name__ == '__main__':
        # read input from console.
        filepath = raw_input("filepath: ")
        output_folder = raw_input("output folder: ")
        json_parser = JsonNestedParser(filepath,output_folder)
        json_parser.read_json_from_file()
