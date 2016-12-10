from time import strftime
import pymongo
import json
import re

# Model for the JSON file arapaho data is currently stored in

# json_path: local path to the json_file to be loaded, and written to
# log_path: local path to atxt file, which does not have to exist yet, to which the updates will be logged

class JsonLexicon:

  def __init__(self, json_path, log_path):

    with open(json_path) as data_file:
      self.data = json.load(data_file)
      json_path_name = json_path.split('.json')[0]
      new_json_path = "%s_%s.%s" %(json_path_name, strftime("%Y_%m_%d_%H_%M_%S"), ".json")
      self.json_file = open(new_json_path, "w")
      self.log_file = open(log_path, "w")

  def next_lex_id(self):
    lexicon = self.data
    klist = []

    for k in lexicon.keys():
        klist.append(int(k.replace('L','')))

    return "L%s" % str(sorted(klist)[-1] + 1)

  # Add the new entry to local lexicon and add them to a txt file
  # Accepts an array of flat dictionaries of the features that the new_lex_id will point to
  def add_to_lexicon(self, new_entries = []):
    lex_id = self.next_lex_id()

    for new_entry in new_entries:
      # For txt log, print lex_id at top of section
      self.log_file.write("%s:" % lex_id)
      for entry_key in lexicon_keys:
        self.data.setdefault(lex_id, {entry_key: ""})
        self.data[lex_id][entry_key] = new_entry.get(entry_key, "")

        # Write to txt file and encode strings utf-8
        if entry_key == "senses":
          self.log_file.write("\t %s: \t %s \n" % ("definition", new_entry["senses"][0]["definition"].encode('utf-8')))
        elif isinstance(new_entry.get(entry_key, ""), basestring):
          self.log_file.write("\t %s: \t %s \n" % (entry_key.encode('utf-8'), new_entry.get(entry_key, "").encode('utf-8')))
        else:
          self.log_file.write("\t %s: \t %s \n" % (entry_key.encode('utf-8'), new_entry.get(entry_key, "")))
      self.log_file.write("\n\n")
      # Increment for the next lex_id
      lex_id = "L%s" % str(int(lex_id.replace('L',''))+1)

    self.log_file.flush()
    self.json_file.write(json.dumps(self.data))

  def update_lexicon():
    return ""


# Connects to the mongodb and gives an interface to query it
# And return LexicalEntry objects

class MongoLexicon:

  def __init__(self):
    # Connection to Mongo DB
    try:
        conn=pymongo.MongoClient()
        print "Connected successfully"
    except pymongo.errors.ConnectionFailure, e:
        print "Could not connect to MongoDB: %s" % e

    # Connect to DB and define var for lexicon collection
    self.db = conn.arapaho

  # Method for getting multiple form class
  def find_lexical_entries(self, args={}):
      results = self.db.lexicon.find(args)
      entries_array = []

      for result in results:
        entries_array.append(LexicalEntry(result))

      return entries_array

  def refresh_from_json(self, lexicon_path):
      # Delete current db
      self.db.lexicon.remove()

      # Find up-to-date json file
      with open(lexicon_path) as data_file:
        arapaho_lexicon = json.load(data_file)

      # List of json objects, 1 for each entry
      original_lexicon_list = []
      # Remove the keys, so that each json object can be indexed and given a mongo _id
      # Store the keys (lex_id) in the flat json object for later reference
      for lex_id in arapaho_lexicon:
        entry = arapaho_lexicon[lex_id]
        a = {}
        for key in entry.keys():
            a[key] = entry[key]
        # Store this info in order to reference the original JSON
        a["lex_id"] = lex_id
        original_lexicon_list.append(a)

      # Formatting json
      entries_json = json.dumps(original_lexicon_list)
      entries = json.loads(entries_json)

      for entry in entries:
        # mongo preprocessing, remove '.' from keys, replace with '-'
        d = entry.get("derivations")
        if isinstance(d, dict):
          for key in d.keys():
              d[re.sub("\.", "-", key)] = d.pop(key)
              entry["derivations"] = d

        # Insert into new collection
        result = self.db.lexicon.insert_one(entry)

# This class serves to allow me to more easily interface with the json object.
# Here you can find existing entries, modify, and add new entries
class LexicalEntry:

  def __init__(self, json_object):
    try:
      self._id = json_object["_id"]
    except:
      self._id = None
    try:
      self.lex_id = json_object["lex_id"]
    except:
      self.lex_id = ""
    try:
      self.status = json_object["status"]
    except:
      self.status = ""
    try:
      self.sound = json_object["sound"]
    except:
      self.sound = ""
    try:
      self.language = json_object["language"]
    except:
      self.language = ""
    try:
      self.date_modified = json_object["date_modified"]
    except:
      self.date_modified = strftime("%Y-%m-%d %H:%M:%S")
    try:
      self.image = json_object["image"]
    except:
      self.image = ""
    try:
      self.gloss = json_object["gloss"]
    except:
      self.gloss = ""
    # Try multiple for senses, as there should always be a sense with the gloss as its definition
    try:
      self.senses = json_object["senses"]
    except:
      self.senses = [{}]
    try:
      self.senses = [{"definition": json_object["gloss"]}]
    except:
      self.senses = [{}]
    try:
      self.pos = json_object["pos"]
    except:
      self.pos = ""
    try:
      self.parent_lex = json_object["parent_lex"]
    except:
      self.parent_lex = ""
    try:
      self.morphology = json_object["morphology"]
    except:
      self.morphology = ""
    try:
      self.derivations = json_object["derivations"]
    except:
      self.derivations = {}
    try:
      self.allolexemes = json_object["allolexemes"]
    except:
      self.allolexemes = []
    try:
      self.lex = json_object["lex"]
    except:
      self.lex = ""
    try:
      self.date_added = json_object["date_added"]
    except:
      self.date_added = strftime("%Y-%m-%d %H:%M:%S")
    try:
      self.base_form = json_object["base_form"]
    except:
      self.base_form = ""
    try:
      self.examplefrequency = json_object["examplefrequency"]
    except:
      self.examplefrequency = 0
    try:
      self.parent_lexid = json_object["parent_lexid"]
    except:
      self.parent_lexid = ""
    try:
      self.parent_rel = json_object["parent_rel"]
    except:
      self.parent_rel = ""
    try:
      self.examples = json_object["examples"]
    except:
      self.examples = []

  def add_to_json_lexicon(json_lexicon):
    return ""

  def add_sense():
    return ""

  def update_sense():
    return ""

  def postprocessing_for_json_lexicon(self):

    # Preprocessing
    # Change the '-' in derivations keys back to a '.'
    d = self.derivations
    if isinstance(d, dict):
      for key in d.keys():
        d[re.sub("-", ".", key)] = d.pop(key)

    self.derivations = d


lexicon_keys = [ "sound", "senses", "language", "date_modified", "image", "gloss", "pos", "parent_lex", "morphology", "derivations", "allolexemes", "lex", "date_added", "base_form", "examplefrequency", "parent_lexid", "parent_rel", "examples"]
