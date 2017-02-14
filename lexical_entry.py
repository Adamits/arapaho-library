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
