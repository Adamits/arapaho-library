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

  def test(self):
    print "yo doogo"

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
