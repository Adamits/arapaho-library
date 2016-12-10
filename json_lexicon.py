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
