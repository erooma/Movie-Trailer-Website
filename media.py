import webbrowser


class Movie():
    """ This class provides a way to store movie related information """

    def __init__(self, movie_title, movie_year, movie_director, movie_actors,
    	         movie_storyline, poster_image, trailer_youtube):
                     self.title = movie_title
                     self.year = movie_year
                     self.director = movie_director
                     self.actors = movie_actors
                     self.storyline = movie_storyline
                     self.poster_image_url = poster_image
                     self.trailer_youtube_url = trailer_youtube
		
    def show_trailer(self):
        webbrowser.open(self.trailer_youtube_url)