import flixnet
import media
from content import movies


# entertainment_center.py
# Author: Andrew Moore (modified from fresh.tomatoes.py, Udacity.com
# Last modified by Andrew Moore
# 2015/10/24
# sorts the movies alphabetically and then opens the web page renderer
sorted_movies = sorted(movies, key=lambda x: x.title)
flixnet.open_movies_page(sorted_movies)