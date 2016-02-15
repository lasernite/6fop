def next_song(likes, dislikes, music):
  # Return the song id in range(0, len(music)) as per the lab assignment
  import operator

  # Remove likes and dislikes from new music object
  unplayed_music = {}
  likes_dislikes = likes + dislikes
  for i in range(len(music)):
  	# Only add to unplayed_music if not in likes or dislikes
  	if i not in likes_dislikes:
  		unplayed_music[i] = music[i] 
  
  # Average Distance Function
  def average_distance(song, rated_songs):
  	# No ratings to calculate
  	if not rated_songs:
  		return 0
  	# Otherwise calculate
  	total_distance = 0
  	for rated_song_index in rated_songs:
  		total_distance += get_distance(song, rated_song_index)

  	# Return average distance from song to rated songs
  	return float(total_distance)/len(rated_songs)

  # Get genetic distance between two songs
  def get_distance(song, rated_song_index):
  	distance = 0
  	for gene in range(len(song)):
  		# If genes don't match, increase distance
  		if not song[gene] == music[rated_song_index][gene]:
  			distance += 1
  	return distance

  # Get the goodness of all music
  def goodness(music, likes, dislikes, goodness_dic):
  	for song_index in unplayed_music.keys():
  		goodness_dic[song_index] = average_distance(music[song_index], dislikes) - average_distance(music[song_index], likes)

  goodness_dic = {}
  # Call function
  goodness(music, likes, dislikes, goodness_dic)

  # Return most liked song
  return max(goodness_dic.items(), key=operator.itemgetter(1))[0]
