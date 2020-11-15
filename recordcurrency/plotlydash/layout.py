html_layout = '''
<!DOCTYPE html>
<html>

  <head>
      {%metas%}
      <title>{%title%}</title>
      {%favicon%}
      {%css%}
  </head>

  <head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <meta name="description"
          content="{% block meta_description %}{% endblock %}">

    <!-- <title>{% block title %}{% endblock %}</title> -->



    <link
      rel="stylesheet"
      href="static/styles/vendor/bootstrap.min.css">
    <link
      rel="stylesheet"
      href="static/styles/main.css">
    <link
      rel="stylesheet"
      href="static/styles/vendor/font-awesome.min.css">
    <script src="https://code.jquery.com/jquery-1.12.2.min.js"
            integrity="sha256-lZFHibXzMHo3GGeehn1hudTAP3Sc0uKXBXAzHX1sjtk="
            crossorigin="anonymous"></script>
  </head>
  <body>
    <nav class="navbar navbar-default navbar-fixed-top">
      <div class="container">
        <div class="navbar-header">
          <button type="button" class="navbar-toggle collapsed"
                  data-toggle="collapse" data-target="#navbar"
                  aria-expanded="false" aria-controls="navbar">
            <span class="sr-only">Toggle navigation</span>
            <span class="icon-bar"></span>
            <span class="icon-bar"></span>
            <span class="icon-bar"></span>
          </button>
          <a href="{{ url_for('page.home') }}">
            <img src="{{ url_for('static', filename='images/ism-logo.png') }}"
                 class="img-responsive"
                 width="229" height="50" title="ISM" alt="ISM"/>
          </a>
        </div>
      </div>
    </nav>


    <main class="container">
    {%app_entry%}
    </main>

    <footer class="footer text-center">
      <div class="container">
        <ul class="list-inline">
          <li class="text-muted">ISM &copy; 2020</li>
          <li><a href="{{ url_for('page.privacy') }}">Privacy Policy</a></li>
          <li><a href="{{ url_for('page.terms') }}">Terms of Service</a></li>
          <li><a href="{{ url_for('page.faqs') }}">FAQs</a></li>


        </ul>
      </div>
    {%config%}
    {%scripts%}
    {%renderer%}
    </footer>

    <script
      src="{{ url_for('static', filename='scripts/vendor/bootstrap.min.js') }}">
    </script>
  </body>
</html>
'''