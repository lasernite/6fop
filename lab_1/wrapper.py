import lab, json
reload(lab) # this forces the student code to be reloaded when page is refreshed

def run_test( input_data ):
  f = getattr(lab, input_data["function"])
  return f(**input_data["inputs"])

music_genome = []
def init():
  global music_genome
  music_genome = []
  with open('resources/music.json') as data_file:
    music_file = json.load(data_file)
    for track in music_file:
      music_genome.append(track["genes"])

def next( d ):
  return lab.next_song( d["likes"], d["dislikes"], music_genome )

init()
