import webbrowser
import os
import re


# Styles and scripting for the page
main_page_head = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <title>Flixnet!</title>
    <!-- Bootstrap 3 -->
    <link rel="stylesheet" href="https://netdna.bootstrapcdn.com/bootstrap/3.1.0/css/bootstrap.min.css">
    <link rel="stylesheet" href="https://netdna.bootstrapcdn.com/bootstrap/3.1.0/css/bootstrap-theme.min.css">
    <script src="http://code.jquery.com/jquery-1.10.1.min.js"></script>
    <script src="https://netdna.bootstrapcdn.com/bootstrap/3.1.0/js/bootstrap.min.js"></script>
    <style type="text/css" media="screen">
        body {
            padding-top: 80px;
            background-color: #ECF8F9;
        }
        .btn-trailer {
            margin-bottom: 5px;
            width:145px;
            font-size: 14px;
        }
        .btn-storyinfo {
            margin-bottom: 5px;
            width:145px; 
            font-size: 14px;      
        }
        #trailer .modal-dialog {
            margin-top: 200px;
            width: 640px;
            height: 480px;
        }
        #storyinfo .modal-dialog {
            margin-top:200px;
            width: 200px:
            height: 200px;
        }
        .hanging-close {
            position: absolute;
            top: -12px;
            right: -12px;
            z-index: 9001;
        }
        #trailer-video {
            width: 100%;
            height: 100%;
        }
        #storyinfo-container {
            padding:10px;
            font: Constantia, "Lucida Bright", "DejaVu Serif", Georgia, serif;
            border: 4px solid black;
            background-color: #EEE;
        }
        .menu-plus{
            font-size: 18px;
        }
        .movie-tile {
            margin-bottom: 20px;
            padding-top: 20px;
        }
        .movie-tile:hover {
            background-color: #A3dfe6;
            cursor: pointer;
        }
        .scale-media {
            padding-bottom: 56.25%;
            position: relative;
        }
        .scale-media iframe {
            border: none;
            height: 100%;
            position: absolute;
            width: 100%;
            left: 0;
            top: 0;
            background-color: white;
        }
        .storyline {
            display:none;
            align-content:center;
            font:Constantia, "Lucida Bright", "DejaVu Serif", Georgia, serif;
            font-size:16px;
            font-weight:bold;
            text-align: center;
            margin-top: -342px;
            padding-top: 10px;
            padding-left: 5px;
            padding-right: 5px;
            height: 342px;
            width: 75%
            background-color: #33B1C0;
        }
    </style>
    <script type="text/javascript" charset="utf-8">
        // Display the trailer and info buttons when the mouse hovers over the image
        $(document).on('mouseover', '.movie-tile', function () {
            $(this).find('img').css({'height': '225px', 'width': '145px', 'margin-top': '117px', 'margin-bottom': '0px'});  
            $(this).find('.storyline').css({'display':'block'});
        });
        $(document).on('mouseout', '.movie-tile', function () {
            $(this).find('img').css({'height': '342px', 'width': '220px', 'margin-top': '0px', 'margin-bottom': '0px'});
            $(this).find('.storyline').css({'display': 'none'});
        });
        // Pause the video when the modal is closed
        $(document).on('click', '.hanging-close, .modal-backdrop, .modal', function (event) {
            // Remove the src so the player itself gets removed, as this is the only
            // reliable way to ensure the video stops playing in IE
            $("#trailer-video-container").empty();
        });
        // Start playing the video whenever the trailer modal is opened
        $(document).on('click', '.btn-trailer', function (event) {
            var trailerYouTubeId = $(this).attr('data-trailer-youtube-id');
            if (trailerYouTubeId == 'None') {
                var sourceUrl = 'trailer_not_found.html';
            } else {
                var sourceUrl = 'http://www.youtube.com/embed/' + trailerYouTubeId + '?autoplay=1&html5=1';
            };
            $("#trailer-video-container").empty().append($("<iframe></iframe>", {
              'id': 'trailer-video',
              'type': 'text-html',
              'src': sourceUrl,
              'frameborder': 0
            }));
        });
          // Show the movie information whenever the information modal is opened
        $(document).on('click', '.btn-storyinfo', function (event) {
            var movie_information=$(this).attr('data-storyinfo-id');
            var movie_year=$(this).attr('data-year');
            var movie_title=$(this).attr('id');
            movie_title=movie_title.replace(/_/g, ' ');
            var movie_director=$(this).attr('data-director');
            var movie_actors=$(this).attr('data-actors');
            $("#storyinfo-container").empty().html(function() {
              return '<h3>'+movie_title+'</h3><p><span style="font-weight: bold;">Year of production:</span>'+movie_year+'</p><p><span style="font-weight: bold;">Director:</span>'+movie_director+'</p><p><span style="font-weight: bold;">Actors:</span>'+movie_actors+'</p><p><span style="font-weight: bold;">Movie synopsis:</span>'+movie_information+'</p>';
            });
        });
        // Animate in the movies when the page loads
        $(document).ready(function () {
          $('.movie-tile').hide().first().show("fast", function showNext() {
            $(this).next("div").show("fast", showNext);
          });
        });
        //Search for a movie
        $(document).on('click', '#btn-search', function(event) {
            var term=$('#movie-search').val();
            $('#movie-search').attr('placeholder', 'Search for a movie').val('').focus().blur();
            term=term.replace(/\s+/g, '_');
            term='#'+term;
            $term=$(term);
            content='';
            content=$term.closest('div.movie-tile').offset();
            if (content) {
                window.scrollTo(0,content.top);
            } else {
                $('#btn-search').popover('show');
                $('#btn-search').mouseover(function() {
                    $(this).popover('hide');
                });
            };
            
            event.preventDefault();
        });
    </script>
</head>
'''


# The main page layout and title bar
main_page_content = '''
  <body>
    <!-- Trailer Video Modal -->
    <div class="modal" id="trailer">
      <div class="modal-dialog">
        <div class="modal-content">
          <a href="#" class="hanging-close" data-dismiss="modal" aria-hidden="true">
            <img src="https://lh5.ggpht.com/v4-628SilF0HtHuHdu5EzxD7WRqOrrTIDi_MhEG6_qkNtUK5Wg7KPkofp_VJoF7RS2LhxwEFCO1ICHZlc-o_=s0#w=24&h=24"/>
          </a>
          <div class="scale-media" id="trailer-video-container">
          </div>
        </div>
      </div>
    </div>
     <!-- Storyinfo Modal -->
    <div class="modal" id="storyinfo">
      <div class="modal-dialog modal-sm">
        <div class="modal-content">
          <a href="#" class="hanging-close" data-dismiss="modal" aria-hidden="true">
            <img src="https://lh5.ggpht.com/v4-628SilF0HtHuHdu5EzxD7WRqOrrTIDi_MhEG6_qkNtUK5Wg7KPkofp_VJoF7RS2LhxwEFCO1ICHZlc-o_=s0#w=24&h=24"/>
          </a>
          <div class="scale-media" id="storyinfo-container">
          </div>
        </div>
      </div>
    </div>
    <!-- Main Page Content -->
    <div class="container">
      <div class="navbar navbar-inverse navbar-fixed-top" role="navigation">
        <div class="container">
          <div class="navbar-header">
            <button type="button" class="navbar-toggle collapsed" data-toggle="collapse" data-target="#topFixedNavbar1">
                <span class="sr-only">Toggle navigation</span><span class="icon-bar"></span><span class="icon-bar"></span><span class="icon-bar"></span>
            </button>
            <a class="navbar-brand" href="#"><img src="brand.jpg" height="26px" width="80px" alt="Flixnet!" /> All your favorite movie trailers!</a>
           </div>
            <!-- Collect the nav links, forms, and other content for toggling -->
            <div class="collapse navbar-collapse" id="topFixedNavbar1">
                <form class="navbar-form navbar-right">
                    <div class="form-group">
                    <input type="text" class="form-control" placeholder="Search for a movie" id="movie-search">
                    </div>
                    <button class="btn btn-default" id="btn-search" data-container="body" data-toggle="popover"  data-placement="bottom" data-content="Sorry we couldn't find that movie. Please try again.">Submit</button>
                </form>       
            </div>
            <!-- /.navbar-collapse -->
          </div>
        </div>
      </div>
    </div>
    <div class="container">
      {movie_tiles}
    </div>
  </body>
</html>
'''


# A single movie entry html template
movie_tile_content = '''
<div class="col-xs-6 col-md-4 movie-tile text-center">
    <img src="{poster_image_url}" alt="Sorry, this movie poster wasn't found." width="220" height="342">
        <div class="storyline">
            <button type="button" class="btn btn-info btn-lg btn-trailer" data-trailer-youtube-id="{trailer_youtube_id}" data-toggle="modal" data-target="#trailer">Movie trailer</button>
            <button type="button" class="btn btn-info btn-lg btn-storyinfo" id="{movie_ID}" data-director="{movie_director}" data-actors="{movie_actors}" data-storyinfo-id="{movie_storyline}" data-year="{movie_year}" data-toggle="modal" data-target="#storyinfo">Movie information</button>
        </div>
    
    <h3>{movie_title}</h3><br />
</div>
'''


def create_movie_tiles_content(movies):
    # The HTML content for this section of the page
    content = ''
    for movie in movies:
        # Extract the youtube ID from the url
        youtube_id_match = re.search(
            r'(?<=v=)[^&#]+', movie.trailer_youtube_url)
        youtube_id_match = youtube_id_match or re.search(
            r'(?<=be/)[^&#]+', movie.trailer_youtube_url)
        trailer_youtube_id = (youtube_id_match.group(0) if youtube_id_match
                              else None)

        # Append the tile for the movie with its content, information and ID 
        movie_ID=movie.title.replace(" ", "_")
        content += movie_tile_content.format(
            movie_title=movie.title,
            movie_ID=movie_ID,
            movie_year=movie.year,
            movie_director=movie.director,
            movie_actors=movie.actors,
            movie_storyline=movie.storyline,
            poster_image_url=movie.poster_image_url,
            trailer_youtube_id=trailer_youtube_id
        )
    return content


def open_movies_page(movies):
    # Create or overwrite the output file
    output_file = open('flixnet.html', 'w')

    # Replace the movie tiles placeholder generated content
    rendered_content = main_page_content.format(
        movie_tiles=create_movie_tiles_content(movies))

    # Output the file
    output_file.write(main_page_head + rendered_content)
    output_file.close()

    # open the output file in the browser (in a new tab, if possible)
    url = os.path.abspath(output_file.name)
    webbrowser.open('file://' + url, new=2)